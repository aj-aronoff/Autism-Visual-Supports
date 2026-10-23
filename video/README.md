# Concept video

60 seconds, 1920×1080, 30fps, silent.

**The rendered MP4 is deliberately not committed.** It is a 16 MB binary that these
scripts rebuild in about seventeen seconds, and the finished video lives on YouTube
rather than in version control. Everything needed to reproduce it byte-for-byte is
here.

Not the hackathon submission video. The submission (due 9 November) has to be a
walkthrough of the running ODC application that the judges can replicate, and that
gets recorded during the build week. This is the pitch: the problem, the evidence,
and what the application will do.

## Regenerating

```bash
python3 build_video.py          # writes the 12 frame SVGs
# rasterize each to PNG at 1920x1080 with headless Chrome
python3 make_video.py           # assembles with ffmpeg: slow push + crossfades
```

`build_video.py` imports `assets/build_art.py`, so the frames use exactly the same
figures, palette and First→Then board the product itself draws. Change the artwork
and the video follows.

## Shot list

| # | Frame | Beat |
|---|---|---|
| 1 | `f01-open` | Title |
| 2 | `f02-four-minutes` | The scene: four minutes to get out the door |
| 3 | `f03-what-works` | What works is a picture |
| 4 | `f04-forty-minutes` | What it costs to make one by hand |
| 5 | `f05-trust` | The TRIAD quote — the thesis |
| 6 | `f06-three-questions` | The ask |
| 7 | `f07-three-things` | Cards, script, plan |
| 8 | `f08-loop` | Twilio closes the loop |
| 9 | `f09-promises` | Promises kept, not boards made |
| 10 | `f10-agents` | Three agents, grounded |
| 11 | `f11-why` | Why this team |
| 12 | `f12-end` | End card |

## Audio

Deliberately silent. A synthetic voice reading "my daughter is autistic" is worse
than no voice at all. Narration should be recorded by the author.
