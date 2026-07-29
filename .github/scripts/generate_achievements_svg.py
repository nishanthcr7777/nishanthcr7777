"""
Generate a terminal-style Achievements SVG card.
CLI aesthetic with SMIL animations.
"""
import os, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "achievements.svg")

# Colors
BG, BG2   = "#0d1117", "#111722"
FRAME     = "#30363d"
TITLE_CLR = "#7d8590"
DIM       = "#8b949e"
MAIN      = "#c9d1d9"
GOLD      = "#e3b341"
GREEN     = "#3fb950"
CYAN      = "#79c0ff"
RED       = "#f97583"
PURPLE    = "#d2a8ff"

W, TITLEBAR = 420, 30
PAD, CELL   = 18, 20
FONT        = 13

ROWS = [
    ("*", "BCH-1 Hackcelerator", "Overall Winner · $10,000", GOLD),
    ("*", "Web3Conf'25 Hackathon", "First Runner-Up · $800", GREEN),
    ("*", "Cardano Asia Hackathon", "Top 5 Finalist", CYAN),
    ("*", "LeetCode Contest", "Rating 1600+", RED),
]

ROW_DUR = 0.12
STAGGER = 0.18

num_rows = len(ROWS)
H = TITLEBAR + PAD + num_rows * (CELL + 6) + PAD + 10

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" '
           f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">')

# Background
svg.append(f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
           f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
           f'</linearGradient></defs>')
svg.append(f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>')
svg.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>')

# Title bar
svg.append(f'<line x1="0" y1="{TITLEBAR}" x2="{W}" y2="{TITLEBAR}" stroke="{FRAME}"/>')
for i, c in enumerate(["#ff5f56","#ffbd2e","#27c93f"]):
    svg.append(f'<circle cx="{PAD+i*16}" cy="{TITLEBAR//2}" r="5" fill="{c}"/>')
svg.append(f'<text x="{W//2}" y="{TITLEBAR//2+4}" fill="{TITLE_CLR}" font-size="12" '
           f'text-anchor="middle">nishanthcr7777@github: ~/achievements</text>')

# Rows
start_y = TITLEBAR + PAD
for idx, (icon, title, detail, color) in enumerate(ROWS):
    y = start_y + idx * (CELL + 6)
    delay = idx * STAGGER

    safe_title  = html.escape(title)
    safe_detail = html.escape(detail)

    line = (f'<text xml:space="preserve" x="{PAD}" y="{y + CELL * 0.75:.0f}" font-size="{FONT}">'
            f'<tspan fill="{MAIN}">{icon} </tspan>'
            f'<tspan fill="{color}" font-weight="bold">{safe_title}</tspan>'
            f'<tspan fill="{DIM}">  {safe_detail}</tspan></text>')

    # Clip-wipe animation
    svg.append(f'<clipPath id="a{idx}"><rect x="{PAD}" y="{y}" height="{CELL+4}" width="0">'
               f'<animate attributeName="width" from="0" to="{W - PAD*2}" '
               f'begin="{delay:.3f}s" dur="{ROW_DUR:.2f}s" fill="freeze"/>'
               f'</rect></clipPath>')
    svg.append(f'<g clip-path="url(#a{idx})">{line}</g>')

    # Cursor
    svg.append(f'<rect y="{y+2}" width="8" height="{CELL-2}" fill="{MAIN}" opacity="0">'
               f'<animate attributeName="x" from="{PAD}" to="{W-PAD}" '
               f'begin="{delay:.3f}s" dur="{ROW_DUR:.2f}s" fill="freeze"/>'
               f'<set attributeName="opacity" to="0.85" begin="{delay:.3f}s"/>'
               f'<set attributeName="opacity" to="0" begin="{delay+ROW_DUR:.3f}s"/></rect>')

# Blinking cursor at the end
end_y = start_y + num_rows * (CELL + 6) + 4
end_delay = num_rows * STAGGER + ROW_DUR
svg.append(f'<rect x="{PAD}" y="{end_y}" width="8" height="{CELL-4}" fill="{MAIN}">'
           f'<set attributeName="opacity" to="0" begin="0s"/>'
           f'<set attributeName="opacity" to="1" begin="{end_delay:.3f}s"/>'
           f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
           f'dur="1s" repeatCount="indefinite" begin="{end_delay:.3f}s"/></rect>')

svg.append("</svg>")

out = "".join(svg)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(out)
print(f"wrote {OUT}  {len(out)} bytes  {W}x{H}")
