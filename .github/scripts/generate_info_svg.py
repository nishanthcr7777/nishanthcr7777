import os
import sys
import html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "info.svg")

STATIC = bool(os.environ.get("STATIC"))

# Styling
BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
TEXT_MAIN = "#c9d1d9"
COLOR_KEY = "#79c0ff"
COLOR_VAL = "#c9d1d9"
COLOR_USER = "#ff7b72"
COLOR_HOST = "#79c0ff"
CURSOR = "#c9d1d9"

# Layout
CANVAS_W = 450
CANVAS_H = 340
TITLEBAR_H = 30
PAD = 20
CELL_H = 22
FONT_SIZE = 14

LINES = [
    [("nishanthcr7777", COLOR_USER), ("@", TEXT_MAIN), ("github", COLOR_HOST)],
    [("----------------", TEXT_MAIN)],
    [("Role       ", COLOR_KEY), ("*Backend Engineer & AI-Native Systems", COLOR_VAL)],
    [("Education  ", COLOR_KEY), ("*B.Tech IT, Chennai Institute of Technology", COLOR_VAL)],
    [("Exp        ", COLOR_KEY), ("*SDE Intern @ TVS Automobile Solutions", COLOR_VAL)],
    [("           ", COLOR_KEY), ("*Open-Source Contributor @ BrainGlobe", COLOR_VAL)],
    [("Awards     ", COLOR_KEY), ("*BCH-1 Hackcelerator Overall Winner", COLOR_VAL)],
    [("           ", COLOR_KEY), ("*Web3Conf'25 First Runner-Up", COLOR_VAL)],
    [("           ", COLOR_KEY), ("*LeetCode Contest Rating 1600+", COLOR_VAL)],
]

# Reveal timing
ROW_DUR = 0.4
STAGGER = 0.4

parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, '
    f'Menlo, Consolas, monospace">'
)
parts.append('<defs>'
             f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
             f'</linearGradient></defs>')

parts.append(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#bg)"/>')
parts.append(f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" '
             f'fill="none" stroke="{FRAME}" stroke-width="1"/>')

parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" '
             f'text-anchor="middle">nishanthcr7777@github: ~$ ./info.sh</text>')

start_y = TITLEBAR_H + PAD

for i, line_segments in enumerate(LINES):
    y = start_y + i * CELL_H
    delay = i * STAGGER

    text_content = ""
    for text, color in line_segments:
        safe_text = html.escape(text)
        text_content += f'<tspan fill="{color}">{safe_text}</tspan>'

    text_element = f'<text xml:space="preserve" x="{PAD}" y="{y + CELL_H * 0.7:.1f}" font-size="{FONT_SIZE}">{text_content}</text>'

    if STATIC:
        parts.append(text_element)
        continue

    parts.append(
        f'<clipPath id="l{i}"><rect x="{PAD}" y="{y}" height="{CELL_H}" width="0">'
        f'<animate attributeName="width" from="0" to="{CANVAS_W - PAD*2}" begin="{delay:.3f}s" '
        f'dur="{ROW_DUR:.2f}s" fill="freeze"/></rect></clipPath>'
    )
    parts.append(f'<g clip-path="url(#l{i})">{text_element}</g>')
    parts.append(
        f'<rect y="{y+2}" width="8" height="{CELL_H-4}" fill="{CURSOR}" opacity="0">'
        f'<animate attributeName="x" from="{PAD}" to="{CANVAS_W - PAD}" begin="{delay:.3f}s" '
        f'dur="{ROW_DUR:.2f}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0.85" begin="{delay:.3f}s"/>'
        f'<set attributeName="opacity" to="0" begin="{delay+ROW_DUR:.3f}s"/></rect>'
    )

# Prompt line at the end
end_idx = len(LINES)
final_y = start_y + end_idx * CELL_H
final_delay = end_idx * STAGGER

parts.append(f'<text xml:space="preserve" x="{PAD}" y="{final_y + CELL_H * 0.7:.1f}" font-size="{FONT_SIZE}">'
             f'<tspan fill="{COLOR_USER}">nishanthcr7777</tspan><tspan fill="{TEXT_MAIN}">@</tspan><tspan fill="{COLOR_HOST}">github</tspan>'
             f'<tspan fill="{TEXT_MAIN}">:~$ </tspan></text>')
parts.append(f'<rect x="{PAD + 160}" y="{final_y+2}" width="8" height="{CELL_H-4}" fill="{CURSOR}">'
             f'<set attributeName="opacity" to="0" begin="0s"/>'
             f'<set attributeName="opacity" to="1" begin="{final_delay:.3f}s"/>'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
             f'dur="1s" repeatCount="indefinite" begin="{final_delay:.3f}s"/></rect>')

parts.append("</svg>")

svg_data = "".join(parts)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    f.write(svg_data)

print(f"wrote {OUT} {len(svg_data)} bytes; {CANVAS_W} x {CANVAS_H}")
