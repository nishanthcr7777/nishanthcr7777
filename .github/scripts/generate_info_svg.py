import os
import sys
import html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "info.svg")

STATIC = bool(os.environ.get("STATIC"))

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
MAIN = "#c9d1d9"
DIM = "#8b949e"
KEY = "#79c0ff"
USER = "#ff7b72"
HOST = "#79c0ff"
CURSOR = "#c9d1d9"
GOLD = "#e3b341"
GREEN = "#3fb950"
CYAN = "#79c0ff"
RED = "#f97583"
PURPLE = "#d2a8ff"
TEAL = "#39d353"

CANVAS_W = 520
TITLEBAR_H = 30
PAD = 22
CELL_H = 20
FONT_SIZE = 13
ROW_DUR = 0.28
STAGGER = 0.22

# Each line: list of (text, color, bold?)  |  None = spacer
LINES = [
    [("nishanthcr7777", USER, False), ("@", MAIN, False), ("github", HOST, False)],
    [("────────────────────────", DIM, False)],
    None,
    [("Role      ", KEY, False), ("Backend Engineer & AI-Native Systems", TEAL, True)],
    None,
    [("Education ", KEY, False), ("B.Tech IT  ·  Chennai Institute of Technology", PURPLE, False)],
    None,
    [("Exp       ", KEY, False), ("SDE Intern @ TVS Automobile Solutions", CYAN, False)],
    [("          ", KEY, False), ("Open-Source Contributor @ BrainGlobe", CYAN, False)],
    None,
    [("Awards    ", KEY, False), ("BCH-1 Hackcelerator", GOLD, True),
     ("  Overall Winner  ", MAIN, False), ("$10,000", GOLD, True)],
    [("          ", KEY, False), ("Web3Conf'25", GREEN, True),
     ("  First Runner-Up  ", MAIN, False), ("$800", GOLD, True)],
    [("          ", KEY, False), ("ETHnile", PURPLE, True),
     ("  Winner", MAIN, False)],
    [("          ", KEY, False), ("Cardano Asia", CYAN, True),
     ("  Top 5  ·  200+ teams  ·  3k+ regs", MAIN, False)],
    [("          ", KEY, False), ("LeetCode", RED, True),
     ("  Contest Rating 1600+", MAIN, False)],
]

content_rows = sum(1 if line is None else 1 for line in LINES)
CANVAS_H = TITLEBAR_H + PAD + content_rows * CELL_H + CELL_H + PAD + 8

parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, '
    f'Menlo, Consolas, monospace">'
)
parts.append(
    '<defs>'
    f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    f'</linearGradient></defs>'
)
parts.append(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#bg)"/>')
parts.append(
    f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" '
    f'fill="none" stroke="{FRAME}" stroke-width="1"/>'
)
parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(
    f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" '
    f'text-anchor="middle">nishanthcr7777@github: ~$ ./info.sh</text>'
)

start_y = TITLEBAR_H + PAD
y = start_y
anim_i = 0

for line in LINES:
    if line is None:
        y += CELL_H
        continue

    delay = anim_i * STAGGER
    text_content = ""
    for item in line:
        text, color = item[0], item[1]
        bold = item[2] if len(item) > 2 else False
        weight = ' font-weight="bold"' if bold else ""
        text_content += f'<tspan fill="{color}"{weight}>{html.escape(text)}</tspan>'

    text_element = (
        f'<text xml:space="preserve" x="{PAD}" y="{y + CELL_H * 0.72:.1f}" '
        f'font-size="{FONT_SIZE}">{text_content}</text>'
    )

    if STATIC:
        parts.append(text_element)
    else:
        parts.append(
            f'<clipPath id="l{anim_i}"><rect x="{PAD}" y="{y}" height="{CELL_H}" width="0">'
            f'<animate attributeName="width" from="0" to="{CANVAS_W - PAD*2}" begin="{delay:.3f}s" '
            f'dur="{ROW_DUR:.2f}s" fill="freeze"/></rect></clipPath>'
        )
        parts.append(f'<g clip-path="url(#l{anim_i})">{text_element}</g>')
        parts.append(
            f'<rect y="{y+2}" width="8" height="{CELL_H-4}" fill="{CURSOR}" opacity="0">'
            f'<animate attributeName="x" from="{PAD}" to="{CANVAS_W - PAD}" begin="{delay:.3f}s" '
            f'dur="{ROW_DUR:.2f}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0.85" begin="{delay:.3f}s"/>'
            f'<set attributeName="opacity" to="0" begin="{delay+ROW_DUR:.3f}s"/></rect>'
        )

    y += CELL_H
    anim_i += 1

final_delay = anim_i * STAGGER
parts.append(
    f'<text xml:space="preserve" x="{PAD}" y="{y + CELL_H * 0.72:.1f}" font-size="{FONT_SIZE}">'
    f'<tspan fill="{USER}">nishanthcr7777</tspan><tspan fill="{MAIN}">@</tspan>'
    f'<tspan fill="{HOST}">github</tspan><tspan fill="{MAIN}">:~$ </tspan></text>'
)
parts.append(
    f'<rect x="{PAD + 168}" y="{y+3}" width="8" height="{CELL_H-6}" fill="{CURSOR}">'
    f'<set attributeName="opacity" to="0" begin="0s"/>'
    f'<set attributeName="opacity" to="1" begin="{final_delay:.3f}s"/>'
    f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
    f'dur="1s" repeatCount="indefinite" begin="{final_delay:.3f}s"/></rect>'
)

parts.append("</svg>")

svg_data = "".join(parts)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg_data)

print(f"wrote {OUT} {len(svg_data)} bytes; {CANVAS_W} x {CANVAS_H}")
