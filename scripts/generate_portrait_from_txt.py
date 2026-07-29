"""
Build the animated terminal-style portrait.svg from assets/ascii-art.txt.
Prefer this over photo conversion when the txt file exists.
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "ascii-art.txt")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "assets", "portrait.svg")

CELL_W = 7
CELL_H = 12
PAD = 20
TITLEBAR_H = 30
STATUS_H = 30

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
INK = "#c9d1d9"
CURSOR = "#c9d1d9"

ROW_DUR = 0.08
STAGGER = 0.08
STATIC = bool(os.environ.get("STATIC"))


def load_rows(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read().splitlines()

    # Drop trailing blank lines; keep leading ones for framing
    while raw and not raw[-1].rstrip():
        raw.pop()
    # Drop leading blank lines beyond 1 spacer
    while len(raw) > 1 and not raw[0].rstrip() and not raw[1].rstrip():
        raw.pop(0)

    width = max((len(line.rstrip("\n")) for line in raw), default=0)
    # Keep trailing spaces for alignment up to max width
    return [line.ljust(width)[:width] for line in raw]


rows_txt = load_rows(SRC)
COLS = max((len(r) for r in rows_txt), default=80)
ROWS = len(rows_txt)

ART_W = COLS * CELL_W
ART_H = ROWS * CELL_H
CANVAS_W = ART_W + PAD * 2
CANVAS_H = TITLEBAR_H + ART_H + STATUS_H + PAD

art_top = TITLEBAR_H + PAD * 0.35

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
    f'text-anchor="middle">nishanthcr7777@github: ~$ ./portrait.sh</text>'
)

font_size = CELL_H * 0.86
for ry, line in enumerate(rows_txt):
    y = art_top + ry * CELL_H + CELL_H * 0.74
    row_y = art_top + ry * CELL_H
    delay = ry * STAGGER
    safe = html.escape(line)
    text = (
        f'<text xml:space="preserve" x="{PAD}" y="{y:.1f}" fill="{INK}" '
        f'font-size="{font_size:.1f}" textLength="{ART_W}" lengthAdjust="spacing">{safe}</text>'
    )

    if STATIC:
        parts.append(text)
        continue

    parts.append(
        f'<clipPath id="r{ry}"><rect x="{PAD}" y="{row_y:.1f}" height="{CELL_H}" width="0">'
        f'<animate attributeName="width" from="0" to="{ART_W}" begin="{delay:.3f}s" '
        f'dur="{ROW_DUR:.2f}s" fill="freeze"/></rect></clipPath>'
    )
    parts.append(f'<g clip-path="url(#r{ry})">{text}</g>')
    parts.append(
        f'<rect y="{row_y+1:.1f}" width="{CELL_W}" height="{CELL_H-2}" fill="{CURSOR}" opacity="0">'
        f'<animate attributeName="x" from="{PAD}" to="{PAD+ART_W}" begin="{delay:.3f}s" '
        f'dur="{ROW_DUR:.2f}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0.85" begin="{delay:.3f}s"/>'
        f'<set attributeName="opacity" to="0" begin="{delay+ROW_DUR:.3f}s"/></rect>'
    )

status_line_y = TITLEBAR_H + ART_H + PAD * 0.35
status_y = status_line_y + 19
parts.append(
    f'<line x1="0" y1="{status_line_y:.1f}" x2="{CANVAS_W}" y2="{status_line_y:.1f}" stroke="{FRAME}"/>'
)
parts.append(
    f'<text x="{PAD}" y="{status_y:.1f}" fill="{TITLE_TEXT}" font-size="13">'
    f'nishanthcr7777@github:~$ whoami <tspan fill="{INK}">Nishanth B</tspan></text>'
)
parts.append(
    f'<rect x="{PAD+250}" y="{status_y-12:.1f}" width="8" height="14" fill="{INK}">'
    f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
    f'dur="1s" repeatCount="indefinite"/></rect>'
)

parts.append("</svg>")
svg = "".join(parts)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"wrote {OUT} {len(svg)} bytes; {CANVAS_W}x{CANVAS_H}; {COLS}x{ROWS} chars")
