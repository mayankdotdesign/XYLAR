#!/usr/bin/env python3
"""
Assemble the Xylar fund reports: inject base64 fonts, the vendored JS
libraries (Three.js + GSAP, used by the horizon cover), and image assets
into each template, emit single self-contained HTML files — zero external
requests.

Usage:  python3 build.py
Output: xylar-flexicap-report-v2.html   (original material system)
        xylar-flexicap-report-v3.html   (smoked glass & machined metal)

All paths are relative to this script — the package works from any location.
"""
import base64, pathlib

ROOT = pathlib.Path(__file__).parent
DENTON = ROOT / 'assets' / 'fonts' / 'denton'
GEIST = ROOT / 'assets' / 'fonts' / 'geist'
VENDOR = ROOT / 'assets' / 'vendor'

TEMPLATES = {
    'brief-template-v2.html': 'xylar-flexicap-report-v2.html',
    'brief-template-v3.html': 'xylar-flexicap-report-v3.html',
}

FONTS = {
    '%%DENTON_LIGHT%%':          DENTON / 'DentonTest-Light.otf',
    '%%DENTON_LIGHT_ITALIC%%':   DENTON / 'DentonTest-LightItalic.otf',
    '%%DENTON_REGULAR%%':        DENTON / 'DentonTest-Regular.otf',
    '%%DENTON_REGULAR_ITALIC%%': DENTON / 'DentonTest-RegularItalic.otf',
    '%%GEIST_VAR%%':             GEIST / 'Geist-VariableFont_wght.ttf',
}

# vendor <script src> tags swapped for inline scripts so the built file
# renders the cover with no network access (template stays runnable from
# the folder directly, where the src= form works as-is)
VENDOR_SCRIPTS = ['three.min.js', 'gsap.min.js']

# CSS url() image assets swapped for data URIs (v3 photo backdrops)
IMAGES = {
    "url('assets/img/rock.webp')": ROOT / 'assets' / 'img' / 'rock.webp',
}

for tpl, outname in TEMPLATES.items():
    html = (ROOT / tpl).read_text()
    for token, path in FONTS.items():
        b64 = base64.b64encode(path.read_bytes()).decode()
        assert token in html, f'{tpl}: missing token {token}'
        html = html.replace(token, b64)
    for name in VENDOR_SCRIPTS:
        tag = f'<script src="assets/vendor/{name}"></script>'
        assert tag in html, f'{tpl}: missing vendor tag {tag}'
        js = (VENDOR / name).read_text()
        html = html.replace(tag, f'<script>\n{js}\n</script>')
    for ref, path in IMAGES.items():
        if ref in html:
            b64 = base64.b64encode(path.read_bytes()).decode()
            html = html.replace(ref, f'url(data:image/webp;base64,{b64})')
    out = ROOT / outname
    out.write_text(html)
    print(f'wrote {out} ({out.stat().st_size/1024:.0f} KB)')
