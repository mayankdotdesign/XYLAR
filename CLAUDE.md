# Xylar Fund Report v2 — project instructions

This folder contains the complete, working source for the **Xylar Private Fund Report** —
a single-file interactive HTML report on the JioBlackRock Flexi Cap Fund, built to validate
Xylar's brand identity. Xylar is a wealth-management platform for UHNWIs; this report is a
recurring (weekly/monthly) client-facing asset.

## How this project works

- Two templates share the same content and engine and differ only in the material layer:
  `brief-template-v2.html` (original toned-down glass) and `brief-template-v3.html`
  ("smoked glass & machined metal": graphite card fills, metallic gradient rims with a
  cursor-tracked specular, page film grain, ink-rimmed paper cards in the light section,
  and darkened rock-photo backdrops — `assets/img/rock.webp` — in the dividers and close).
  Content edits (the DATA object) must be applied to both.
- `brief-template-v2.html` — the reference structure. Three layers, top to bottom:
  1. **CSS design tokens** (`:root`) — brand colors, type, materials. Touch rarely.
  2. **`const DATA = {...}`** at the top of the `<script>` — ALL per-issue content
     (copy, numbers, chart series, footnotes). For a new monthly issue, edit only this.
  3. **Engine** — render functions, canvas scenes, interactions. Don't touch for content changes.
- `python3 build.py` — injects the fonts as base64 and inlines the vendored Three.js + GSAP
  (`assets/vendor/`, used by the horizon cover) into the template and writes
  `xylar-flexicap-report-v2.html` (~1.1MB, fully self-contained, zero external requests).
- `reference/xylar-flexicap-report-v2.html` — the known-good built output. After any change,
  your build should look identical except for what you intentionally changed.
- `reference/JioBlackRock-FlexiCap-Presentation.pdf` — the 12-page source deck. ALL report copy
  is taken near-verbatim from it (this is deliberate — see Tone below). Render pages as images
  to check any chart/diagram before changing data.

## Brand system (locked — do not deviate)

**Type.** Denton (serif) for display headlines and large numerals only, weights Light/Regular.
The signature move: one italic word/phrase per headline (`<em>` = Denton italic) — never bold,
never color, for emphasis. Geist (variable) for everything else: body, labels, buttons, chart
text. Eyebrows are Geist 11px, letterspaced 0.22em, uppercase, #575757.

**Color.** Ground #050505, surfaces #0D0D0D/#1B1B1B, muted #575757, secondary text #B4B2B1,
light section #F9F9F9/#FFFFFF. Accents #D66001 → #F1F0A8 → #9FFFFB → #4757EA exist ONLY as the
"beam" gradient = the intelligence layer. Rule: the beam appears only where AI/systematic
interpretation is literally the subject (the SAE signal path, the beamed statement, "SAE Signal"
funnel stage, highlight-CTA ring). Never on plain data, never as decoration. Historical/factual
charts stay neutral or use semantic colors (the factor heatmap uses muted red/green because
the source deck does).

**Particle vocabulary.** Data point (single dot) → data pool (unstructured dot field) →
signal (activated dot path through a grid) → beam (gradient along the transformation).
All dot-matrix icons, the cover's halftone horizon, the SAE scroll stage, and divider dot
fields derive from this. Scale shifts with context but it is one continuous concept.

**Materials.** Dark frosted glass: `backdrop-filter: blur`, 1px border rgba(255,255,255,.055),
14px radius, faint top specular edge. Premium = restraint: hairlines, negative space, no loud
strokes.

**Personality.** Intelligent, precise, composed, discreet, controlled. NOT loud, playful,
generic-fintech, cyberpunk, or marketing-brochure.

**Tone.** This is a REPORT, not a marketing site. Headlines and body copy are the PDF's own
words, reorganized — do not rewrite into ad copy. Fine print, sources, and SEBI-style
disclosures are part of the design, not an afterthought.

## The cover — "the intelligence horizon" (preserve when editing)

The cover visual is a full-screen Three.js fragment shader (halftone dot screen) inside the
`cover()` IIFE, adopted from the standalone `xylar-hero-horizon` package and re-set in Denton
(never Advercase). `sceneColor()` builds a rim-lit ring rising from below the fold — two
concentric circle strokes with the beam gradient glowing in the gap plus a contained blue
halo above the crest; `main()` renders it as a halftone dot screen (dot radius tracks scene
luminance) with a cursor magnifier. GSAP drives the intro rise (`uIntro`) and idle breathing
(`uPulse`); reduced-motion gets a single static frame. Tuning knobs: `uRes.y / 95.0` dot
pitch, `R`/`ringW`/`sw` ring geometry, `c.y` arc height (crest tops out ~16% up the viewport
so the cover content clears it), `0.195` bloom falloff, and the `ramp()` color stops. The
beam-gradient ring is the intelligence layer made literal — it satisfies the beam rule.

## Interactions (already implemented — preserve when editing)

- Custom cursor: 32px white circle, `mix-blend-mode:difference`, lerp-follow, grows 1.7×
  over interactive elements. Disabled on touch / reduced-motion.
- Card tilt: ~4.5° perspective tilt + pointer-following sheen on `.tilt` cards.
- Scroll reveals (`.rv`), masked line reveals on display headlines (`.mask`), animated
  counters, chart draw-ins (lines sweep, bars grow, heatmap cells cascade).
- SAE scroll-locked canvas stage: chaos → grid+links → beam signal path (380vh section).

## Known gotchas (learned the hard way)

1. Absolutely-positioned `<canvas>` MUST have explicit CSS `width:100%;height:100%` —
   `inset:0` alone does not size a replaced element, and resize events will then double
   the buffer indefinitely (browser gray-screens past ~32k px).
2. `.why-list li` is flex — always wrap injected HTML in a `<span>` or mixed text/`<b>`
   nodes become separate flex items.
3. The turnover line chart (Exhibit A) series are deterministic REDRAWS of the source
   chart's shapes (the PDF publishes no monthly numbers) — footnoted "illustrative".
   The coverage bars and factor heatmap are verbatim source data; keep them exact.
4. Denton files are the free TEST cut (`DentonTest-*.otf`). Verify a commercial license
   before real client distribution. Geist is OFL (license included).

## Verifying changes

Serve the folder (`python3 -m http.server`) and check in a browser: hero reveal, SAE stage
at three scroll depths, both charts + heatmap in the light section, cursor/tilt behavior,
mobile (~390px) for horizontal overflow. Compare against `reference/` output.
