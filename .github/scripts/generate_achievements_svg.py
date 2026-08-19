"""
Generate a terminal-style Achievements SVG card.
Two-line CLI entries (title then position/prize) with SMIL clip-wipe animations.
"""
import os, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "achievements.svg")

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

W, TITLEBAR = 460, 30
PAD         = 18
FONT        = 13
LINE_H      = 18

# (title, color, position, prize) — prize is highlighted separately when set
ENTRIES = [
    ("BCH-1 Hackcelerator", GOLD,   "Overall Winner",  "$10,000"),
    ("Web3Conf'25 Hackathon", GREEN, "First Runner-Up", "$800"),
    ("ETHnile", PURPLE,              "Winner",          None),
    ("Cardano Asia Hackathon", CYAN, "Top 5 Finalist", "200+ teams · 3k+ regs"),
    ("LeetCode Contest", RED,        "Rating 1600+",    None),
]

ROW_DUR = 0.10
STAGGER = 0.14

# header + detail + spacer per entry
total_lines = len(ENTRIES) * 3
H = TITLEBAR + PAD + total_lines * LINE_H + PAD

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" '
           f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">')

svg.append(f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
           f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
           f'</linearGradient></defs>')
svg.append(f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>')
svg.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>')

svg.append(f'<line x1="0" y1="{TITLEBAR}" x2="{W}" y2="{TITLEBAR}" stroke="{FRAME}"/>')
for i, c in enumerate(["#ff5f56","#ffbd2e","#27c93f"]):
    svg.append(f'<circle cx="{PAD+i*16}" cy="{TITLEBAR//2}" r="5" fill="{c}"/>')
svg.append(f'<text x="{W//2}" y="{TITLEBAR//2+4}" fill="{TITLE_CLR}" font-size="12" '
           f'text-anchor="middle">nishanthcr7777@github: ~/achievements</text>')


def wipe(idx, y, content):
    delay = idx * STAGGER
    svg.append(f'<clipPath id="a{idx}"><rect x="{PAD}" y="{y-2}" height="{LINE_H+2}" width="0">'
               f'<animate attributeName="width" from="0" to="{W-PAD*2}" '
               f'begin="{delay:.3f}s" dur="{ROW_DUR:.2f}s" fill="freeze"/>'
               f'</rect></clipPath>')
    svg.append(f'<g clip-path="url(#a{idx})">{content}</g>')
    svg.append(f'<rect y="{y}" width="7" height="{LINE_H-3}" fill="{MAIN}" opacity="0">'
               f'<animate attributeName="x" from="{PAD}" to="{W-PAD}" '
               f'begin="{delay:.3f}s" dur="{ROW_DUR:.2f}s" fill="freeze"/>'
               f'<set attributeName="opacity" to="0.8" begin="{delay:.3f}s"/>'
               f'<set attributeName="opacity" to="0" begin="{delay+ROW_DUR:.3f}s"/></rect>')


y = TITLEBAR + PAD
row_idx = 0

for title, color, position, prize in ENTRIES:
    header = (f'<text xml:space="preserve" x="{PAD}" y="{y + LINE_H * 0.75:.0f}" font-size="{FONT}">'
              f'<tspan fill="{DIM}">&gt; </tspan>'
              f'<tspan fill="{color}" font-weight="bold">{html.escape(title)}</tspan></text>')
    wipe(row_idx, y, header)
    y += LINE_H
    row_idx += 1

    if prize:
        detail = (f'<text xml:space="preserve" x="{PAD + 14}" y="{y + LINE_H * 0.75:.0f}" '
                  f'font-size="{FONT - 1}">'
                  f'<tspan fill="{DIM}">\u2502 </tspan>'
                  f'<tspan fill="{MAIN}">{html.escape(position)}</tspan>'
                  f'<tspan fill="{DIM}">  \u00b7  </tspan>'
                  f'<tspan fill="{GOLD}" font-weight="bold">{html.escape(prize)}</tspan></text>')
    else:
        detail = (f'<text xml:space="preserve" x="{PAD + 14}" y="{y + LINE_H * 0.75:.0f}" '
                  f'font-size="{FONT - 1}">'
                  f'<tspan fill="{DIM}">\u2502 </tspan>'
                  f'<tspan fill="{MAIN}">{html.escape(position)}</tspan></text>')
    wipe(row_idx, y, detail)
    y += LINE_H
    row_idx += 1

    y += LINE_H
    row_idx += 1

end_delay = row_idx * STAGGER
svg.append(f'<rect x="{PAD}" y="{y - LINE_H + 4}" width="8" height="{LINE_H-4}" fill="{CYAN}">'
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
