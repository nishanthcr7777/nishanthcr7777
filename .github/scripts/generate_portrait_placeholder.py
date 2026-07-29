"""
Write a terminal-style portrait placeholder SVG when no source photo exists.
Replace by running generate_ascii_svg.py after adding assets/source.png.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "portrait.svg")

W, H = 420, 480
TITLEBAR = 30
PAD = 20
BG, BG2 = "#0d1117", "#111722"
FRAME = "#30363d"
TITLE = "#7d8590"
INK = "#c9d1d9"
ACCENT = "#70A5FD"
PURPLE = "#bf91f3"
TEAL = "#38bdae"

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>
<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>
<line x1="0" y1="{TITLEBAR}" x2="{W}" y2="{TITLEBAR}" stroke="{FRAME}"/>
<circle cx="{PAD}" cy="{TITLEBAR/2}" r="5" fill="#ff5f56"/>
<circle cx="{PAD+16}" cy="{TITLEBAR/2}" r="5" fill="#ffbd2e"/>
<circle cx="{PAD+32}" cy="{TITLEBAR/2}" r="5" fill="#27c93f"/>
<text x="{W/2}" y="{TITLEBAR/2 + 4}" fill="{TITLE}" font-size="12" text-anchor="middle">nishanthcr7777@github: ~$ ./portrait.sh</text>
<text x="{W/2}" y="{H/2 - 20}" fill="{ACCENT}" font-size="72" font-weight="bold" text-anchor="middle">NB</text>
<text x="{W/2}" y="{H/2 + 40}" fill="{PURPLE}" font-size="14" text-anchor="middle">NISHANTH B</text>
<text x="{W/2}" y="{H/2 + 62}" fill="{TEAL}" font-size="12" text-anchor="middle">BACKEND · AI-NATIVE SYSTEMS</text>
<text x="{W/2}" y="{H - 28}" fill="{TITLE}" font-size="11" text-anchor="middle">Add assets/source.png to generate ASCII portrait</text>
</svg>
'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"wrote {OUT} {len(svg)} bytes")
