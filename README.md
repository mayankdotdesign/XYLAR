# Xylar Fund Report — v2 handoff package

Everything needed to rebuild, edit, and re-issue the Xylar Private fund report
(JioBlackRock Flexi Cap Fund) exactly as designed. Drop this folder into any machine
with Claude Code and say: *"Read CLAUDE.md, then build and open the report."*

## Contents

```
XYLAR/
├── CLAUDE.md                  ← brand system + editing rules (Claude Code reads this automatically)
├── README.md                  ← this file
├── build.py                   ← python3 build.py → emits the final single-file report
├── brief-template-v2.html     ← THE source. Edit DATA object for new issues.
├── assets/
│   ├── xylar-logo.svg         ← Xylar wordmark (white, for dark grounds)
│   ├── fonts/
│   │   ├── denton/            ← Denton Test cut: Light, LightItalic, Regular, RegularItalic
│   │   └── geist/             ← Geist variable font + OFL license
│   └── vendor/
│       ├── three.min.js       ← Three.js r128 (classic global build) — powers the horizon cover
│       └── gsap.min.js        ← GSAP 3.12.5 — cover intro/pulse tweens
└── reference/
    ├── xylar-flexicap-report-v2.html          ← known-good built output (open in browser)
    └── JioBlackRock-FlexiCap-Presentation.pdf ← 12-page source deck (all content derives from it)
```

## Quick start

```bash
python3 build.py                      # → xylar-flexicap-report-v2.html (~1.1 MB, self-contained)
python3 -m http.server 8000           # then open http://localhost:8000/xylar-flexicap-report-v2.html
```

The built file has fonts, Three.js, and GSAP embedded — it can be emailed, hosted
anywhere, or opened by double-clicking with zero external requests. No dependencies,
no build tools beyond Python 3 stdlib. (The template itself also runs directly from
this folder, where the vendor scripts load via `<script src>`.)

## The cover — "the intelligence horizon"

The report opens on a halftone-horizon hero (adopted from the standalone
`xylar-hero-horizon` package, re-set in Denton instead of Advercase): a rim-lit
ring rising from below the fold — two concentric circle strokes with a beam-gradient
glow (orange → cream → cyan → blue) in the gap — rendered as a halftone dot screen
where each dot's size tracks the underlying brightness. A cursor magnifier grows
dots near the pointer and the glow breathes at idle. It's a full-screen Three.js
fragment shader inside the `cover()` IIFE: `sceneColor()` builds the ring + glow,
`main()` applies the halftone. Key knobs: `uRes.y / 95.0` (dot pitch), `R`/`ringW`/`sw`
(ring geometry), `c.y` (arc height), the `0.195` bloom falloff, and the `ramp()` stops.
The report's own cover content (eyebrow, headline, CTAs, NFO meta chips) sits on top.

## Issuing a new report (the monthly workflow)

1. Open `brief-template-v2.html`, find `const DATA = {` near the top of the `<script>`.
2. Edit content there: issue number/date, fund metadata, stats, chart series, copy, footnotes.
   Everything visible on the page is driven from this object.
3. `python3 build.py`. Done.

Design tokens (colors/type/materials) live in `:root` in the CSS and should not change —
they are the locked Xylar brand system. See `CLAUDE.md` for the full rules, including
when the beam gradient may and may not be used.

## Licensing notes

- **Geist** — SIL Open Font License (included at `assets/fonts/geist/OFL.txt`). Fine to embed.
- **Denton** — these are the free *Test* files. Confirm a commercial webfont/embedding license
  before sending to real clients.
- **Three.js** (MIT) and **GSAP** (standard "no charge" license) — vendored in `assets/vendor/`.
- Fund content © Jio BlackRock Asset Management; sourced from their public NFO presentation.
- Note: the original brand-guideline boards (Figma screenshots) are not included as images;
  their rules are fully transcribed in `CLAUDE.md`.
