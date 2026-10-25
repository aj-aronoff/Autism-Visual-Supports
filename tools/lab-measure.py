#!/usr/bin/env python3
"""Measure one model call through the AWS CLI and log what it cost.

Replaces the per-board estimates in TOKEN-BUDGET.md section 3 with measurements,
writing them to the same tools/token-log.csv that token-budget.py reads.

    python3 tools/lab-measure.py --prompt prompts/composer-draft.txt --op Composer
    python3 tools/lab-measure.py --prompt p.txt --op Reviewer --dry-run

Billed to YOUR AWS account, not to the hackathon allocation. Set the budget in
PRE-BUILD-LAB.md section 3 before the first real run.

Uses the AWS CLI rather than boto3, because the CLI is what is installed.
"""
import argparse
import csv
import datetime
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "token-log.csv")
FIELDS = ["date", "day", "operation", "model", "calls",
          "input_tokens", "output_tokens", "images", "notes"]


def run(args, stdin=None, timeout=300):
    p = subprocess.run(args, capture_output=True, text=True,
                       input=stdin, timeout=timeout)
    if p.returncode != 0:
        sys.exit("aws cli failed (%d):\n%s" % (p.returncode, p.stderr.strip()))
    return p.stdout


def converse(model, system, user, max_tokens, temperature, region):
    """One Bedrock Converse call. Returns (text, usage, seconds)."""
    body = {
        "messages": [{"role": "user", "content": [{"text": user}]}],
        "inferenceConfig": {"maxTokens": max_tokens, "temperature": temperature},
    }
    if system:
        body["system"] = [{"text": system}]
    args = ["aws", "bedrock-runtime", "converse",
            "--region", region, "--model-id", model,
            "--cli-input-json", json.dumps(body), "--output", "json"]
    t0 = time.time()
    out = run(args)
    elapsed = time.time() - t0
    data = json.loads(out)
    text = "".join(c.get("text", "")
                   for c in data["output"]["message"]["content"])
    return text, data.get("usage", {}), elapsed


def append(row):
    exists = os.path.exists(LOG)
    with open(LOG, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if not exists:
            w.writeheader()
        w.writerow(row)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True, help="file holding the user prompt")
    ap.add_argument("--system", help="file holding the system prompt")
    ap.add_argument("--op", required=True,
                    choices=["Composer", "Reviewer", "Illustrator"])
    # Bedrock model ids are not the same strings as the Anthropic API uses, and
    # they change. Confirm this default against `aws bedrock list-foundation-models`
    # before trusting it; pass --model explicitly once you know what is enabled.
    ap.add_argument("--model", default="us.anthropic.claude-sonnet-4-5-20250929-v1:0")
    ap.add_argument("--region", default=os.environ.get("AWS_REGION", "us-east-1"))
    ap.add_argument("--max-tokens", type=int, default=2000)
    ap.add_argument("--temperature", type=float, default=0.4)
    ap.add_argument("--day", type=int, default=0,
                    help="build day, for the plan-vs-actual check; 0 for lab runs")
    ap.add_argument("--note", default="lab")
    ap.add_argument("--show", action="store_true", help="print the model output")
    ap.add_argument("--dry-run", action="store_true",
                    help="show what would be sent, call nothing, bill nothing")
    a = ap.parse_args()

    user = open(a.prompt, encoding="utf-8").read()
    system = open(a.system, encoding="utf-8").read() if a.system else None

    if a.dry_run:
        print("model   %s" % a.model)
        print("region  %s" % a.region)
        print("system  %s" % ("%d chars" % len(system) if system else "(none)"))
        print("user    %d chars" % len(user))
        print("\n-- nothing sent, nothing billed --")
        return 0

    text, usage, elapsed = converse(a.model, system, user,
                                    a.max_tokens, a.temperature, a.region)
    tin = usage.get("inputTokens", 0)
    tout = usage.get("outputTokens", 0)

    print("operation     %s" % a.op)
    print("model         %s" % a.model)
    print("input tokens  %s" % "{:,}".format(tin))
    print("output tokens %s" % "{:,}".format(tout))
    print("total         %s" % "{:,}".format(tin + tout))
    print("latency       %.1f s" % elapsed)

    # Does it parse as the output contract? Composer's whole job is that it does.
    if a.op == "Composer":
        body = text.strip()
        if body.startswith("```"):
            body = body.split("\n", 1)[1].rsplit("```", 1)[0]
        try:
            parsed = json.loads(body)
            keys = ", ".join(sorted(parsed)[:6])
            print("contract      parsed ok (%s)" % keys)
        except ValueError as exc:
            print("contract      DID NOT PARSE -- %s" % exc)

    if a.show:
        print("\n" + text)

    append({"date": datetime.date.today().isoformat(), "day": a.day,
            "operation": a.op, "model": a.model.split(".")[-1][:24], "calls": 1,
            "input_tokens": tin, "output_tokens": tout, "images": 0,
            "notes": "%s %.1fs" % (a.note, elapsed)})
    print("\nlogged to %s" % LOG)
    return 0


if __name__ == "__main__":
    sys.exit(main())
