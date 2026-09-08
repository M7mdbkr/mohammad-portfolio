from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path('/Users/engmohammed/Desktop/mohammad-portfolio/figma-report')
W, H = 1600, 1000
BG = '#F4F0E8'
CARD = '#FBFAF6'
INK = '#17252B'
MUTED = '#68767A'
LINE = '#C9C4B8'
CORAL = '#B75034'
TEAL = '#176D78'
GOLD = '#B68A3A'
DARK = '#17252B'
LIGHT = '#F7F3EA'
SERIF = 'Georgia, Times New Roman, serif'
SANS = 'Arial, Helvetica, sans-serif'
MONO = 'Courier New, monospace'


def esc(value):
    return escape(str(value), {'"': '&quot;'})


def text(x, y, value, size=18, fill=INK, family=SANS, weight='400', anchor='start', letter=0, opacity=1):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-family="{family}" font-size="{size}px" font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{letter}px" opacity="{opacity}">{esc(value)}</text>'


def lines(x, y, values, size=18, leading=28, fill=INK, family=SANS, weight='400', letter=0):
    return ''.join(text(x, y + i * leading, value, size, fill, family, weight, 'start', letter) for i, value in enumerate(values))


def rect(x, y, w, h, fill=CARD, stroke=LINE, radius=0, sw=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def rule(x1, y1, x2, y2, stroke=LINE, sw=1):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"/>'


def pill(x, y, label, fill='#E6DED1', color=INK, stroke='none', w=None):
    width = w or (len(label) * 8 + 26)
    return rect(x, y, width, 30, fill, stroke, 15) + text(x + width / 2, y + 20, label, 11, color, MONO, '700', 'middle', .5)


def header(page, section, number, dark=False):
    fg = LIGHT if dark else INK
    muted = '#AEBDBD' if dark else MUTED
    line = '#496064' if dark else LINE
    return text(70, 60, 'MJB / PORTFOLIO REPORT', 12, fg, MONO, '700', letter=1.5) + text(1530, 60, f'{number}  ·  {section.upper()}', 12, muted, MONO, '700', 'end', 1.2) + rule(70, 82, 1530, 82, line)


def footer(page, label='MOHAMMAD J. BAKR  ·  2026', dark=False):
    fg = '#AEBDBD' if dark else MUTED
    line = '#496064' if dark else LINE
    return rule(70, 930, 1530, 930, line) + text(70, 962, label, 11, fg, MONO, '700', letter=.8) + text(1530, 962, f'{page:02d} / 09', 11, fg, MONO, '700', 'end', .8)


def shell(content, dark=False):
    bg = DARK if dark else BG
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="{bg}"/>{content}</svg>'''


def save(name, content, dark=False):
    (OUT / name).write_text(shell(content, dark), encoding='utf-8')


def page_01():
    c = header(1, 'cover', '01')
    c += text(70, 154, 'COMPUTER ENGINEERING  /  AI SYSTEMS  /  PRODUCT SOFTWARE', 13, CORAL, MONO, '700', letter=1.2)
    c += text(70, 300, 'Computer engineering,', 82, INK, SERIF, '400', letter=-3)
    c += text(70, 382, 'built systems.', 82, CORAL, SERIF, '400', letter=-3)
    c += rect(1040, 155, 3, 350, CORAL, CORAL)
    c += lines(1080, 190, ['Mohammad J. Bakr builds', 'practical software where', 'automation, interfaces,', 'and safety have to work', 'together.'], 25, 37, INK, SERIF)
    c += pill(1080, 430, 'SAUDI ARABIA', '#E7DED1', CORAL)
    c += pill(1080, 475, 'OPEN TO ENGINEERING ROLES', '#DCE9E8', TEAL)
    c += rect(70, 580, 1460, 1, INK, INK)
    c += text(70, 625, 'A portfolio of local-first systems, Arabic-first product interfaces, automation pipelines, and motion experiments.', 21, MUTED, SANS, '400')
    tags = ['PYTHON', 'TYPESCRIPT', 'REACT', 'SQLITE', 'AUTOMATION', 'ARABIC UI']
    x = 70
    for tag in tags:
        c += pill(x, 705, tag, CARD, TEAL, LINE)
        x += len(tag) * 8 + 46
    c += text(70, 850, 'mohammadbakrwork@gmail.com', 15, CORAL, MONO, '700')
    c += text(1530, 850, 'GITHUB.COM/M7MDBKR', 15, TEAL, MONO, '700', 'end')
    c += footer(1)
    save('01-cover.svg', c)


def page_02():
    c = header(2, 'throughline', '02')
    c += text(70, 160, 'THE THROUGHLINE', 13, CORAL, MONO, '700', letter=1.4)
    c += text(70, 228, 'Systems that stay', 62, INK, SERIF, '400', letter=-2)
    c += text(70, 288, 'understandable.', 62, CORAL, SERIF, '400', letter=-2)
    c += lines(70, 355, ['The projects vary in surface area — an operating system,', 'a POS, a news bot, a route planner, a video pipeline —', 'but the engineering instinct stays consistent.'], 20, 31, MUTED, SANS)
    principles = [
        ('01', 'MAKE STATE VISIBLE', 'Dashboards, timelines, logs, and clear empty states.'),
        ('02', 'KEEP ACTIONS EXPLICIT', 'Approval gates before email, publishing, or deployment.'),
        ('03', 'DESIGN FOR THE REAL USER', 'Arabic-first flows, local constraints, and practical defaults.'),
        ('04', 'LEAVE A TRAIL', 'Tests, manifests, source records, and honest limitations.'),
    ]
    y = 500
    for num, title, desc in principles:
        c += rule(70, y - 18, 805, y - 18, LINE)
        c += text(70, y + 15, num, 13, CORAL, MONO, '700', letter=1)
        c += text(125, y + 15, title, 16, INK, MONO, '700', letter=.8)
        c += text(125, y + 45, desc, 15, MUTED, SANS)
        y += 92
    c += rect(930, 155, 600, 660, INK, INK, 2)
    c += text(980, 210, 'BUILD MAP', 12, '#D99D8B', MONO, '700', letter=1.4)
    c += text(980, 275, 'FROM IDEA', 12, '#AEBDBD', MONO, '700', letter=1)
    c += text(980, 315, '→', 34, CORAL, SERIF)
    c += text(1030, 313, 'brief / problem / constraint', 19, LIGHT, SERIF)
    c += text(980, 390, 'TO SYSTEM', 12, '#AEBDBD', MONO, '700', letter=1)
    c += text(980, 430, '→', 34, CORAL, SERIF)
    c += text(1030, 428, 'data / policy / interface', 19, LIGHT, SERIF)
    c += text(980, 505, 'TO PROOF', 12, '#AEBDBD', MONO, '700', letter=1)
    c += text(980, 545, '→', 34, CORAL, SERIF)
    c += text(1030, 543, 'tests / smoke check / review', 19, LIGHT, SERIF)
    c += rule(980, 620, 1480, 620, '#496064')
    c += lines(980, 680, ['No cloud dependency by default.', 'No silent external side effects.', 'No claims without a visible trail.'], 22, 39, LIGHT, SERIF)
    c += footer(2)
    save('02-throughline.svg', c)


def page_03():
    c = header(3, 'featured case', '03', True)
    c += text(70, 155, '01 / FEATURED CASE', 13, '#D99D8B', MONO, '700', letter=1.4)
    c += text(70, 225, 'AgenticOS', 78, LIGHT, SERIF, '400', letter=-2)
    c += text(70, 270, 'A local-first personal agent operating system.', 22, '#AEBDBD', SANS)
    c += lines(70, 360, ['Four specialist workspaces, a human-in-the-loop', 'approval layer, Telegram and n8n hooks, local context,', 'schedules, page-agent interactions, and a SHA-256 audit chain.'], 19, 30, LIGHT, SANS)
    c += text(70, 495, 'THE ENGINEERING STORY', 12, '#D99D8B', MONO, '700', letter=1)
    bullets = ['State is stored locally in SQLite.', 'External actions become reviewable cards.', 'Providers are replaceable instead of permanent.', 'Runtime data stays outside the public snapshot.']
    for i, b in enumerate(bullets):
        yy = 535 + i * 39
        c += text(70, yy, '—', 22, CORAL, SERIF)
        c += text(102, yy, b, 16, '#DCE7E3', SANS)
    c += rect(850, 145, 680, 600, '#20353A', '#496064', 2)
    c += text(900, 195, 'ARCHITECTURE', 12, '#D99D8B', MONO, '700', letter=1.2)
    boxes = [('BROWSER', 'HTML / CSS / JS'), ('OPERATIONS STORE', 'Python + SQLite'), ('APPROVAL LAYER', 'exact scope + audit'), ('OPTIONAL CONNECTORS', 'Telegram / n8n / Ollama')]
    yy = 240
    for i, (a, b) in enumerate(boxes):
        c += rect(900, yy, 580, 75, '#17252B', '#557277', 8)
        c += text(925, yy + 30, a, 12, '#D99D8B', MONO, '700', letter=1)
        c += text(925, yy + 57, b, 16, LIGHT, SANS)
        if i < len(boxes) - 1:
            c += text(1188, yy + 106, '↓', 25, CORAL, SERIF, '400', 'middle')
        yy += 112
    c += pill(70, 720, '16 TESTS PASS', '#26464A', '#D3E7E3', '#557277')
    c += pill(235, 720, 'PYTHON + JS SYNTAX', '#26464A', '#D3E7E3', '#557277')
    c += pill(465, 720, 'LOOPBACK SMOKE TEST', '#26464A', '#D3E7E3', '#557277')
    c += text(70, 820, 'github.com/M7mdbkr/agenticos', 18, '#E8B4A4', MONO, '700')
    c += text(1530, 820, 'PUBLIC SNAPSHOT  ·  RUNTIME DATA EXCLUDED', 12, '#AEBDBD', MONO, '700', 'end', 1)
    c += footer(3, 'AGENTICOS  ·  LOCAL-FIRST  ·  APPROVAL-GATED  ·  AUDITABLE', True)
    save('03-agenticos.svg', c, True)


def page_04():
    c = header(4, 'product case', '04')
    c += text(70, 155, '02 / PRODUCT CASE', 13, CORAL, MONO, '700', letter=1.4)
    c += text(70, 225, 'Rizq POS', 78, INK, SERIF, '400', letter=-2)
    c += text(70, 270, 'Arabic-first point of sale for cafés and restaurants.', 22, MUTED, SANS)
    c += rect(70, 345, 690, 430, INK, INK, 12)
    c += text(105, 390, 'RIZQ / الكاشير', 15, '#E6B7A8', MONO, '700', letter=1)
    c += rect(105, 425, 185, 300, '#22343A', '#526C70', 8)
    c += text(130, 460, 'OWNER', 11, '#AEBDBD', MONO, '700', letter=1)
    c += text(130, 510, 'Inventory', 16, LIGHT, SANS)
    c += text(130, 550, 'Orders', 16, LIGHT, SANS)
    c += text(130, 590, 'Discounts', 16, LIGHT, SANS)
    c += text(130, 630, 'Ledger', 16, LIGHT, SANS)
    c += rect(315, 425, 410, 300, '#F7F3EA', '#F7F3EA', 8)
    c += text(345, 462, 'طلب جديد', 18, INK, SANS, '700')
    c += text(345, 500, 'قهوة عربية', 16, INK, SANS)
    c += text(640, 500, '18.00 ر.س', 16, CORAL, MONO, '700', 'end')
    c += rule(345, 520, 695, 520, '#D2CCC0')
    c += text(345, 565, 'ضريبة القيمة المضافة', 15, MUTED, SANS)
    c += text(640, 565, '15%', 15, TEAL, MONO, '700', 'end')
    c += rule(345, 585, 695, 585, '#D2CCC0')
    c += text(345, 635, 'الإجمالي', 20, INK, SANS, '700')
    c += text(640, 635, '20.70 ر.س', 20, CORAL, MONO, '700', 'end')
    c += rect(345, 665, 350, 38, CORAL, CORAL, 19)
    c += text(520, 690, 'إتمام الطلب', 13, '#FFF8F0', SANS, '700', 'middle')
    c += text(850, 355, 'THE PRODUCT STORY', 12, CORAL, MONO, '700', letter=1.2)
    c += lines(850, 410, ['A real operational surface,', 'not just a dashboard mockup.'], 32, 38, INK, SERIF)
    c += lines(850, 515, ['Separate cashier and owner flows.', 'Browser-local SQLite/WASM storage.', 'Receipts, CSV export, inventory, VAT.', 'RTL layout and Arabic typography.'], 17, 34, MUTED, SANS)
    c += rect(850, 680, 680, 95, '#F6E6DF', '#D5A08F', 10)
    c += text(880, 715, 'HONEST READINESS NOTE', 11, CORAL, MONO, '700', letter=1)
    c += text(880, 750, 'Build passes; security hardening is required before real customer data.', 15, INK, SANS)
    c += pill(70, 825, 'REACT', CARD, TEAL, LINE)
    c += pill(155, 825, 'TYPESCRIPT', CARD, TEAL, LINE)
    c += pill(280, 825, 'VITE', CARD, TEAL, LINE)
    c += pill(350, 825, 'SQL.JS', CARD, TEAL, LINE)
    c += text(1530, 850, 'github.com/M7mdbkr/rizq-pos', 16, CORAL, MONO, '700', 'end')
    c += footer(4, 'RIZQ POS  ·  RTL  ·  PRODUCT THINKING  ·  DEMO-FIRST', False)
    save('04-rizq-pos.svg', c)


def page_05():
    c = header(5, 'automation + data', '05')
    c += text(70, 155, '03 / AUTOMATION + DATA', 13, CORAL, MONO, '700', letter=1.4)
    c += text(70, 225, 'Pipelines that move', 60, INK, SERIF, '400', letter=-2)
    c += text(70, 283, 'from signal to useful output.', 60, CORAL, SERIF, '400', letter=-2)
    c += rect(70, 355, 700, 435, CARD, LINE, 12)
    c += text(105, 405, 'ARABIC NEWS BOT', 13, TEAL, MONO, '700', letter=1.2)
    c += text(105, 450, 'RSS → Arabic → Telegram', 30, INK, SERIF)
    c += lines(105, 515, ['Cars and technology feeds become', 'deduplicated stories, Arabic headlines,', 'owner-only commands, and weekly', 'reports plus ready-to-edit video scripts.'], 17, 29, MUTED, SANS)
    steps = [('01', 'FETCH', 'RSS / Atom'), ('02', 'NORMALIZE', 'clean + translate'), ('03', 'STORE', 'SQLite dedup'), ('04', 'PUBLISH', 'Telegram gate')]
    x = 105
    for n, a, b in steps:
        c += rect(x, 665, 145, 70, '#E6F0EF', '#A5C8C7', 8)
        c += text(x + 15, 690, n, 11, CORAL, MONO, '700')
        c += text(x + 15, 712, a, 12, INK, MONO, '700')
        c += text(x + 15, 729, b, 10, MUTED, SANS)
        x += 160
    c += rect(830, 355, 700, 435, INK, INK, 12)
    c += text(865, 405, 'CRYPTO SIGNAL ANALYZER', 13, '#D99D8B', MONO, '700', letter=1.2)
    c += text(865, 450, 'Data, with the caveat attached.', 30, LIGHT, SERIF)
    c += lines(865, 515, ['CoinGecko market data becomes', 'explainable indicators: annualized', 'volatility, drawdown, market-cap rank,', 'and recent momentum.'], 17, 29, '#C7D2D1', SANS)
    c += rect(865, 665, 290, 70, '#20383D', '#557277', 8)
    c += text(890, 695, 'RISK', 11, '#D99D8B', MONO, '700')
    c += text(890, 720, 'volatility + drawdown + rank', 13, LIGHT, SANS)
    c += rect(1170, 665, 320, 70, '#20383D', '#557277', 8)
    c += text(1195, 695, 'MOMENTUM', 11, '#D99D8B', MONO, '700')
    c += text(1195, 720, '7d + 30d performance', 13, LIGHT, SANS)
    c += text(70, 850, 'The point is not “AI magic.” It is a chain a teammate can inspect, run, and improve.', 19, MUTED, SERIF)
    c += text(1530, 850, 'PYTHON  ·  RSS  ·  SQLITE  ·  TELEGRAM  ·  HTTP APIs', 12, TEAL, MONO, '700', 'end', 1)
    c += footer(5, 'ARABIC NEWS BOT  ·  CRYPTO SIGNAL ANALYZER  ·  EXPLAINABLE PIPELINES', False)
    save('05-pipelines.svg', c)


def page_06():
    c = header(6, 'interfaces', '06')
    c += text(70, 155, '04 / INTERFACES', 13, CORAL, MONO, '700', letter=1.4)
    c += text(70, 225, 'Make the next action', 60, INK, SERIF, '400', letter=-2)
    c += text(70, 283, 'obvious.', 60, CORAL, SERIF, '400', letter=-2)
    cards = [
        ('OPERATIONS EXPLORER', 'AOS CORE', 'Interactive architecture map for agents, task routing, exact-scope approvals, audit events, and a loopback-only API.', TEAL, ['Python', 'SQLite', 'Policy']),
        ('MALHAM LINE', 'ROUTE PLANNING', 'Editorial route-planning interface with stops, timings, mode changes, bilingual context, and light/dark themes.', CORAL, ['HTML', 'SVG', 'Arabic UI']),
        ('JOB SEARCH DASHBOARD', 'WORKFLOW UX', 'Bilingual job-search workspace concept: new matches, drafts, awaiting replies, applications, and assistant flow.', GOLD, ['HTML', 'Bilingual', 'Product UX']),
    ]
    x = 70
    for title, subtitle, desc, accent, tags in cards:
        c += rect(x, 370, 465, 400, CARD, LINE, 12)
        c += rect(x, 370, 465, 8, accent, accent, 4)
        c += text(x + 32, 425, subtitle, 11, accent, MONO, '700', letter=1.2)
        c += text(x + 32, 480, title, 22, INK, MONO, '700', letter=.3)
        c += lines(x + 32, 550, [desc[i:i + 44] for i in range(0, len(desc), 44)], 16, 26, MUTED, SANS)
        tx = x + 32
        for tag in tags:
            c += pill(tx, 690, tag.upper(), CARD, accent, LINE)
            tx += len(tag) * 8 + 46
        x += 500
    c += rule(70, 830, 1530, 830, LINE)
    c += text(70, 870, 'Design is not decoration here. It is the compression layer between system state and human decision.', 20, INK, SERIF)
    c += text(1530, 870, 'DESIGN-LED  ·  LOCAL-FIRST  ·  READABLE', 12, TEAL, MONO, '700', 'end', 1)
    c += footer(6, 'OPERATIONS EXPLORER  ·  MALHAM LINE  ·  JOB SEARCH DASHBOARD', False)
    save('06-interfaces.svg', c)


def page_07():
    c = header(7, 'motion systems', '07')
    c += text(70, 155, '05 / MOTION SYSTEMS', 13, CORAL, MONO, '700', letter=1.4)
    c += text(70, 225, 'Motion as a system,', 60, INK, SERIF, '400', letter=-2)
    c += text(70, 283, 'not a pile of clips.', 60, CORAL, SERIF, '400', letter=-2)
    c += lines(70, 350, ['Remotion work across car edits, Arabic tech news,', 'commercial creative, and children’s storytelling.', 'The code separates timing, composition, and assets.'], 18, 29, MUTED, SANS)
    items = [
        ('CAR MEET', 'clip timing · camera movement · audio', CORAL),
        ('TECH NEWS', 'captions · voice layers · vertical framing', TEAL),
        ('WISAA', 'product story · Arabic type · campaign rhythm', GOLD),
        ('LITTLE LANTERNS', 'storyboard · hooks · QA manifest', CORAL),
        ('WHEELS ON THE BUS', 'FFmpeg assembly · deterministic render', TEAL),
    ]
    y = 480
    for i, (name, detail, accent) in enumerate(items):
        c += rule(70, y - 18, 1530, y - 18, LINE)
        c += text(70, y + 18, f'{i + 1:02d}', 12, accent, MONO, '700', letter=1)
        c += text(135, y + 18, name, 19, INK, MONO, '700', letter=.6)
        c += text(500, y + 18, detail, 16, MUTED, SANS)
        c += rect(1120, y + 3, 350, 12, '#E3DED3', '#E3DED3', 6)
        c += rect(1120, y + 3, 80 + i * 53, 12, accent, accent, 6)
        y += 74
    c += rect(70, 855, 1460, 55, '#F6E6DF', '#D5A08F', 8)
    c += text(100, 890, 'PUBLIC SNAPSHOT RULE  ·  SOURCE CODE is shareable; generated media and imported assets stay out until rights are clear.', 13, CORAL, MONO, '700', letter=.35)
    c += footer(7, 'REMOTION  ·  REACT  ·  TYPESCRIPT  ·  STORYBOARDING  ·  QA', False)
    save('07-motion.svg', c)


def page_08():
    c = header(8, 'proof + publishing', '08')
    c += text(70, 155, '06 / PROOF + PUBLISHING', 13, CORAL, MONO, '700', letter=1.4)
    c += text(70, 225, 'A clean public snapshot', 58, INK, SERIF, '400', letter=-2)
    c += text(70, 282, 'is part of the work.', 58, CORAL, SERIF, '400', letter=-2)
    c += text(70, 350, 'Evidence captured before publication', 13, TEAL, MONO, '700', letter=1.1)
    cols = [('PROJECT', 70), ('PROOF', 470), ('PUBLIC POSTURE', 1050)]
    for name, x in cols:
        c += text(x, 395, name, 11, MUTED, MONO, '700', letter=1)
    rows = [
        ('AgenticOS', '16 unit tests · syntax · smoke test', 'ready / runtime excluded'),
        ('Operations Explorer', '23 core tests · API policy checks', 'ready / local core'),
        ('Rizq POS', 'npm run build passes', 'hardening before real use'),
        ('Smart Black Box', 'C++ / ESP32 source on GitHub', 'private / access on request'),
        ('Remotion projects', 'lint + TypeScript checks pass', 'source-only / assets excluded'),
        ('Interfaces + analysis', 'static parse + source audit', 'docs + prototypes'),
    ]
    y = 435
    for i, (project, proof, posture) in enumerate(rows):
        c += rule(70, y - 18, 1530, y - 18, LINE)
        c += text(70, y + 16, project, 16, INK, SANS, '700')
        c += text(470, y + 16, proof, 15, MUTED, SANS)
        color = TEAL if 'ready' in posture else CORAL if 'hardening' in posture else GOLD
        c += text(1050, y + 16, posture, 13, color, MONO, '700')
        y += 61
    c += rect(70, 760, 700, 120, INK, INK, 10)
    c += text(105, 800, 'LEFT OUT OF THE PUBLIC SET', 11, '#D99D8B', MONO, '700', letter=1)
    c += lines(105, 835, ['credentials · runtime databases · browser profiles', 'private vault notes · generated media · third-party clones'], 15, 26, LIGHT, SANS)
    c += rect(830, 760, 700, 120, '#E4F0EE', '#A7C8C5', 10)
    c += text(865, 800, 'WHAT A COMPANY CAN SEE', 11, TEAL, MONO, '700', letter=1)
    c += lines(865, 835, ['problem framing · architecture · code quality', 'tests · constraints · honest readiness notes'], 15, 26, INK, SANS)
    c += footer(8, 'AUDITED LOCALLY  ·  SANITIZED STAGING  ·  READY FOR GITHUB PUBLICATION', False)
    save('08-proof.svg', c)


def page_09():
    c = header(9, 'close', '09')
    c += text(70, 180, 'LET’S BUILD THE', 13, CORAL, MONO, '700', letter=1.5)
    c += text(70, 300, 'next useful', 86, INK, SERIF, '400', letter=-3)
    c += text(70, 385, 'system.', 86, CORAL, SERIF, '400', letter=-3)
    c += lines(70, 505, ['Computer engineering student at Taif University,', 'graduating in 2026. Interested in AI systems,', 'automation, product software, embedded systems,', 'and cloud/networking foundations.'], 22, 34, MUTED, SANS)
    c += rect(980, 170, 550, 500, INK, INK, 12)
    c += text(1030, 225, 'CONTACT', 12, '#D99D8B', MONO, '700', letter=1.3)
    c += text(1030, 305, 'Mohammad J. Bakr', 36, LIGHT, SERIF)
    c += rule(1030, 350, 1460, 350, '#496064')
    c += text(1030, 410, 'mohammadbakrwork@gmail.com', 17, '#E8B4A4', MONO, '700')
    c += text(1030, 465, 'github.com/M7mdbkr', 17, '#D3E7E3', MONO, '700')
    c += text(1030, 520, 'Saudi Arabia  ·  Arabic / English', 15, '#AEBDBD', SANS)
    c += pill(1030, 580, 'OPEN TO ENGINEERING ROLES', '#26464A', '#D3E7E3', '#557277')
    c += text(70, 770, 'AI SYSTEMS', 13, TEAL, MONO, '700', letter=1.1)
    c += text(300, 770, 'AUTOMATION', 13, CORAL, MONO, '700', letter=1.1)
    c += text(535, 770, 'PRODUCT SOFTWARE', 13, GOLD, MONO, '700', letter=1.1)
    c += text(820, 770, 'INTERFACE DESIGN', 13, TEAL, MONO, '700', letter=1.1)
    c += text(70, 855, 'Thank you for looking.', 28, INK, SERIF)
    c += footer(9, 'MOHAMMAD J. BAKR  ·  BUILT SYSTEMS  ·  2026', False)
    save('09-contact.svg', c)


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    page_01(); page_02(); page_03(); page_04(); page_05(); page_06(); page_07(); page_08(); page_09()
    (OUT / 'README.md').write_text('''# Figma-ready portfolio report\n\nNine 1600×1000 SVG frames for importing into Figma. Import the SVGs in filename order to create a polished case-study report.\n\nThe report uses an original editorial visual system: warm paper, ink, coral, teal, and restrained mono labels. Project claims are limited to locally verified evidence; runtime data, credentials, private notes, generated media, and third-party clones are excluded.\n''', encoding='utf-8')
    print(f'created {len(list(OUT.glob("*.svg")))} SVG frames in {OUT}')
