# Videos

| File | Slot | Behaviour |
| --- | --- | --- |
| `riskprismpromo.mp4` | Cover video at the top of the page | autoplay, loop |
| `keepout_comparison.mp4` | Real-robot scenario 1 — Keep-Out Zones | autoplay on scroll, loop |
| `avoidance_comparison.mp4` | Real-robot scenario 2 — Hazard Avoidance | autoplay on scroll, loop |
| `keepin_comparison.mp4` | Real-robot scenario 3 — Keep-In Zones | autoplay on scroll, loop |
| `looped_gauntlet_full5x.mp4` | The RiskPrism Gauntlet | click to play, loop |

Everything is muted; none of these files carries an audio track at all.

The three scenario clips carry `data-autoplay`, so `assets/js/main.js` pauses
them while scrolled out of view and resumes on re-entry. The Gauntlet is
deliberately click-to-play — at ~57 MB, autoplaying it would download more than
the rest of the page combined. To autoplay it anyway, add `autoplay` and
`data-autoplay` to its `<video>` tag in `index.md`.

To swap a clip, replace the file and update the matching `<source>` in
`index.md`. Keep each under ~20 MB — GitHub Pages allows 100 MB per file and
1 GB per site, but large files make the page slow to load. H.264 in an `.mp4`
container plays everywhere:

```sh
ffmpeg -i input.mov -vf "scale=1280:-2" -c:v libx264 -crf 26 -preset slow \
       -pix_fmt yuv420p -movflags +faststart -an output.mp4
```

`-movflags +faststart` matters: it moves the index to the front of the file so
playback can begin before the whole clip has downloaded.
