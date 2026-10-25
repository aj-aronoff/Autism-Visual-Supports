#!/usr/bin/env python3
"""Token burn-rate and reserve check for the hackathon build window.

Reads tools/token-log.csv, compares spend against the allocation, and reports
whether the demo reserve is still intact.

    python3 tools/token-budget.py --allocation 5000000
    python3 tools/token-budget.py --allocation 5000000 --images 500

Allocation is unknown until the 2 November kickoff; pass the figure once it is.
"""
import argparse
import csv
import os
import sys

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token-log.csv")

# From TOKEN-BUDGET.md section 4.
RESERVE_FRACTION = 0.30
RESERVE_FLOOR_TOKENS = 500_000
RESERVE_FLOOR_IMAGES = 150

# Section 5: share of the spendable pool consumed by the end of each build day.
CUMULATIVE_PLAN = {3: 0.30, 4: 0.30, 5: 0.50, 6: 0.75, 7: 0.85, 8: 1.00}

PER_BOARD = 8_000  # section 3 planning figure


def load(path):
    if not os.path.exists(path):
        sys.exit("no log at %s" % path)
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(r for r in fh if not r.startswith("#")):
            if not (row.get("date") or "").strip():
                continue
            rows.append(row)
    return rows


def num(row, key):
    try:
        return int(float(row.get(key) or 0))
    except ValueError:
        return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--allocation", type=int, required=True,
                    help="total token allocation for the team")
    ap.add_argument("--images", type=int, default=0,
                    help="separate per-image quota, if image generation is metered that way")
    ap.add_argument("--log", default=LOG)
    args = ap.parse_args()

    rows = load(args.log)
    spent = sum(num(r, "input_tokens") + num(r, "output_tokens") for r in rows)
    images = sum(num(r, "images") for r in rows)

    reserve = max(int(args.allocation * RESERVE_FRACTION), RESERVE_FLOOR_TOKENS)
    spendable = args.allocation - reserve
    remaining = args.allocation - spent
    headroom = spendable - spent  # before the reserve is touched

    print("Allocation        %12s" % "{:,}".format(args.allocation))
    print("Reserve (demo)    %12s   (%s)" % (
        "{:,}".format(reserve),
        "floor" if reserve == RESERVE_FLOOR_TOKENS else "%d%% of allocation" % (RESERVE_FRACTION * 100)))
    print("Spendable pool    %12s" % "{:,}".format(spendable))
    print("Spent to date     %12s   (%.1f%% of allocation)" % (
        "{:,}".format(spent), 100.0 * spent / args.allocation if args.allocation else 0))
    print("Headroom          %12s   before the reserve is touched" % "{:,}".format(headroom))
    print("Boards affordable %12s   at %s tokens each" % (
        "{:,}".format(max(headroom, 0) // PER_BOARD), "{:,}".format(PER_BOARD)))

    if args.images:
        img_reserve = max(int(args.images * RESERVE_FRACTION), RESERVE_FLOOR_IMAGES)
        print("Images            %12s   of %s, reserve %s" % (
            "{:,}".format(images), "{:,}".format(args.images), "{:,}".format(img_reserve)))
        if images > args.images - img_reserve:
            print("  ! image reserve breached")
    elif images:
        print("Images generated  %12s   (no quota given; pass --images)" % "{:,}".format(images))

    # Burn rate over the last two logged days.
    by_day = {}
    for r in rows:
        by_day.setdefault((r.get("date") or "").strip(), 0)
        by_day[(r.get("date") or "").strip()] += num(r, "input_tokens") + num(r, "output_tokens")
    recent = [by_day[d] for d in sorted(by_day)[-2:]]
    rate = sum(recent) / len(recent) if recent else 0
    if rate:
        print("Burn rate         %12s   per day, last %d logged day(s)" % (
            "{:,}".format(int(rate)), len(recent)))
        print("Reserve reached in%12.1f   days at this rate" % (max(headroom, 0) / rate))

    # Against the plan, if a day number is logged.
    days = [num(r, "day") for r in rows if num(r, "day")]
    verdict, note = "ON TRACK", ""
    if days and spendable > 0:
        day = max(days)
        planned = CUMULATIVE_PLAN.get(day)
        if planned:
            actual = spent / float(spendable)
            print("Plan vs actual     day %d: %.0f%% planned, %.0f%% of spendable used"
                  % (day, planned * 100, actual * 100))
            if actual > planned + 0.15:
                verdict, note = "OVER PLAN", "pull a lever from TOKEN-BUDGET.md section 7 tonight"

    if spent >= args.allocation:
        verdict, note = "EXHAUSTED", "allocation gone; deterministic template only"
    elif headroom <= 0:
        verdict, note = "RESERVE BREACHED", "demo budget is being spent; stop generating and seed the library by hand"
    elif headroom < reserve * 0.25:
        verdict, note = "CLOSE TO RESERVE", "headroom under a quarter of the reserve"

    print()
    print("VERDICT: %s%s" % (verdict, "  -- " + note if note else ""))
    return 0 if verdict in ("ON TRACK",) else 1


if __name__ == "__main__":
    sys.exit(main())
