from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

W, H = A4

# ── Colour palette ──────────────────────────────────────────────────────────
C_BLUE_DARK  = colors.HexColor('#0C447C')
C_BLUE_MID   = colors.HexColor('#378ADD')
C_BLUE_LIGHT = colors.HexColor('#E6F1FB')
C_BLUE_BORDER= colors.HexColor('#B5D4F4')

C_GREEN_DARK  = colors.HexColor('#27500A')
C_GREEN_MID   = colors.HexColor('#639922')
C_GREEN_LIGHT = colors.HexColor('#EAF3DE')
C_GREEN_BORDER= colors.HexColor('#C0DD97')

C_AMBER_DARK  = colors.HexColor('#633806')
C_AMBER_MID   = colors.HexColor('#BA7517')
C_AMBER_LIGHT = colors.HexColor('#FAEEDA')
C_AMBER_BORDER= colors.HexColor('#FAC775')

C_PURPLE_DARK  = colors.HexColor('#3C3489')
C_PURPLE_MID   = colors.HexColor('#7F77DD')
C_PURPLE_LIGHT = colors.HexColor('#EEEDFE')
C_PURPLE_BORDER= colors.HexColor('#CECBF6')

C_GRAY_LIGHT = colors.HexColor('#F1EFE8')
C_GRAY_MID   = colors.HexColor('#B4B2A9')
C_GRAY_DARK  = colors.HexColor('#2C2C2A')
C_BLACK      = colors.HexColor('#1A1A1A')
C_WHITE      = colors.white

# ── Styles ───────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

sTitle = S('sTitle',
    fontName='Helvetica-Bold', fontSize=22, textColor=C_BLACK,
    spaceAfter=4, leading=28, alignment=TA_LEFT)

sSubtitle = S('sSubtitle',
    fontName='Helvetica', fontSize=12, textColor=colors.HexColor('#5F5E5A'),
    spaceAfter=2, leading=16)

sMeta = S('sMeta',
    fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#5F5E5A'),
    leading=14, spaceAfter=0)

sHook = S('sHook',
    fontName='Helvetica', fontSize=10, textColor=C_BLUE_DARK,
    leading=15, spaceAfter=0)

sSceneHeader = S('sSceneHeader',
    fontName='Helvetica-Bold', fontSize=13, textColor=C_WHITE,
    leading=18, spaceAfter=0)

sSceneTiming = S('sSceneTiming',
    fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#CECBF6'),
    leading=14, spaceAfter=0)

sBlockLabel = S('sBlockLabel',
    fontName='Helvetica-Bold', fontSize=8, leading=12, spaceAfter=3,
    textColor=C_BLACK)

sBlockBody = S('sBlockBody',
    fontName='Helvetica', fontSize=9, leading=14, spaceAfter=0,
    textColor=C_BLACK)

sLegendLabel = S('sLegendLabel',
    fontName='Helvetica', fontSize=9, textColor=colors.HexColor('#5F5E5A'),
    leading=12)

sFooter = S('sFooter',
    fontName='Helvetica', fontSize=8, textColor=C_GRAY_MID,
    alignment=TA_CENTER, leading=11)

# ── Scene data ───────────────────────────────────────────────────────────────
scenes = [
  {
    "num":"01", "title":"Hook — The Problem", "timing":"0:00 – 1:00",
    "aroll":"""You (face-cam, slight lean forward, serious tone):

"Everyone's talking about AI replacing developers. But here's what they're NOT telling you — if you learn web dev the RIGHT way, using AI as your co-pilot, you can get job-ready in half the time." Pause. Smirk. "Let me show you exactly how." """,
    "broll":"""Quick-cut montage: VS Code with Copilot suggestions appearing, ChatGPT answering a coding question, a portfolio website loading, GitHub commit history filling up rapidly. End on a clean roadmap graphic animating in.""",
    "tos":"""CENTERED BOLD:
"Can AI help you learn to code FASTER?"

Bottom left badge:
"2025 Web Dev Roadmap"

Chapter card:
"SCENE 1: The Problem Most Beginners Face" """,
    "vo":"""Upbeat lo-fi music fades in. Presenter speaks directly to camera throughout. Music duck under speech at -18db."""
  },
  {
    "num":"02", "title":"Roadmap Overview — The Big Picture", "timing":"1:00 – 2:30",
    "aroll":"""You (relaxed, gesturing at screen or whiteboard):

"Before we dive in, here's what the entire journey looks like. Five stages. Each one builds on the last. And yes — we'll use AI at every single stage." Walk through each stage briefly, pointing to visual.""",
    "broll":"""Animated roadmap graphic slides in showing: Stage 1 → Foundations, Stage 2 → JavaScript, Stage 3 → React, Stage 4 → Backend, Stage 5 → Portfolio. Each stage box highlights as mentioned. Transition arrows between stages.""",
    "tos":"""ROADMAP GRAPHIC LABELS:
— Stage 1: HTML/CSS Foundations
— Stage 2: JavaScript Core
— Stage 3: React (Frontend Framework)
— Stage 4: Node.js + Databases
— Stage 5: Portfolio & Job Hunting

Callout badge: "AI Tools at Every Step ✓"

Bottom bar: "Estimated: 6–12 months (with AI: 4–8 months)" """,
    "vo":"""VO over B-roll: "Think of this like a map. Most people start driving without one — and that's why 80% of beginners quit. Today, you're getting the map." """
  },
  {
    "num":"03", "title":"Stage 1 — HTML & CSS with AI", "timing":"2:30 – 4:30",
    "aroll":"""You (energetic):

"Stage one — Foundations. HTML and CSS. I know, I know — everyone says this is boring. But here's the secret: use AI to EXPLAIN things as you go." Open ChatGPT. "Instead of a 3-hour tutorial, ask AI to give you a project first, then explain what you don't understand." """,
    "broll":"""Screen recording: Type into ChatGPT — 'Give me a beginner HTML/CSS project and break it down step by step.' Show the response. Cut to VS Code with a basic webpage being built. Copilot suggests closing tags and class names. Zoom into browser preview refreshing in real time.""",
    "tos":"""STAGE BADGE: "Stage 1 of 5 — HTML & CSS"

TIPS (appear one by one):
✅ Start with projects, not tutorials
✅ Ask AI to explain every line you don't get
✅ Build 3 pages before moving on

COUNTER: "Time to complete: 2–4 weeks"

AI PROMPT OVERLAY:
"Prompt: 'Explain flexbox like I'm 10 years old'" """,
    "vo":"""VO over screen recording: "The biggest mistake beginners make is watching tutorials passively. AI flips this — you build first, understand second. It mirrors how real developers actually work." """
  },
  {
    "num":"04", "title":"Stage 2 — JavaScript & AI Debugging", "timing":"4:30 – 6:30",
    "aroll":"""You (slightly frustrated expression, then relief):

"JavaScript. This is where most people QUIT. The error messages make zero sense. But THIS is where AI becomes your best friend." Open VS Code. "Watch what happens when I paste my broken code into Claude." """,
    "broll":"""Screen recording sequence: Write a buggy JavaScript function (arrow function with wrong return). Red error in console. Copy error + code → paste into Claude. Claude explains the bug clearly with a fixed version. Paste fix back into VS Code. Console shows success. Developer does a mini fist pump.""",
    "tos":"""STAGE BADGE: "Stage 2 of 5 — JavaScript"

CALLOUT:
"🚨 Error messages are AI prompts waiting to happen"

KEY CONCEPTS TICKER (bottom bar):
"Variables → Functions → Arrays → DOM → Events → Async/Await → APIs"

TIMER: "Estimated: 4–6 weeks"

PROMPT TIP:
"Paste error + code and say: 'What's wrong and how do I fix it?'" """,
    "vo":"""VO during B-roll: "AI doesn't just fix your code — it teaches you WHY it was broken. That's the difference between copy-paste and actually learning." """
  },
  {
    "num":"05", "title":"Stage 3 — React & AI Code Generation", "timing":"6:30 – 8:30",
    "aroll":"""You (leaning in, excited):

"Stage three — React. This is where you go from 'I can make websites' to 'I can build apps.' And with GitHub Copilot? You'll write components in half the time." Open VS Code with Copilot enabled. "Watch me describe what I want in a comment and let AI write the first draft." """,
    "broll":"""Screen recording: Create a new React component file. Type a comment: '// A card component that shows user profile photo, name, and bio with a follow button.' GitHub Copilot autocompletes the entire component. Show it render in the browser. Then cut to: ChatGPT conversation — 'What's the difference between useState and useEffect? Give me a simple example.' Show clear, practical AI response.""",
    "tos":"""STAGE BADGE: "Stage 3 of 5 — React"

OVERLAY STATS:
"React powers: Meta, Airbnb, Netflix, Twitter (X)"

COMPONENT LABELS on code:
"Props → State → Hooks → Components → Routing"

AI WORKFLOW GRAPHIC:
"Comment what you want → AI drafts → You review + customize → Ship it"

PRO TIP BOX:
"💡 Never accept AI code blindly — always read it line by line" """,
    "vo":"""VO: "AI code generation is like having a senior developer pair-programming with you 24/7. The key is staying in the driver's seat — AI suggests, you decide." """
  },
  {
    "num":"06", "title":"Stage 4 — Backend, Node.js & Databases", "timing":"8:30 – 10:30",
    "aroll":"""You (direct, clear):

"Stage four is where it gets real. Backend development. This is the engine behind everything. And honestly? This used to take years to learn. With AI? It's a different game." Pull up a terminal. "I'll show you how to set up an Express server in under 3 minutes using AI as your guide." """,
    "broll":"""Screen recording: Open Claude or ChatGPT. Type: 'Give me a minimal Express.js server with one GET endpoint that returns a JSON list of users.' Copy output to VS Code. Run npm install + node server.js in terminal. Browser shows JSON response. Cut to: Database diagram of a simple schema. Then ChatGPT explaining SQL vs NoSQL in plain English with a comparison table.""",
    "tos":"""STAGE BADGE: "Stage 4 of 5 — Backend + Databases"

TECH STACK LABELS:
"Node.js → Express.js → REST APIs → MongoDB or PostgreSQL → Authentication"

KEY CONCEPT CALLOUT:
"Frontend = what users see
Backend = what makes it WORK"

AI PROMPT STRIP:
"Try: 'Explain how a REST API works using a pizza restaurant analogy'"

BOTTOM TIMER: "Estimated: 6–8 weeks" """,
    "vo":"""VO during B-roll: "The backend used to feel like a black box. AI turns it into a glass box — you can see exactly how each piece fits together, and ask why until it clicks." """
  },
  {
    "num":"07", "title":"Stage 5 — Portfolio, GitHub & Jobs", "timing":"10:30 – 12:30",
    "aroll":"""You (warm, practical):

"Last stage — and this one people always rush. Don't. Your portfolio is your first impression. Use AI to help you write project descriptions, README files, and even prep for technical interviews." Pull up a GitHub profile. "Three quality projects beats ten half-finished ones every time." """,
    "broll":"""Screen recording montage: GitHub profile with pinned repos. Click into a repo — show a well-written README generated with AI help. Cut to: ChatGPT conversation: 'Write a professional README for a React todo app with these features…' — show output. Then: LinkedIn profile being updated. Then: Mock interview session with ChatGPT acting as an interviewer — question and answer back and forth. End on: A clean portfolio website loading on both desktop and mobile.""",
    "tos":"""STAGE BADGE: "Stage 5 of 5 — Portfolio & Jobs"

CHECKLIST:
☑ 3 projects on GitHub
☑ Live deployed versions (Vercel / Netlify)
☑ Clean README files
☑ LinkedIn + portfolio website updated
☑ Practice 30 common interview questions with AI

AI USE CASE CARDS:
"AI writes your README"
"AI mocks your interview"
"AI reviews your resume"

MOTIVATION BAR:
"You're closer than you think. Keep going." """,
    "vo":"""VO: "AI can even roleplay as your interviewer. Ask it to give you hard React questions, then critique your answers. That's 100 hours of interview prep in your bedroom." """
  },
  {
    "num":"08", "title":"Outro — Recap & CTA", "timing":"12:30 – 14:00",
    "aroll":"""You (direct to camera, confident but warm):

"That's the full roadmap. Five stages. HTML and CSS → JavaScript → React → Backend → Portfolio. And AI as your co-pilot the entire way. The people who learn to USE AI while learning will leave everyone else behind." Smile. "Drop a comment: which stage are YOU at right now? And if this helped — subscribe, because next week I'm doing a deep dive on the exact AI prompts that cut my learning time in half." Point to screen.""",
    "broll":"""Quick recap montage — 5-second clips from each stage's B-roll, each labeled Stage 1 through 5. End card appears: Subscribe button animates in, two video thumbnails slide in for 'Watch Next' and 'Watch Later'. Upbeat outro music swells.""",
    "tos":"""FULL SCREEN RECAP GRAPHIC:
"Your Web Dev Roadmap"
Stage 1 → HTML/CSS (2–4 weeks)
Stage 2 → JavaScript (4–6 weeks)
Stage 3 → React (4–6 weeks)
Stage 4 → Backend (6–8 weeks)
Stage 5 → Portfolio (ongoing)

CTA OVERLAY:
"👇 Comment which stage you're at!"
"🔔 Subscribe for weekly dev tutorials"

END CARD:
Watch Next: 'Best AI Prompts for Coding'
Watch Later: 'Build Your First React App' """,
    "vo":"""Outro music: lo-fi / hip-hop beat at full volume. VO over recap: "Six months from now, you could be a working developer. The roadmap is here — all you have to do is start." """
  }
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def nbsp(s):
    return s.replace('\n', '<br/>')

def block_table(scene):
    """Build a 2x2 table of the four blocks for a scene."""
    cell_pad = 7

    def cell(label, text, bg, label_color, text_color, border_color):
        lbl = Paragraph(label, ParagraphStyle('bl',
            fontName='Helvetica-Bold', fontSize=8, leading=11,
            textColor=label_color, spaceAfter=4))
        body = Paragraph(nbsp(text.strip()), ParagraphStyle('bb',
            fontName='Helvetica', fontSize=8.5, leading=13,
            textColor=text_color))
        return [lbl, body]

    aroll_cell  = cell('A-ROLL — TALKING HEAD',  scene['aroll'],  C_GREEN_LIGHT,  C_GREEN_MID,  C_GREEN_DARK,  C_GREEN_BORDER)
    broll_cell  = cell('B-ROLL — VISUALS / SCREEN', scene['broll'], C_BLUE_LIGHT,  C_BLUE_MID,   C_BLUE_DARK,   C_BLUE_BORDER)
    tos_cell    = cell('TEXT ON SCREEN',           scene['tos'],    C_AMBER_LIGHT, C_AMBER_MID,  C_AMBER_DARK,  C_AMBER_BORDER)
    vo_cell     = cell('VOICEOVER / AUDIO NOTES',  scene['vo'],     C_PURPLE_LIGHT,C_PURPLE_MID, C_PURPLE_DARK, C_PURPLE_BORDER)

    col = (W - 30*mm) / 2

    data = [
        [aroll_cell,  broll_cell],
        [tos_cell,    vo_cell],
    ]

    style = TableStyle([
        # backgrounds
        ('BACKGROUND', (0,0),(0,0), C_GREEN_LIGHT),
        ('BACKGROUND', (1,0),(1,0), C_BLUE_LIGHT),
        ('BACKGROUND', (0,1),(0,1), C_AMBER_LIGHT),
        ('BACKGROUND', (1,1),(1,1), C_PURPLE_LIGHT),
        # borders
        ('BOX',        (0,0),(0,0), 0.5, C_GREEN_BORDER),
        ('BOX',        (1,0),(1,0), 0.5, C_BLUE_BORDER),
        ('BOX',        (0,1),(0,1), 0.5, C_AMBER_BORDER),
        ('BOX',        (1,1),(1,1), 0.5, C_PURPLE_BORDER),
        ('ROUNDEDCORNERS', [4]),
        ('VALIGN',     (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING', (0,0),(-1,-1), cell_pad),
        ('BOTTOMPADDING',(0,0),(-1,-1), cell_pad),
        ('LEFTPADDING',(0,0),(-1,-1), cell_pad),
        ('RIGHTPADDING',(0,0),(-1,-1), cell_pad),
        ('INNERGRID',  (0,0),(-1,-1), 0, colors.white),
        ('LINEBELOW',  (0,0),(-1,0), 4, colors.white),   # gap between rows
        ('LINERIGHT',  (0,0),(0,-1), 4, colors.white),   # gap between cols
    ])

    return Table(data, colWidths=[col, col], style=style, hAlign='LEFT',
                 spaceBefore=0, spaceAfter=0)


def on_page(canvas, doc):
    """Footer on every page."""
    canvas.saveState()
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(C_GRAY_MID)
    canvas.drawCentredString(W/2, 18*mm,
        'YouTube Script — Web Development Roadmap Using AI  |  Confidential')
    canvas.drawRightString(W - 15*mm, 18*mm, f'Page {doc.page}')
    canvas.restoreState()


# ── Build story ───────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    '/mnt/user-data/outputs/WebDev_AI_YouTube_Script.pdf',
    pagesize=A4,
    topMargin=18*mm, bottomMargin=26*mm,
    leftMargin=15*mm, rightMargin=15*mm,
)

story = []

# ── Cover block ───────────────────────────────────────────────────────────────
story.append(Spacer(1, 4*mm))
story.append(Paragraph('YouTube Video Script', sSubtitle))
story.append(Paragraph('Web Development Roadmap Using AI', sTitle))
story.append(Spacer(1, 3*mm))

meta_data = [
    ['Video Length', '~12–15 minutes'],
    ['Total Scenes', '8 scenes'],
    ['Target Audience', 'Beginners feeling overwhelmed by web dev'],
    ['Format', 'Talking head + Screen recording + Motion graphics'],
    ['Music', 'Lo-fi / hip-hop (YouTube Audio Library — free)'],
]
meta_style = TableStyle([
    ('FONTNAME',    (0,0),(0,-1), 'Helvetica-Bold'),
    ('FONTNAME',    (1,0),(1,-1), 'Helvetica'),
    ('FONTSIZE',    (0,0),(-1,-1), 9),
    ('TEXTCOLOR',   (0,0),(0,-1), colors.HexColor('#5F5E5A')),
    ('TEXTCOLOR',   (1,0),(1,-1), C_BLACK),
    ('TOPPADDING',  (0,0),(-1,-1), 3),
    ('BOTTOMPADDING',(0,0),(-1,-1), 3),
    ('LEFTPADDING', (0,0),(-1,-1), 0),
    ('RIGHTPADDING',(0,0),(-1,-1), 8),
    ('LINEBELOW',   (0,-1),(-1,-1), 0, colors.white),
])
story.append(Table(meta_data, colWidths=[48*mm, None], style=meta_style, hAlign='LEFT'))
story.append(Spacer(1, 3*mm))

# hook box
hook_data = [[Paragraph(
    '<b>Video Concept:</b> A step-by-step roadmap showing how to learn web development in 2025 '
    'using AI tools — targeting beginners who feel overwhelmed, structured as a motivational + '
    'practical guide. Hook on the fear of being left behind; payoff is a clear, actionable path.',
    sHook)]]
hook_style = TableStyle([
    ('BACKGROUND',   (0,0),(-1,-1), C_BLUE_LIGHT),
    ('BOX',          (0,0),(-1,-1), 0.5, C_BLUE_BORDER),
    ('ROUNDEDCORNERS',[4]),
    ('TOPPADDING',   (0,0),(-1,-1), 8),
    ('BOTTOMPADDING',(0,0),(-1,-1), 8),
    ('LEFTPADDING',  (0,0),(-1,-1), 10),
    ('RIGHTPADDING', (0,0),(-1,-1), 10),
])
story.append(Table(hook_data, colWidths=[W - 30*mm], style=hook_style, hAlign='LEFT'))
story.append(Spacer(1, 4*mm))

# legend
legend_items = [
    (C_GREEN_LIGHT,  C_GREEN_MID,  'A-Roll — Talking Head (what you say on camera)'),
    (C_BLUE_LIGHT,   C_BLUE_MID,   'B-Roll — Visuals / Screen recordings / Cutaways'),
    (C_AMBER_LIGHT,  C_AMBER_MID,  'Text on Screen — Overlays, badges, callouts, CTAs'),
    (C_PURPLE_LIGHT, C_PURPLE_MID, 'Voiceover / Audio Notes — Narration & music cues'),
]
leg_data = []
for bg, border, label in legend_items:
    swatch = Table([['']], colWidths=[12], style=TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), bg),
        ('BOX',(0,0),(-1,-1),0.5,border),
        ('TOPPADDING',(0,0),(-1,-1),5),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),
    ]))
    leg_data.append([swatch, Paragraph(label, sLegendLabel)])

leg_style = TableStyle([
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(-1,-1),2),
    ('BOTTOMPADDING',(0,0),(-1,-1),2),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),10),
])
story.append(Paragraph('Legend', ParagraphStyle('leg_hd',
    fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#5F5E5A'),
    spaceAfter=4)))
story.append(Table(leg_data, colWidths=[18, None], style=leg_style, hAlign='LEFT'))
story.append(Spacer(1, 6*mm))
story.append(HRFlowable(width='100%', thickness=0.5, color=C_GRAY_MID))
story.append(Spacer(1, 4*mm))

# ── Scenes ────────────────────────────────────────────────────────────────────
for i, scene in enumerate(scenes):
    # Header bar
    hdr_data = [[
        Paragraph(f'Scene {scene["num"]}  —  {scene["title"]}', sSceneHeader),
        Paragraph(scene['timing'], sSceneTiming),
    ]]
    hdr_style = TableStyle([
        ('BACKGROUND',  (0,0),(-1,-1), colors.HexColor('#185FA5')),
        ('ROUNDEDCORNERS',[4]),
        ('TOPPADDING',  (0,0),(-1,-1), 8),
        ('BOTTOMPADDING',(0,0),(-1,-1), 8),
        ('LEFTPADDING', (0,0),(-1,-1), 12),
        ('RIGHTPADDING',(0,0),(-1,-1), 12),
        ('VALIGN',      (0,0),(-1,-1), 'MIDDLE'),
        ('ALIGN',       (1,0),(1,0), 'RIGHT'),
    ])
    hdr = Table(hdr_data, colWidths=[None, 40*mm],
                style=hdr_style, hAlign='LEFT')

    bt = block_table(scene)

    story.append(KeepTogether([hdr, Spacer(1, 3*mm), bt]))
    story.append(Spacer(1, 6*mm))

    if i == 2:   # page break after scene 3 to balance pages
        story.append(PageBreak())

# ── Recap table ───────────────────────────────────────────────────────────────
story.append(HRFlowable(width='100%', thickness=0.5, color=C_GRAY_MID))
story.append(Spacer(1, 4*mm))
story.append(Paragraph('Full Roadmap Recap', ParagraphStyle('rh',
    fontName='Helvetica-Bold', fontSize=13, textColor=C_BLACK,
    spaceAfter=6)))

recap_rows = [
    ['Stage', 'Topic', 'Est. Time (without AI)', 'Est. Time (with AI)'],
    ['Stage 1', 'HTML & CSS Foundations', '3–6 weeks', '2–4 weeks'],
    ['Stage 2', 'JavaScript Core',        '6–10 weeks','4–6 weeks'],
    ['Stage 3', 'React (Frontend Framework)','6–10 weeks','4–6 weeks'],
    ['Stage 4', 'Node.js + Databases',    '8–12 weeks','6–8 weeks'],
    ['Stage 5', 'Portfolio & Job Hunting','Ongoing',   'Ongoing'],
]
recap_style = TableStyle([
    ('BACKGROUND',  (0,0),(-1,0), colors.HexColor('#185FA5')),
    ('TEXTCOLOR',   (0,0),(-1,0), C_WHITE),
    ('FONTNAME',    (0,0),(-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',    (0,0),(-1,-1), 9),
    ('FONTNAME',    (0,1),(-1,-1), 'Helvetica'),
    ('TEXTCOLOR',   (0,1),(-1,-1), C_BLACK),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[C_GRAY_LIGHT, C_WHITE]),
    ('GRID',        (0,0),(-1,-1), 0.4, C_GRAY_MID),
    ('TOPPADDING',  (0,0),(-1,-1), 5),
    ('BOTTOMPADDING',(0,0),(-1,-1), 5),
    ('LEFTPADDING', (0,0),(-1,-1), 8),
    ('RIGHTPADDING',(0,0),(-1,-1), 8),
    ('ALIGN',       (2,0),(-1,-1), 'CENTER'),
    ('VALIGN',      (0,0),(-1,-1), 'MIDDLE'),
])

col_w = [20*mm, 65*mm, 42*mm, 42*mm]
story.append(Table(recap_rows, colWidths=col_w, style=recap_style, hAlign='LEFT'))
story.append(Spacer(1, 8*mm))

# ── Build ─────────────────────────────────────────────────────────────────────
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print('PDF created successfully.')