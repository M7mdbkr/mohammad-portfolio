from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent / 'figma-report-v2'
W, H = 1920, 1080
M = 86
INK = '#10191C'
PAPER = '#F2EEE5'
CARD = '#FAF8F3'
MUTED = '#6B7678'
LINE = '#C9C5BA'
LIME = '#D9F36A'
CORAL = '#C95C3E'
TEAL = '#18727A'
GOLD = '#B68A3A'
DARK = '#10191C'
DARK2 = '#17272A'
LIGHT = '#F8F4EA'
DARK_MUTED = '#A6B5B3'
SERIF = 'Georgia, Times New Roman, serif'
SANS = 'Arial, Helvetica, sans-serif'
MONO = 'Courier New, monospace'


def esc(value):
    return escape(str(value), {'"': '&quot;'})


def text(x, y, value, size=18, fill=INK, family=SANS, weight='400', anchor='start', letter=0.0, opacity=1):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-family="{family}" font-size="{size}px" font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{letter}px" opacity="{opacity}">{esc(value)}</text>'


def lines(x, y, values, size=18, leading=28, fill=INK, family=SANS, weight='400', letter=0.0):
    return ''.join(text(x, y + i * leading, value, size, fill, family, weight, 'start', letter) for i, value in enumerate(values))


def rect(x, y, w, h, fill='none', stroke='none', radius=0, sw=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def line(x1, y1, x2, y2, stroke=LINE, sw=1, dash=''):
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{dash_attr}/>'


def circle(cx, cy, r, fill='none', stroke='none', sw=1, opacity=1):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"/>'


def tag(x, y, label, fill='#E2DED3', color=INK, stroke='none', width=None):
    w = width or len(label) * 8.2 + 30
    return rect(x, y, w, 32, fill, stroke, 16) + text(x + w / 2, y + 21, label, 11, color, MONO, '700', 'middle', .8)


def top(page, name, dark=False):
    fg = LIGHT if dark else INK
    muted = DARK_MUTED if dark else MUTED
    stroke = '#40575A' if dark else LINE
    return text(M, 58, 'MJB / 2026', 12, fg, MONO, '700', letter=1.5) + text(W - M, 58, f'{page:02d}  /  {name.upper()}', 12, muted, MONO, '700', 'end', 1.2) + line(M, 82, W - M, 82, stroke)


def bottom(page, caption, dark=False):
    muted = DARK_MUTED if dark else MUTED
    stroke = '#40575A' if dark else LINE
    return line(M, H - 76, W - M, H - 76, stroke) + text(M, H - 39, caption, 11, muted, MONO, '700', letter=.8) + text(W - M, H - 39, f'{page:02d} / 08', 11, muted, MONO, '700', 'end', .8)


def shell(content, dark=False):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="{DARK if dark else PAPER}"/>{content}</svg>'


def save(name, content, dark=False):
    (OUT / name).write_text(shell(content, dark), encoding='utf-8')


def page_01():
    c = top(1, 'cover')
    c += text(M, 170, 'COMPUTER ENGINEERING  /  PORTFOLIO REPORT', 13, CORAL, MONO, '700', letter=1.5)
    c += text(M, 330, 'Build', 148, INK, SERIF, '400', letter=-6)
    c += text(M, 468, 'with', 148, INK, SERIF, '400', letter=-6)
    c += text(M, 606, 'intent.', 148, CORAL, SERIF, '400', letter=-6)
    c += rect(1110, 145, 724, 730, INK, INK, 18)
    c += circle(1472, 392, 210, 'none', LIME, 2)
    c += circle(1472, 392, 158, 'none', '#4E6969', 1)
    c += circle(1472, 392, 74, LIME, LIME)
    c += text(1472, 400, 'M', 50, INK, SERIF, '700', 'middle')
    c += line(1472, 177, 1472, 320, '#557071', 1)
    c += line(1472, 464, 1472, 608, '#557071', 1)
    c += line(1257, 392, 1398, 392, '#557071', 1)
    c += line(1546, 392, 1688, 392, '#557071', 1)
    c += text(1170, 735, 'LOCAL-FIRST', 12, LIME, MONO, '700', letter=1.2)
    c += text(1170, 770, 'SYSTEMS  /  PRODUCTS  /  INTERFACES', 13, LIGHT, MONO, '700', letter=.8)
    c += text(1170, 824, 'Mohammad J. Bakr', 24, LIGHT, SERIF)
    c += text(M, 805, 'Practical software where automation, interfaces,', 22, MUTED, SANS)
    c += text(M, 838, 'and safety have to work together.', 22, MUTED, SANS)
    c += tag(M, 900, 'PYTHON', CARD, TEAL, LINE)
    c += tag(190, 900, 'TYPESCRIPT', CARD, TEAL, LINE)
    c += tag(330, 900, 'REACT', CARD, TEAL, LINE)
    c += tag(430, 900, 'SQLITE', CARD, TEAL, LINE)
    c += tag(540, 900, 'EMBEDDED', CARD, TEAL, LINE)
    c += bottom(1, 'MOHAMMAD J. BAKR  ·  SAUDI ARABIA  ·  OPEN TO ENGINEERING ROLES')
    save('01-cover.svg', c)


def page_02():
    c = top(2, 'throughline')
    c += text(M, 165, 'THE THROUGHLINE', 13, CORAL, MONO, '700', letter=1.5)
    c += text(M, 245, 'One engineering instinct.', 64, INK, SERIF, '400', letter=-2)
    c += text(M, 305, 'Many surfaces.', 64, CORAL, SERIF, '400', letter=-2)
    c += lines(M, 390, ['The work moves from embedded safety hardware to local AI systems,', 'Arabic-first products, automation bots, and motion compositions.'], 20, 32, MUTED, SANS)
    columns = [
        ('01', 'SYSTEMS', 'State, policy, routing, and auditability.', ['AgenticOS', 'Operations Explorer', 'Alfred Clean']),
        ('02', 'PRODUCTS', 'Real workflows shaped around real users.', ['Rizq POS', 'Job Search Dashboard', 'Arabic News Bot']),
        ('03', 'SURFACES', 'Interfaces and media that make ideas legible.', ['Malham Line', 'Remotion compositions', 'Little Lanterns']),
    ]
    x = M
    for num, title, desc, items in columns:
        c += rect(x, 560, 515, 320, CARD, LINE, 16)
        c += text(x + 30, 610, num, 12, CORAL if num != '02' else TEAL, MONO, '700', letter=1)
        c += text(x + 30, 655, title, 25, INK, MONO, '700', letter=1)
        c += text(x + 30, 700, desc, 16, MUTED, SANS)
        c += line(x + 30, 730, x + 485, 730, LINE)
        for i, item in enumerate(items):
            c += text(x + 30, 765 + i * 30, item, 15, INK, SANS, '600')
            c += text(x + 480, 765 + i * 30, '↗', 15, TEAL, SERIF, '400', 'end')
        x += 550
    c += rect(70, 930, 1780, 42, INK, INK, 21)
    c += text(960, 957, 'BUILD  →  EXPLAIN  →  VERIFY  →  SHIP SAFELY', 12, LIME, MONO, '700', 'middle', 1.1)
    c += bottom(2, 'THE COMMON THREAD  ·  VISIBLE STATE  ·  EXPLICIT ACTIONS  ·  HONEST LIMITS')
    save('02-throughline.svg', c)


def page_03():
    c = top(3, 'AgenticOS', True)
    c += text(M, 160, '01 / FEATURED CASE', 13, '#F0A48E', MONO, '700', letter=1.5)
    c += text(M, 245, 'AgenticOS', 84, LIGHT, SERIF, '400', letter=-3)
    c += text(M, 296, 'A personal agent operating system with a safety boundary.', 22, DARK_MUTED, SANS)
    c += text(M, 420, 'THE IDEA', 12, '#F0A48E', MONO, '700', letter=1.2)
    c += lines(M, 465, ['Give agents useful capabilities without giving them', 'silent authority over the outside world.'], 30, 40, LIGHT, SERIF)
    c += text(M, 620, 'THE PROOF', 12, '#F0A48E', MONO, '700', letter=1.2)
    proof = [('16', 'unit tests pass'), ('SHA-256', 'audit chain'), ('127.0.0.1', 'loopback default')]
    x = M
    for value, label in proof:
        c += text(x, 680, value, 27, LIME, MONO, '700')
        c += text(x, 715, label, 14, DARK_MUTED, SANS)
        x += 220 if value != 'SHA-256' else 260
    c += rect(930, 145, 900, 690, DARK2, '#496467', 18)
    c += text(980, 200, 'SYSTEM FLOW', 12, '#F0A48E', MONO, '700', letter=1.2)
    c += rect(1000, 270, 760, 105, '#213B3F', '#587174', 10)
    c += text(1040, 312, 'BROWSER', 13, LIME, MONO, '700', letter=1)
    c += text(1040, 350, 'chat  ·  workspaces  ·  approvals  ·  schedules', 18, LIGHT, SANS)
    c += text(1380, 405, '↓', 30, '#F0A48E', SERIF, '400', 'middle')
    c += rect(1000, 450, 760, 105, '#213B3F', '#587174', 10)
    c += text(1040, 492, 'LOCAL OPERATIONS STORE', 13, LIME, MONO, '700', letter=1)
    c += text(1040, 530, 'Python  ·  SQLite  ·  context  ·  agent routing', 18, LIGHT, SANS)
    c += text(1380, 585, '↓', 30, '#F0A48E', SERIF, '400', 'middle')
    c += rect(1000, 630, 760, 105, '#2E4B43', LIME, 10, 2)
    c += text(1040, 672, 'APPROVAL GATE', 13, LIME, MONO, '700', letter=1)
    c += text(1040, 710, 'exact payload  →  human click  →  external effect', 18, LIGHT, SANS)
    c += text(1000, 790, 'optional connectors: Telegram  ·  n8n  ·  Ollama', 13, DARK_MUTED, MONO, '700')
    c += tag(M, 835, 'PUBLIC SNAPSHOT', '#203A3D', LIGHT, '#557174')
    c += text(310, 856, 'runtime data excluded', 14, DARK_MUTED, SANS)
    c += text(1830, 857, 'github.com/M7mdbkr/agenticos', 16, '#F0A48E', MONO, '700', 'end')
    c += bottom(3, 'AGENTICOS  ·  PYTHON  ·  SQLITE  ·  VANILLA JS  ·  APPROVAL-GATED  ·  AUDITABLE', True)
    save('03-agenticos.svg', c, True)


def page_04():
    c = top(4, 'Rizq POS')
    c += text(M, 160, '02 / PRODUCT CASE', 13, CORAL, MONO, '700', letter=1.5)
    c += text(M, 245, 'Rizq POS', 84, INK, SERIF, '400', letter=-3)
    c += text(M, 296, 'Arabic-first RTL point of sale for cafés and restaurants.', 22, MUTED, SANS)
    c += rect(M, 375, 920, 490, INK, INK, 18)
    c += text(M + 38, 425, 'RIZQ / الكاشير', 15, '#E5B09F', MONO, '700', letter=1)
    c += rect(M + 38, 465, 205, 350, '#20383D', '#557174', 9)
    c += text(M + 65, 510, 'OWNER', 11, LIME, MONO, '700', letter=1)
    for i, item in enumerate(['Inventory', 'Orders', 'Discounts', 'Ledger']):
        c += text(M + 65, 570 + i * 48, item, 17, LIGHT if i == 1 else DARK_MUTED, SANS, '600' if i == 1 else '400')
    c += rect(M + 275, 465, 605, 350, '#F7F3EA', '#F7F3EA', 9)
    c += text(M + 315, 510, 'طلب جديد', 21, INK, SANS, '700')
    c += line(M + 315, 540, M + 840, 540, '#CEC8BC')
    c += text(M + 315, 590, 'قهوة عربية', 17, INK, SANS)
    c += text(M + 840, 590, '18.00 ر.س', 17, CORAL, MONO, '700', 'end')
    c += text(M + 315, 650, 'ضريبة القيمة المضافة', 15, MUTED, SANS)
    c += text(M + 840, 650, '15%', 15, TEAL, MONO, '700', 'end')
    c += line(M + 315, 680, M + 840, 680, '#CEC8BC')
    c += text(M + 315, 735, 'الإجمالي', 22, INK, SANS, '700')
    c += text(M + 840, 735, '20.70 ر.س', 22, CORAL, MONO, '700', 'end')
    c += rect(M + 315, 765, 525, 34, CORAL, CORAL, 17)
    c += text(M + 577, 788, 'إتمام الطلب', 13, '#FFF8F0', SANS, '700', 'middle')
    c += text(1110, 410, 'THE PRODUCT STORY', 12, CORAL, MONO, '700', letter=1.2)
    c += lines(1110, 470, ['A real operational surface,', 'not just a dashboard mockup.'], 32, 38, INK, SERIF)
    c += lines(1110, 610, ['Cashier + owner flows.', 'Browser-local SQLite/WASM.', 'Inventory, receipts, CSV export.', 'Arabic typography and RTL layout.'], 18, 34, MUTED, SANS)
    c += rect(1110, 760, 720, 105, '#F7E7E0', '#D5A08F', 12)
    c += text(1145, 800, 'READINESS NOTE', 11, CORAL, MONO, '700', letter=1)
    c += text(1145, 837, 'Build passes. Harden before real customer data.', 17, INK, SANS, '700')
    c += tag(M, 920, 'REACT', CARD, TEAL, LINE)
    c += tag(184, 920, 'TYPESCRIPT', CARD, TEAL, LINE)
    c += tag(330, 920, 'VITE', CARD, TEAL, LINE)
    c += tag(420, 920, 'SQL.JS', CARD, TEAL, LINE)
    c += text(1830, 941, 'github.com/M7mdbkr/rizq-pos-demo', 15, CORAL, MONO, '700', 'end')
    c += bottom(4, 'RIZQ POS  ·  RTL  ·  PRODUCT THINKING  ·  DEMO-FIRST')
    save('04-rizq-pos.svg', c)


def page_05():
    c = top(5, 'pipelines', True)
    c += text(M, 160, '03 / AUTOMATION + DATA', 13, '#F0A48E', MONO, '700', letter=1.5)
    c += text(M, 245, 'From signal', 78, LIGHT, SERIF, '400', letter=-3)
    c += text(M, 320, 'to useful output.', 78, '#F0A48E', SERIF, '400', letter=-3)
    c += lines(M, 410, ['The interesting part is the chain: fetch, normalize, store,', 'translate, explain, and send only what the user can inspect.'], 20, 32, DARK_MUTED, SANS)
    c += rect(M, 550, 845, 300, DARK2, '#496467', 16)
    c += text(M + 35, 602, 'ARABIC NEWS BOT', 13, LIME, MONO, '700', letter=1.2)
    c += text(M + 35, 655, 'RSS  →  Arabic  →  Telegram', 30, LIGHT, SERIF)
    c += lines(M + 35, 710, ['multi-feed polling', 'SQLite deduplication', 'owner-only commands', 'weekly report + video script'], 16, 28, DARK_MUTED, SANS)
    c += rect(995, 550, 835, 300, '#2E4B43', '#557174', 16)
    c += text(1030, 602, 'CRYPTO SIGNAL ANALYZER', 13, LIME, MONO, '700', letter=1.2)
    c += text(1030, 655, 'Data, with the caveat attached.', 30, LIGHT, SERIF)
    c += lines(1030, 710, ['CoinGecko market data', 'volatility + drawdown + rank', '7d / 30d momentum', 'informational, not a promise'], 16, 28, '#D6E0DD', SANS)
    c += text(M, 935, '01', 12, '#F0A48E', MONO, '700')
    c += text(M + 48, 935, 'FETCH', 12, DARK_MUTED, MONO, '700')
    c += line(M + 122, 930, M + 405, 930, '#557174', 2)
    c += text(M + 435, 935, '02', 12, '#F0A48E', MONO, '700')
    c += text(M + 483, 935, 'NORMALIZE', 12, DARK_MUTED, MONO, '700')
    c += line(M + 590, 930, M + 880, 930, '#557174', 2)
    c += text(M + 910, 935, '03', 12, '#F0A48E', MONO, '700')
    c += text(M + 958, 935, 'STORE + EXPLAIN', 12, DARK_MUTED, MONO, '700')
    c += line(M + 1125, 930, W - M, 930, LIME, 2)
    c += bottom(5, 'PYTHON  ·  RSS / HTTP APIs  ·  SQLITE  ·  TELEGRAM  ·  EXPLAINABLE OUTPUT', True)
    save('05-pipelines.svg', c, True)


def page_06():
    c = top(6, 'embedded safety')
    c += text(M, 160, '04 / EMBEDDED SYSTEMS', 13, CORAL, MONO, '700', letter=1.5)
    c += text(M, 245, 'Smart Black Box', 74, INK, SERIF, '400', letter=-3)
    c += text(M, 300, 'Graduation project · ESP32 vehicle safety prototype.', 22, MUTED, SANS)
    c += rect(M, 390, 720, 450, INK, INK, 18)
    c += text(M + 40, 440, 'THE HARDWARE LOOP', 12, '#F0A48E', MONO, '700', letter=1.2)
    modules = [('SENSE', 'MPU6050  ·  MQ-135  ·  GPS  ·  OBD-II'), ('DECIDE', 'ESP32  ·  configurable thresholds'), ('RESPOND', 'SD log  ·  SMS  ·  Google Maps link')]
    y = 505
    for i, (title, desc) in enumerate(modules):
        c += rect(M + 40, y, 640, 78, '#20383D', '#557174', 10)
        c += text(M + 70, y + 31, f'{i + 1:02d}', 12, LIME, MONO, '700')
        c += text(M + 120, y + 31, title, 13, '#F0A48E', MONO, '700', letter=1)
        c += text(M + 120, y + 57, desc, 16, LIGHT, SANS)
        if i < 2: c += text(M + 360, y + 107, '↓', 25, CORAL, SERIF, '400', 'middle')
        y += 120
    c += rect(925, 390, 905, 450, CARD, LINE, 18)
    c += text(970, 440, 'WHY IT MATTERS', 12, TEAL, MONO, '700', letter=1.2)
    c += lines(970, 505, ['A low-cost, locally engineered record', 'of impact, location, and cabin conditions.'], 31, 39, INK, SERIF)
    c += line(970, 625, 1785, 625, LINE)
    c += text(970, 675, 'PROJECT LEAD', 11, MUTED, MONO, '700', letter=1)
    c += text(970, 708, 'Mohammad J. Bakr', 18, INK, SANS, '700')
    c += text(970, 760, '14-member team · Taif University', 16, MUTED, SANS)
    c += tag(970, 795, 'C++', '#E4F0EE', TEAL, '#A7C8C5')
    c += tag(1050, 795, 'ESP32', '#E4F0EE', TEAL, '#A7C8C5')
    c += tag(1160, 795, 'OBD-II', '#E4F0EE', TEAL, '#A7C8C5')
    c += tag(1270, 795, 'GPS / GSM', '#E4F0EE', TEAL, '#A7C8C5')
    c += rect(M, 900, 1780, 54, '#F7E7E0', '#D5A08F', 10)
    c += text(M + 30, 934, 'GITHUB STATUS', 11, CORAL, MONO, '700', letter=1)
    c += text(M + 220, 934, 'private by choice · graduation team project · access on request', 15, INK, SANS)
    c += bottom(6, 'SMART BLACK BOX  ·  C++  ·  ESP32  ·  SENSOR FUSION  ·  SAFETY-CRITICAL THINKING')
    save('06-smart-black-box.svg', c)


def page_07():
    c = top(7, 'gallery', True)
    c += text(M, 160, '05 / INTERFACE + MOTION GALLERY', 13, '#F0A48E', MONO, '700', letter=1.5)
    c += text(M, 245, 'Make the system', 72, LIGHT, SERIF, '400', letter=-3)
    c += text(M, 315, 'legible.', 72, LIME, SERIF, '400', letter=-3)
    c += text(M, 390, 'A selection of surfaces built around hierarchy, timing, and context.', 20, DARK_MUTED, SANS)
    items = [
        ('MALHAM LINE', 'route planning', 'bilingual stops · timing · SVG route', '#F0A48E'),
        ('JOB SEARCH', 'workflow UX', 'matches · drafts · replies · applications', LIME),
        ('TECH NEWS', 'motion system', 'Arabic captions · voice layers · 9:16', '#7ED3D4'),
        ('LITTLE LANTERNS', 'production pipeline', 'storyboard · hooks · QA manifest', '#F0A48E'),
    ]
    y = 500
    for i, (name, kind, detail, accent) in enumerate(items):
        c += line(M, y - 28, W - M, y - 28, '#40575A')
        c += text(M, y + 18, f'{i + 1:02d}', 12, accent, MONO, '700', letter=1)
        c += text(M + 75, y + 18, name, 20, LIGHT, MONO, '700', letter=.8)
        c += text(M + 560, y + 18, kind.upper(), 11, accent, MONO, '700', letter=1)
        c += text(M + 925, y + 18, detail, 16, DARK_MUTED, SANS)
        c += rect(1580, y - 5, 250, 14, '#263D40', '#263D40', 7)
        c += rect(1580, y - 5, 55 + i * 45, 14, accent, accent, 7)
        y += 83
    c += rect(M, 885, 1780, 50, '#203A3D', '#557174', 10)
    c += text(M + 30, 917, 'PUBLIC SNAPSHOT RULE', 11, LIME, MONO, '700', letter=1)
    c += text(M + 255, 917, 'code is shareable; imported media, generated audio, and private footage stay out until rights are clear.', 15, LIGHT, SANS)
    c += bottom(7, 'HTML  ·  CSS  ·  JAVASCRIPT  ·  REACT  ·  REMOTION  ·  ARABIC-FIRST DESIGN', True)
    save('07-gallery.svg', c, True)


def page_08():
    c = top(8, 'close')
    c += text(M, 165, '06 / CLOSE', 13, CORAL, MONO, '700', letter=1.5)
    c += text(M, 285, 'Let’s build the', 92, INK, SERIF, '400', letter=-4)
    c += text(M, 380, 'next useful', 92, INK, SERIF, '400', letter=-4)
    c += text(M, 475, 'system.', 92, CORAL, SERIF, '400', letter=-4)
    c += lines(M, 595, ['Mohammad J. Bakr · Computer Engineering student', 'Taif University · graduating 2026', 'Saudi Arabia · Arabic native · English fluent'], 20, 32, MUTED, SANS)
    c += rect(1050, 160, 780, 535, INK, INK, 18)
    c += text(1100, 220, 'CONTACT', 12, '#F0A48E', MONO, '700', letter=1.2)
    c += text(1100, 310, 'Mohammad J. Bakr', 42, LIGHT, SERIF)
    c += line(1100, 355, 1780, 355, '#496467')
    c += text(1100, 430, 'mohammadbakrwork@gmail.com', 18, '#F0A48E', MONO, '700')
    c += text(1100, 485, 'github.com/M7mdbkr', 18, '#D6E0DD', MONO, '700')
    c += text(1100, 540, 'm7mdbkr.github.io/mohammad-portfolio', 16, LIME, MONO, '700')
    c += tag(1100, 615, 'OPEN TO ENGINEERING ROLES', '#29464A', LIGHT, '#557174')
    c += text(M, 825, 'SYSTEMS', 13, TEAL, MONO, '700', letter=1.2)
    c += text(320, 825, 'AUTOMATION', 13, CORAL, MONO, '700', letter=1.2)
    c += text(620, 825, 'PRODUCT SOFTWARE', 13, GOLD, MONO, '700', letter=1.2)
    c += text(1030, 825, 'INTERFACE DESIGN', 13, TEAL, MONO, '700', letter=1.2)
    c += line(M, 860, W - M, 860, INK, 2)
    c += text(M, 910, 'Thank you for looking.', 27, INK, SERIF)
    c += text(W - M, 910, 'github.com/M7mdbkr/mohammad-portfolio', 15, CORAL, MONO, '700', 'end')
    c += bottom(8, 'MOHAMMAD J. BAKR  ·  BUILT SYSTEMS  ·  2026')
    save('08-contact.svg', c)


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    page_01(); page_02(); page_03(); page_04(); page_05(); page_06(); page_07(); page_08()
    (OUT / 'README.md').write_text('''# Figma-ready portfolio report V2\n\nEight 1920×1080 SVG frames for Figma import. Import the SVGs in filename order.\n\nV2 uses a tighter editorial system, fewer generic cards, stronger case-study hierarchy, system diagrams, and explicit readiness notes.\n''', encoding='utf-8')
    print(f'created {len(list(OUT.glob("*.svg")))} SVG frames in {OUT}')
