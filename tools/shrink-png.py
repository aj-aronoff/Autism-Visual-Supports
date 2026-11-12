#!/usr/bin/env python3
"""Bring rasterized PNGs under an upload size limit, losslessly where possible.

    python3 tools/shrink-png.py [--limit 524288] [--apply] [file ...]

Chrome writes 24/32-bit PNGs. Our artwork is flat vector, so two steps usually
suffice and the first one changes nothing at all:

  1  re-encode with zlib level 9 and optimize=True   -- pixel-identical
  2  adaptive palette, 256 then 192 then 128 colours -- only if step 1 misses

A file already under the limit is left alone. A result that is not smaller is
discarded. Without --apply this is a dry run.

Re-run it after re-rasterizing from SVG: a fresh Chrome render is step-0 again.
"""
import argparse, os, sys, glob
from PIL import Image

def encode(im, path, **kw):
    im.save(path, "PNG", optimize=True, compress_level=9, **kw)
    return os.path.getsize(path)

def shrink(path, limit, apply_):
    start = os.path.getsize(path)
    if start <= limit:
        return (path, start, start, "under the limit", False)
    im = Image.open(path); im.load()
    tmp = path + ".tmp"
    best, how = None, None

    size = encode(im, tmp)                       # step 1, pixel-identical
    if size < start:
        best, how = size, "re-encoded, pixels unchanged"
    if best is None or best > limit:
        for colours in (256, 192, 128):
            # RGBA only supports FASTOCTREE; flatten first where there is no
            # real transparency so MEDIANCUT (better for flat art) can be used
            src = im.convert("RGBA")
            opaque = src.getchannel("A").getextrema() == (255, 255)
            if opaque:
                q = src.convert("RGB").quantize(colors=colours, method=Image.MEDIANCUT)
            else:
                q = src.quantize(colors=colours, method=Image.FASTOCTREE)
            s = encode(q, tmp)
            if s <= limit:
                best, how = s, "%d-colour palette" % colours
                break
            if best is None or s < best:
                best, how = s, "%d-colour palette" % colours
    if best is None or best >= start:
        os.path.exists(tmp) and os.remove(tmp)
        return (path, start, start, "could not improve", False)
    if apply_:
        os.replace(tmp, path)
    else:
        os.remove(tmp)
    return (path, start, best, how, best <= limit)

a = argparse.ArgumentParser()
a.add_argument("files", nargs="*")
a.add_argument("--limit", type=int, default=512*1024)
a.add_argument("--apply", action="store_true")
o = a.parse_args()
here = os.path.dirname(os.path.abspath(__file__))
files = o.files or sorted(glob.glob(os.path.join(here, "..", "assets", "*.png")))

print("limit %d bytes%s\n" % (o.limit, "" if o.apply else "   (DRY RUN - pass --apply to write)"))
print("%-34s %9s %9s  %s" % ("FILE", "BEFORE", "AFTER", "HOW"))
touched = fails = 0
for f in files:
    p, s0, s1, how, ok = shrink(f, o.limit, o.apply)
    if how == "under the limit":
        continue
    touched += 1
    flag = "" if ok else "   STILL OVER"
    print("%-34s %9d %9d  %s%s" % (os.path.basename(p), s0, s1, how, flag))
    if not ok: fails += 1
print("\n%d file(s) over the limit, %d still over afterwards" % (touched, fails))
sys.exit(1 if fails else 0)
