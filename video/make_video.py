#!/usr/bin/env python3
"""Assemble the concept video: slow push on each frame, crossfades between."""
import os, subprocess, shlex

FR = "/mnt/c/users/ajaro/claude/resume/hackathon-future/video/frames"
OUT = "/mnt/c/users/ajaro/claude/resume/hackathon-future/video/Autism-Visual-Supports-concept.mp4"
FPS, FADE = 30, 0.8

# frame, seconds on screen
SHOTS = [
    ("f01-open",           5.0),
    ("f02-four-minutes",   5.5),
    ("f03-what-works",     5.0),
    ("f04-forty-minutes",  5.5),
    ("f05-trust",          7.0),
    ("f06-three-questions",5.0),
    ("f07-three-things",   6.0),
    ("f08-loop",           7.0),
    ("f09-promises",       5.0),
    ("f10-agents",         6.0),
    ("f11-why",            6.0),
    ("f12-end",            5.5),
]

ins, filt, labels = [], [], []
for i, (name, dur) in enumerate(SHOTS):
    ins += ["-i", os.path.join(FR, name + ".png")]   # exactly one frame in; zoompan makes d frames out
    n = int(dur * FPS)
    # alternate the drift so consecutive shots do not feel mechanical
    if i % 3 == 0:
        x, y = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif i % 3 == 1:
        x, y = f"iw/2-(iw/zoom/2)+(on/{n})*110", "ih/2-(ih/zoom/2)"
    else:
        x, y = f"iw/2-(iw/zoom/2)-(on/{n})*110", f"ih/2-(ih/zoom/2)+(on/{n})*60"
    filt.append(
        f"[{i}:v]scale=2880:1620,setsar=1,"
        f"zoompan=z='1+0.085*on/{n}':x='{x}':y='{y}':d={n}:s=1920x1080:fps={FPS},"
        f"format=yuv420p[v{i}]")
    labels.append(f"v{i}")

acc = SHOTS[0][1]
cur = labels[0]
for i in range(1, len(SHOTS)):
    off = acc - FADE
    out = f"x{i}" if i < len(SHOTS) - 1 else "vout"
    filt.append(f"[{cur}][{labels[i]}]xfade=transition=fade:duration={FADE}:offset={off:.2f}[{out}]")
    cur = out
    acc = acc + SHOTS[i][1] - FADE

cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *ins,
       "-filter_complex", ";".join(filt), "-map", "[vout]",
       "-c:v", "libx264", "-preset", "medium", "-crf", "19",
       "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-r", str(FPS), OUT]
print(f"{len(SHOTS)} shots, {acc:.1f}s final")
subprocess.run(cmd, check=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
