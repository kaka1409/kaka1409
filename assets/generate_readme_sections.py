from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import io
import html

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets" / "sections"
ASSETS.mkdir(parents=True, exist_ok=True)

BG = "#080d17"
PANEL = "#0b1422"
CYAN = "#66e4ef"
PINK = "#d98be8"
TEXT = "#dce7f0"
MUTED = "#8194a8"
GREEN = "#8bd9b1"
LINE = "#20374a"

def esc(value):
    return html.escape(str(value), quote=False)

def text(x, y, value, cls="body", anchor=None, extra=""):
    align = f' text-anchor="{anchor}"' if anchor else ""
    return f'<text x="{x}" y="{y}" class="{cls}"{align} {extra}>{esc(value)}</text>'

def ascii_lines(x, y, lines, cls="art", line_height=17, anchor=None, extra=""):
    # Every illustration is literal monospace character art, not vector-drawn artwork.
    out = []
    for index, value in enumerate(lines):
        line_extra = f'style="--delay:{index * 0.08:.2f}s;--steps:{max(len(value), 1)}"'
        out.append(text(x, y + index * line_height, value, f"{cls} typing", anchor, line_extra))
    return "".join(out)

def typed(x, y, value, cls="body", delay=0.0, anchor=None):
    align = f' text-anchor="{anchor}"' if anchor else ""
    return (f'<text x="{x}" y="{y}" class="{cls} typing" style="--delay:{delay}s;--steps:{max(len(value), 1)}"'
            f'{align}>{esc(value)}</text>')

def svg_doc(title, code, height, body, subtitle):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" viewBox="0 0 900 {height}" role="img" aria-labelledby="title desc">
<title id="title">{esc(title)}</title><desc id="desc">{esc(subtitle)}</desc>
<defs>
<style>
text {{ font-family: Consolas, "Liberation Mono", monospace; white-space: pre; fill:#dce7f0; }}
.bg {{ fill:{BG}; }} .panel {{ fill:{PANEL}; stroke:{LINE}; stroke-width:1.2; }}
.cyan {{ fill:{CYAN}; }} .pink {{ fill:{PINK}; }} .text {{ fill:{TEXT}; }}
.muted {{ fill:{MUTED}; }} .green {{ fill:{GREEN}; }}
.small {{ font-size:13px; letter-spacing:1.1px; }}
.body {{ font-size:16px; }} .heading {{ font-size:20px; font-weight:700; letter-spacing:1.2px; }}
.art {{ font-size:14px; letter-spacing:0; }}
.art-large {{ font-size:19px; letter-spacing:0; font-weight:700; }} .logo-art {{ font-size:13px; letter-spacing:0; font-weight:700; }}
.glow {{ animation: glow 4.16s ease-in-out infinite; }}
.cursor {{ animation: blink 1.04s steps(2,end) infinite; }}
.scan {{ animation: scan 4.16s ease-in-out infinite; }}
.typing {{ }}
.type-soft {{ animation: type-soft 4.16s steps(40,end) var(--delay,0s) infinite; }}
@keyframes glow {{ 0%,100% {{ opacity:.48; }} 50% {{ opacity:1; }} }}
@keyframes blink {{ 0%,48% {{ opacity:1; }} 49%,100% {{ opacity:0; }} }}
@keyframes scan {{ 0%,100% {{ transform:translateX(0); opacity:.12; }} 50% {{ transform:translateX(620px); opacity:.65; }} }}

@keyframes type-soft {{ 0%,8% {{ opacity:0; }} 28%,82% {{ opacity:1; }} 96%,100% {{ opacity:0; }} }}
</style>
</defs>
<rect class="bg" width="900" height="{height}"/>
<rect x="12" y="12" width="876" height="{height-24}" rx="5" class="panel"/>
<path d="M12 54 H888" stroke="{LINE}" stroke-width="1"/>
<text x="32" y="39" class="cyan small">KK1409 / {esc(code)}</text>
<text x="868" y="39" text-anchor="end" class="muted small">[{esc(subtitle)}]</text>
<text x="32" y="57" class="cyan small glow">+--------------------------------------------------------------------------+</text>
<text x="32" y="{height-28}" class="muted small">root@kk1409:~$ <tspan class="cyan cursor">_</tspan></text>
<text x="868" y="{height-28}" text-anchor="end" class="green small glow">[ ONLINE ]</text>
{body}
</svg>'''

# Dense 11x15 character-built glyphs. The logo uses only strokes such as
# /, \, -, _, | and #; no dot-based pixels or font scaling.
GLYPHS = {
"K": [
"||       ||", "||      /||", "||     / ||", "||    /  ||", "||   /   ||",
"||  /    ||", "|||||    ||", "||  \\    ||", "||   \\   ||", "||    \\  ||",
"||     \\ ||", "||      \\||", "||       ||", "||       ||", "||       ||"
],
"1": [
"   _____  ", "  /|||||  ", " / ||||   ", "   ||||   ", "   ||||   ",
"   ||||   ", "   ||||   ", "   ||||   ", "   ||||   ", "   ||||   ",
"   ||||   ", "   ||||   ", "   ||||   ", "   ||||   ", "___||||___"
],
"4": [
"||      ||", "||      ||", "||      ||", "||      ||", "||      ||",
"||      ||", "||######||", "        ||", "        ||", "        ||",
"        ||", "        ||", "        ||", "        ||", "        ||"
],
"0": [
"  _______  ", " /       \\ ", "||       ||", "||       ||", "||       ||",
"||       ||", "||       ||", "||       ||", "||       ||", "||       ||",
"||       ||", "||       ||", "||       ||", " \\       / ", "  -------  "
],
"9": [
"  _______  ", " /       \\ ", "||       ||", "||       ||", "||       ||",
"||       ||", " \\_______||", "         ||", "         ||", "         ||",
"         ||", "         ||", "         ||", "        // ", "  ------   "
]
}

def wordmark():
    rows = []
    for row in range(15):
        rows.append("  ".join(GLYPHS[ch][row].ljust(11) for ch in "KK1409"))
    return rows

sections = {}

# 00 / HERO: typographic identity plus several ASCII-art signals.
hero = ascii_lines(450, 96, wordmark(), "cyan logo-art glow", 16, "middle")
hero += typed(450, 470, "FULLSTACK DEVELOPER", "text heading", .25, "middle")
hero += typed(450, 498, "BUILDING SYSTEMS / LEARNING CONSTANTLY / SHIPPING WITH INTENT", "muted small", .65, "middle")
hero += ascii_lines(42, 112, [
"       .--------.", "      /  .--.    \\", "     |  ( .. )   |", "      \\  '--'   /", "       '--------'"
], "pink art", 16)
hero += ascii_lines(690, 112, [
"       .--------.", "      /  .--.    \\", "     |  ( .. )   |", "      \\  '--'   /", "       '--------'"
], "pink art", 16)
hero += ascii_lines(450, 382, [
"+---------------- SIGNAL TRACE ----------------+",
"  .---.     .---.     .---.     .---.",
"  |   '-----'   '-----'   '-----'   |",
"+-----------------------------------------------+"
], "muted art", 17, "middle")
hero += typed(450, 550, "[ SYSTEM READY ]  [ OPEN TO INTERNSHIP ]", "green small", 1.0, "middle")
sections["00-hero"] = ("KK1409 ASCII identity", "00 / INTRODUCTION", 610, hero, "IDENTITY NODE")

# 01 / PROFILE: identity rendered as a character-built node map.
profile = typed(42, 94, "01 / PROFILE RECORD", "pink small", .1)
profile += typed(42, 133, "PHAN HOANG QUOC KHANH", "heading", .35)
profile += typed(42, 164, "FULLSTACK DEVELOPER  /  HO CHI MINH CITY, VIETNAM", "text", .6)
profile += typed(42, 193, "B.Sc. SOFTWARE ENGINEERING  /  UNIVERSITY OF GREENWICH", "muted body", .85)
profile += ascii_lines(42, 238, [
"+----------------------+       +----------------------+",
"|      HUMAN            |------>|      BUILDER         |",
"|  curiosity / growth   |       |  frontend / backend  |",
"+----------------------+       +----------------------+",
"             |                            |",
"             +------------+---------------+",
"                          v",
"                 [ BUILD / LEARN / SHIP ]"
], "cyan art", 17)
profile += typed(42, 390, "I build end-to-end web applications with clear architecture and reliable user flows.", "text body", 1.15)
profile += typed(42, 416, "Working across interfaces, backend services, APIs, and relational data.", "muted body", 1.45)
sections["01-profile"] = ("Profile and background", "01 / SYSTEM IDENTITY", 460, profile, "IDENTITY RECORD")

# 02 / STACK: terminal matrix and ASCII circuit branches.
stack = typed(42, 94, "02 / TECHNOLOGY MATRIX", "pink small", .1)
stack += ascii_lines(42, 132, [
"+-- LANGUAGES -----------+  +-- FRONTEND -----------------------+",
"| JavaScript / TypeScript|  | React / Next.js / Tailwind CSS   |",
"+-----------------------+  +-----------------------------------+",
"+-- BACKEND -------------+  +-- DATA / QUEUES ------------------+",
"| Node.js / NestJS       |  | PostgreSQL / MySQL / Redis        |",
"+-----------------------+  | Bull Queue                        |",
"                           +-----------------------------------+",
"+-- TOOLCHAIN -------------------------------------------------+",
"| Git / Docker / Figma                                          |",
"+--------------------------------------------------------------+"
], "text art", 20)
stack += typed(42, 365, "CORE STACK < / > CONTINUOUSLY EXPANDING", "green small", 1.0)
stack += ascii_lines(650, 370, [
"       .----.",
"      /      \\",
"  ---+  <>    +---",
"      \\      /",
"       '----'"
], "pink art glow", 15)
sections["02-stack"] = ("Technology stack", "02 / TECHNOLOGY STACK", 470, stack, "TECH MATRIX")

# 03 / AI workflow: ASCII flowchart and sequenced terminal output.
workflow = typed(42, 94, "03 / AI-ASSISTED ENGINEERING", "pink small", .1)
workflow += ascii_lines(42, 133, [
"+----------------+       +----------------+",
"| 01 BRAINSTORM  |------>| 02 SPECIFY     |",
"| ideas / scope  |       | plans / design |",
"+----------------+       +----------------+",
"         |                         |",
"         v                         v",
"+----------------+       +----------------+",
"| 04 VERIFY      |<------| 03 DELEGATE    |",
"| tests / review |       | CLI agents     |",
"+----------------+       +----------------+"
], "cyan art", 20)
workflow += typed(510, 151, "> Explore product ideas and edge cases", "text body", .35)
workflow += typed(510, 190, "> Define architecture, contracts and tasks", "text body", .7)
workflow += typed(510, 229, "> Delegate scoped work to coding agents", "text body", 1.05)
workflow += typed(510, 268, "> Review diffs, tests and quality gates", "text body", 1.4)
workflow += typed(42, 380, "AI SUPPORTS THE PROCESS. ENGINEERING JUDGMENT OWNS THE RESULT.", "muted small", 1.7)
sections["03-ai-workflow"] = ("AI-assisted engineering workflow", "03 / ENGINEERING WORKFLOW", 430, workflow, "WORKFLOW PIPELINE")

# 04 / OBJECTIVE: ASCII launch console, not a project showcase.
objective = typed(42, 96, "04 / CURRENT OBJECTIVE", "pink small", .1)
objective += ascii_lines(42, 153, [
"                 .",
"                / \\",
"               /___\\",
"              |     |",
"              | KK  |",
"              |1409 |",
"             /|_____|\\",
"            /_/     \\_\\",
"               /   \\",
"              /_____\\",
"             /_______\\"
], "cyan art glow", 18)
objective += typed(365, 174, "OPEN TO FULLSTACK DEVELOPER INTERNSHIP", "heading", .4)
objective += typed(365, 215, "Contribute to a professional engineering team.", "text body", .8)
objective += typed(365, 244, "Learn from production workflows and ship", "text body", 1.1)
objective += typed(365, 270, "software that solves real problems.", "text body", 1.35)
objective += typed(365, 322, "[ AVAILABLE FOR INTERNSHIP OPPORTUNITIES ]", "green small", 1.7)
objective += ascii_lines(365, 366, [
"+-----------------------------------------------+",
"| STATUS: READY TO BUILD / LEARN / CONTRIBUTE   |",
"+-----------------------------------------------+"
], "muted art", 18)
sections["04-objective"] = ("Current objective", "04 / MISSION STATUS", 450, objective, "MISSION STATUS")

# 05 / CONTACT: ASCII signal transmitter and connection status.
contact = typed(42, 96, "05 / ESTABLISH CONNECTION", "pink small", .1)
contact += ascii_lines(42, 148, [
"       .-----------.",
"      /  .-------.  \\",
"     |  /  _____  \\  |",
"     | |  /     \\  | |",
"     | | |  LINK | | |",
"     | |  \\_____/  | |",
"      \\ '---------' /",
"       '-----------'",
"          |  |",
"       ___|  |___",
"      /__________\\"
], "cyan art", 17)
contact += typed(390, 165, "GITHUB", "cyan small", .35)
contact += typed(390, 194, "github.com/kaka1409", "text body", .6)
contact += typed(390, 247, "EMAIL", "cyan small", .95)
contact += typed(390, 276, "1aidodacbiet@gmail.com", "text body", 1.2)
contact += ascii_lines(390, 335, [
"+---------------------------------------+",
"| [ BUILD ]   [ LEARN ]   [ SHIP ]       |",
"+---------------------------------------+"
], "green art", 18)
contact += typed(868, 402, "END OF TRANSMISSION", "muted small", 1.6, "end")
sections["05-contact"] = ("Contact information", "05 / CONNECTION", 450, contact, "CONTACT CHANNEL")

# Save SVG sources.
for slug, (title, code, height, body, subtitle) in sections.items():
    (ASSETS / f"{slug}.svg").write_text(
        svg_doc(title, code, height, body, subtitle), encoding="utf-8"
    )

# Render one-shot typewriter GIFs. Every section is typed in DOM order by one
# shared cursor; there is no per-line reveal and no replay after completion.
edge = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
if not edge.exists():
    edge = None

TYPEWRITER_JS = r"""
() => {
  const nodes = [...document.querySelectorAll('text.typing')];
  const entries = nodes.map(node => {
    const value = node.textContent || '';
    const x = parseFloat(node.getAttribute('x') || '0');
    const y = parseFloat(node.getAttribute('y') || '0');
    const anchor = getComputedStyle(node).textAnchor;
    const size = parseFloat(getComputedStyle(node).fontSize) || 16;
    const fullWidth = node.getComputedTextLength();
    const startX = anchor === 'middle' ? x - fullWidth / 2
                 : anchor === 'end' ? x - fullWidth : x;
    node.setAttribute('text-anchor', 'start');
    node.setAttribute('x', startX);
    return {node, value, x:startX, y, size};
  });
  const svg = document.documentElement;
  const cursor = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
  cursor.setAttribute('id', 'global-typewriter-cursor');
  cursor.setAttribute('width', '2.5');
  cursor.setAttribute('height', '16');
  cursor.setAttribute('rx', '0.5');
  cursor.setAttribute('fill', '#66e4ef');
  cursor.setAttribute('pointer-events', 'none');
  svg.appendChild(cursor);
  let total = 0;
  for (const e of entries) total += e.value.length;
  window.__typewriter = {entries, cursor, total};
}
"""

FRAME_JS = r"""
([index, visible]) => {
  const state = window.__typewriter;
  let remaining = index;
  let active = null;
  for (const e of state.entries) {
    const count = Math.min(e.value.length, Math.max(0, remaining));
    e.node.textContent = e.value.slice(0, count);
    remaining -= count;
    if (!active && count < e.value.length) active = {e, count};
  }
  if (!active) {
    const e = state.entries[state.entries.length - 1];
    if (e) active = {e, count:e.value.length};
  }
  if (!active) return;
  const {e, count} = active;
  const prefixWidth = e.node.getComputedTextLength();
  state.cursor.setAttribute('x', e.x + prefixWidth + 1);
  state.cursor.setAttribute('y', e.y - e.size * 0.84);
  state.cursor.setAttribute('height', Math.max(10, e.size * 1.08));
  state.cursor.setAttribute('visibility', visible ? 'visible' : 'hidden');
}
"""

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(
        headless=True, executable_path=str(edge) if edge else None
    )
    page = browser.new_page(viewport={"width": 900, "height": 550}, device_scale_factor=1)
    for slug, (_, _, height, _, _) in sections.items():
        source = ASSETS / f"{slug}.svg"
        page.set_viewport_size({"width": 900, "height": height})
        page.goto(source.as_uri(), wait_until="load")
        page.evaluate(TYPEWRITER_JS)
        total = page.evaluate("window.__typewriter.total")
        # Reveal two characters per 50ms frame (~40 chars/second).
        frames = []
        for index in range(0, total + 1, 2):
            page.evaluate(FRAME_JS, [index, (index // 2 // 5) % 2 == 0])
            shot = page.screenshot(type="png", animations="disabled")
            frames.append(Image.open(io.BytesIO(shot)).convert(
                "P", palette=Image.Palette.ADAPTIVE, colors=128
            ))
        # Leave a short final hold with the single cursor at the end.
        final_blink_frames = (
            [True] * 5 + [False] * 5 +
            [True] * 5 + [False] * 5 +
            [True] * 5 + [False] * 5 +
            [True] * 5
        )
        for blink in final_blink_frames:
            page.evaluate(FRAME_JS, [total, blink])
            shot = page.screenshot(type="png", animations="disabled")
            frames.append(Image.open(io.BytesIO(shot)).convert(
                "P", palette=Image.Palette.ADAPTIVE, colors=128
            ))
        output = ASSETS / f"{slug}.gif"
        frames[0].save(
            output, save_all=True, append_images=frames[1:],
            duration=50, optimize=True, disposal=2
        )
        print(f"{slug}: {total} characters | {len(frames)} frames | {output.stat().st_size:,} B")
    browser.close()

print(f"Generated {len(sections)} one-shot typewriter GIF sections.")
