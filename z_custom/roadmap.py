from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus.flowables import Flowable

W, H = A4

# ── Palette ──────────────────────────────────────────────────────────────────
INDIGO   = colors.HexColor("#4338CA")
INDIGO_L = colors.HexColor("#EEF2FF")
INDIGO_M = colors.HexColor("#C7D2FE")
PURPLE   = colors.HexColor("#5B21B6")
TEAL     = colors.HexColor("#0F6E56")
TEAL_L   = colors.HexColor("#E1F5EE")
AMBER    = colors.HexColor("#854F0B")
AMBER_L  = colors.HexColor("#FAEEDA")
CORAL    = colors.HexColor("#993C1D")
CORAL_L  = colors.HexColor("#FAECE7")
BLUE     = colors.HexColor("#185FA5")
BLUE_L   = colors.HexColor("#E6F1FB")
GREEN    = colors.HexColor("#3B6D11")
GREEN_L  = colors.HexColor("#EAF3DE")
DARK     = colors.HexColor("#1E1B4B")
GRAY     = colors.HexColor("#6B7280")
GRAY_L   = colors.HexColor("#F9FAFB")
GRAY_B   = colors.HexColor("#E5E7EB")
WHITE    = colors.white

# ── Styles ───────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, parent='Normal', **kw):
    return ParagraphStyle(name, parent=base[parent], **kw)

sTitle    = S('sTitle',    'Title',   fontSize=26, textColor=DARK,   spaceAfter=4,  leading=32)
sSubtitle = S('sSubtitle',           fontSize=12, textColor=GRAY,   spaceAfter=16, leading=16)
sH1       = S('sH1',                 fontSize=16, textColor=WHITE,   spaceAfter=0,  leading=20, fontName='Helvetica-Bold')
sH2       = S('sH2',                 fontSize=13, textColor=INDIGO,  spaceBefore=14, spaceAfter=4, leading=18, fontName='Helvetica-Bold')
sH3       = S('sH3',                 fontSize=11, textColor=DARK,    spaceBefore=8,  spaceAfter=3, leading=15, fontName='Helvetica-Bold')
sBody     = S('sBody',               fontSize=9,  textColor=colors.HexColor("#374151"), spaceAfter=3, leading=14)
sBullet   = S('sBullet',             fontSize=9,  textColor=colors.HexColor("#374151"), spaceAfter=2, leading=13, leftIndent=12, firstLineIndent=-10)
sCode     = S('sCode',               fontSize=8,  textColor=INDIGO,  fontName='Courier', spaceAfter=2, leading=12)
sTag      = S('sTag',                fontSize=8,  textColor=INDIGO,  fontName='Helvetica-Bold', spaceAfter=2)
sSmall    = S('sSmall',              fontSize=8,  textColor=GRAY,    spaceAfter=2,  leading=12)
sSig      = S('sSig',                fontSize=8,  textColor=TEAL,    fontName='Helvetica-Bold', spaceAfter=2)

def bullet(txt, color=INDIGO):
    return Paragraph(f'<font color="#{color.hexval()[2:]}">&#x25CF;</font>  {txt}', sBullet)

def sp(h=4): return Spacer(1, h)
def hr(color=GRAY_B): return HRFlowable(width='100%', thickness=0.5, color=color, spaceAfter=6, spaceBefore=6)

# ── Custom Flowables ──────────────────────────────────────────────────────────
class ColorBox(Flowable):
    def __init__(self, text, bg, fg=WHITE, w=None, h=28, radius=6, subtitle=None):
        super().__init__()
        self.text = text; self.bg = bg; self.fg = fg
        self._w = w; self._h = h; self.radius = radius; self.subtitle = subtitle
    def wrap(self, aw, ah):
        self.width = self._w or aw
        self.height = self._h + (12 if self.subtitle else 0)
        return self.width, self.height
    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.roundRect(0, 0, self.width, self.height, self.radius, fill=1, stroke=0)
        c.setFillColor(self.fg)
        c.setFont('Helvetica-Bold', 11)
        ty = self.height - 18
        c.drawString(12, ty, self.text)
        if self.subtitle:
            c.setFont('Helvetica', 8)
            c.setFillColor(colors.HexColor("#A5B4FC") if self.fg == WHITE else GRAY)
            c.drawString(12, ty - 13, self.subtitle)

class Pill(Flowable):
    def __init__(self, text, bg, fg, w=None):
        super().__init__()
        self.text = text; self.bg = bg; self.fg = fg; self._w = w
    def wrap(self, aw, ah):
        self.width = self._w or (len(self.text)*5.5 + 16)
        self.height = 16
        return self.width, self.height
    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.roundRect(0, 0, self.width, self.height, 8, fill=1, stroke=0)
        c.setFillColor(self.fg)
        c.setFont('Helvetica-Bold', 7)
        c.drawCentredString(self.width/2, 4, self.text)

class SidebarCard(Flowable):
    """Card with coloured left border"""
    def __init__(self, title, items, accent=INDIGO, w=None):
        super().__init__()
        self.title = title; self.items = items; self.accent = accent; self._w = w
    def wrap(self, aw, ah):
        self.width = self._w or aw
        self.height = 18 + len(self.items)*13 + 8
        return self.width, self.height
    def draw(self):
        c = self.canv
        c.setFillColor(GRAY_L); c.setStrokeColor(GRAY_B)
        c.roundRect(0, 0, self.width, self.height, 4, fill=1, stroke=1)
        c.setFillColor(self.accent)
        c.rect(0, 0, 4, self.height, fill=1, stroke=0)
        c.setFillColor(DARK); c.setFont('Helvetica-Bold', 9)
        c.drawString(10, self.height - 14, self.title)
        c.setFont('Helvetica', 8); c.setFillColor(colors.HexColor("#374151"))
        for i, item in enumerate(self.items):
            y = self.height - 26 - i*13
            c.setFillColor(self.accent); c.circle(8, y+3, 2, fill=1, stroke=0)
            c.setFillColor(colors.HexColor("#374151"))
            c.drawString(14, y, item)

# ── Document ──────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    'C:/Users/Madhusudhan Rao/workspace/python/senior_frontend_roadmap.pdf',
    pagesize=A4,
    leftMargin=18*mm, rightMargin=18*mm,
    topMargin=16*mm, bottomMargin=16*mm,
    title='Senior Frontend Engineer Roadmap',
    author='DevFlow Roadmap'
)

story = []
add = story.append
addm = story.extend

def section_header(text, bg=INDIGO, subtitle=None):
    add(sp(10))
    add(ColorBox(text, bg=bg, subtitle=subtitle, h=32 if subtitle else 26))
    add(sp(8))

def phase_tag(text, bg=INDIGO_L, fg=INDIGO):
    return Paragraph(f'<font color="#{fg.hexval()[2:]}" size="8"><b>{text}</b></font>', sTag)

def feature_block(tag, title, desc, tag_bg=INDIGO_L, tag_fg=INDIGO):
    hex_fg = tag_fg.hexval()[2:]
    hex_bg = tag_bg.hexval()[2:]
    rows = [[
        Paragraph(f'<font color="#{hex_fg}" size="7"><b>{tag}</b></font>', sTag),
        Paragraph(f'<b>{title}</b><br/><font size="8" color="#6B7280">{desc}</font>', sBody)
    ]]
    t = Table(rows, colWidths=[18*mm, None])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(0,0), tag_bg),
        ('BACKGROUND', (1,0),(1,0), WHITE),
        ('BOX', (0,0),(-1,-1), 0.5, GRAY_B),
        ('INNERGRID', (0,0),(-1,-1), 0.5, GRAY_B),
        ('VALIGN', (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING', (0,0),(-1,-1), 6),
        ('BOTTOMPADDING', (0,0),(-1,-1), 6),
        ('LEFTPADDING', (0,0),(-1,-1), 6),
        ('RIGHTPADDING', (0,0),(-1,-1), 6),
        ('ROUNDEDCORNERS', [4]),
    ]))
    add(t); add(sp(5))

def two_col(left_items, right_items, left_title, right_title, accent=INDIGO):
    lw = rw = (W - 36*mm - 6*mm) / 2
    left_paras  = [Paragraph(f'<b><font size="9">{left_title}</font></b>', sH3)]  + [bullet(i) for i in left_items]
    right_paras = [Paragraph(f'<b><font size="9">{right_title}</font></b>', sH3)] + [bullet(i) for i in right_items]
    data = [[left_paras, right_paras]]
    t = Table(data, colWidths=[lw, rw])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), GRAY_L),
        ('BOX', (0,0),(-1,-1), 0.5, GRAY_B),
        ('INNERGRID', (0,0),(-1,-1), 0.5, GRAY_B),
        ('VALIGN', (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING', (0,0),(-1,-1), 8),
        ('BOTTOMPADDING', (0,0),(-1,-1), 8),
        ('LEFTPADDING', (0,0),(-1,-1), 8),
        ('RIGHTPADDING', (0,0),(-1,-1), 8),
    ]))
    add(t); add(sp(6))

def dsa_block(items):
    rows = [[Paragraph(f'<font color="#4338CA" size="8"><b>DSA Focus</b></font>', sTag), '']]
    for item in items:
        rows.append([Paragraph(f'<font color="#4338CA">&#x25B6;</font>', sBody), Paragraph(item, sBody)])
    t = Table(rows, colWidths=[24*mm, None])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,0), INDIGO_L),
        ('BACKGROUND', (0,1),(-1,-1), GRAY_L),
        ('BOX', (0,0),(-1,-1), 0.5, INDIGO_M),
        ('INNERGRID', (0,0),(-1,-1), 0.5, GRAY_B),
        ('SPAN', (0,0),(1,0)),
        ('TOPPADDING', (0,0),(-1,-1), 4),
        ('BOTTOMPADDING', (0,0),(-1,-1), 4),
        ('LEFTPADDING', (0,0),(-1,-1), 6),
    ]))
    add(t); add(sp(6))

def highlight(text, accent=INDIGO):
    data = [[Paragraph(text, sBody)]]
    t = Table(data, colWidths=[W - 36*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), INDIGO_L),
        ('LEFTPADDING', (0,0),(-1,-1), 10),
        ('RIGHTPADDING', (0,0),(-1,-1), 10),
        ('TOPPADDING', (0,0),(-1,-1), 8),
        ('BOTTOMPADDING', (0,0),(-1,-1), 8),
        ('LINEBEFORE', (0,0),(0,-1), 3, accent),
    ]))
    add(t); add(sp(6))

# ═══════════════════════════════════════════════════════════════════════════════
#  COVER PAGE
# ═══════════════════════════════════════════════════════════════════════════════
add(sp(30))
add(ColorBox('SENIOR FRONTEND ENGINEER', bg=INDIGO, h=44, radius=8))
add(sp(4))
add(Paragraph('Transformation Roadmap', ParagraphStyle('cover_sub', fontSize=22, textColor=DARK, leading=28, fontName='Helvetica-Bold')))
add(sp(6))
add(Paragraph('3 YOE → Senior-level thinking · 20 weeks · 15+ LPA', sSubtitle))
add(hr())
add(sp(8))

# Project banner
data = [[
    Paragraph('<b>The Project: DevFlow</b>', ParagraphStyle('pb', fontSize=13, textColor=WHITE, fontName='Helvetica-Bold')),
    ''
],[
    Paragraph('A developer productivity platform — task boards, snippet manager, real-time notifications, analytics dashboard, command palette, offline mode. Every concept learned becomes a shipped feature.', ParagraphStyle('pd', fontSize=9, textColor=colors.HexColor("#C7D2FE"), leading=14)),
    ''
]]
t = Table(data, colWidths=[W - 36*mm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0),(-1,-1), DARK),
    ('TOPPADDING', (0,0),(-1,-1), 10),
    ('BOTTOMPADDING', (0,0),(-1,-1), 10),
    ('LEFTPADDING', (0,0),(-1,-1), 14),
    ('RIGHTPADDING', (0,0),(-1,-1), 14),
    ('ROUNDEDCORNERS', [8]),
]))
add(t); add(sp(14))

# Tech stack pills as table
tech = ['React 19','TypeScript','Zustand','React Query','Vite','WebSockets','MSW','Playwright','Storybook','Recharts']
pill_data = [[Paragraph(t_, ParagraphStyle('tp', fontSize=8, textColor=INDIGO, fontName='Helvetica-Bold', alignment=TA_CENTER)) for t_ in tech[:5]],
             [Paragraph(t_, ParagraphStyle('tp', fontSize=8, textColor=INDIGO, fontName='Helvetica-Bold', alignment=TA_CENTER)) for t_ in tech[5:]]]
pt = Table(pill_data)
pt.setStyle(TableStyle([
    ('BACKGROUND', (0,0),(-1,-1), INDIGO_L),
    ('BOX', (0,0),(-1,-1), 0.5, INDIGO_M),
    ('INNERGRID', (0,0),(-1,-1), 0.5, INDIGO_M),
    ('TOPPADDING', (0,0),(-1,-1), 5),
    ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ('ALIGN', (0,0),(-1,-1), 'CENTER'),
]))
add(pt); add(sp(16))

# Timeline overview table
add(Paragraph('<b>20-Week Timeline at a Glance</b>', sH2))
tl_data = [
    ['Phase', 'Weeks', 'Focus', 'Key Deliverable'],
    ['1 — Foundation',   '1–3',   'JS/TS mastery, tooling, project setup',      'Auth + layout shell'],
    ['2 — React Depth',  '4–6',   'Fiber internals, state arch, custom hooks',  'Kanban + command palette'],
    ['3 — Patterns',     '7–9',   'Observer, Command, Strategy, Compound',      'Notification system + Storybook'],
    ['4 — Network/Cache','10–13', 'HTTP, caching, WebSocket, API design',       'Typed API client + offline mode'],
    ['5 — Sys Design',   '14–16', 'Architecture, performance, testing',         '90+ Lighthouse + CI/CD'],
    ['6 — Ship & Hunt',  '17–20', 'Launch, resume, interviews, offers',         '15+ LPA offer'],
]
tl = Table(tl_data, colWidths=[32*mm, 14*mm, 70*mm, 40*mm])
tl.setStyle(TableStyle([
    ('BACKGROUND', (0,0),(-1,0), INDIGO),
    ('TEXTCOLOR', (0,0),(-1,0), WHITE),
    ('FONTNAME', (0,0),(-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0),(-1,0), 8),
    ('BACKGROUND', (0,1),(-1,1), INDIGO_L),
    ('BACKGROUND', (0,2),(-1,2), GRAY_L),
    ('BACKGROUND', (0,3),(-1,3), TEAL_L),
    ('BACKGROUND', (0,4),(-1,4), GRAY_L),
    ('BACKGROUND', (0,5),(-1,5), AMBER_L),
    ('BACKGROUND', (0,6),(-1,6), GREEN_L),
    ('FONTSIZE', (0,1),(-1,-1), 8),
    ('BOX', (0,0),(-1,-1), 0.5, GRAY_B),
    ('INNERGRID', (0,0),(-1,-1), 0.5, GRAY_B),
    ('TOPPADDING', (0,0),(-1,-1), 5),
    ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ('LEFTPADDING', (0,0),(-1,-1), 7),
]))
add(tl)
add(sp(12))
highlight('<b>Daily habit:</b> 1 DSA problem (morning) · 1 concept deep-dive · 1–2 hrs building DevFlow · 1 system design sketch per week')

add(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
#  PHASE 1
# ═══════════════════════════════════════════════════════════════════════════════
section_header('PHASE 1 — Foundation & TypeScript Mastery', bg=DARK, subtitle='Weeks 1–3 · Senior engineers write code that is impossible to misuse')

two_col(
    ['Mapped types: { [K in keyof T]: ... }', 'Conditional types + infer keyword',
     'Template literal types for API routes', 'Discriminated unions for state machines',
     'Module augmentation, declaration merging', 'Variance: covariance vs contravariance'],
    ['V8 hidden classes & inline caching', 'Call stack, heap, event loop in detail',
     'Microtask vs macrotask queue — execution order', 'Memory leaks in SPAs — closures, listeners',
     'Garbage collection — mark & sweep', 'WeakMap/WeakRef for leak prevention'],
    'TypeScript — compiler level', 'JS Engine internals'
)

two_col(
    ['Vite: manual chunks, rollup config, aliases', 'ESLint: custom rules, import ordering',
     'Husky + commitlint + lint-staged', 'GitHub Actions: lint, type-check, test, deploy'],
    ['Feature-based folder structure', 'Barrel exports with re-export control',
     'Dependency direction rules (no circular)', 'Shared vs feature-local code boundaries'],
    'Senior-grade tooling', 'Project architecture'
)

add(Paragraph('<b>DevFlow Features to Build</b>', sH2))
feature_block('Feature 1', 'Scaffolding + design token system',
    'Vite + React 19 + TS strict mode. Feature folders. Token-based CSS variables. Base components (Button, Input, Badge) with full generic props. CI pipeline on GitHub Actions.')
feature_block('Feature 2', 'Auth system — typed state machine',
    'Discriminated union AuthState: Unauthenticated | Authenticating | Authenticated | Error. JWT + refresh token rotation. Route guards via React Router v6 loaders. MSW mocks.')
feature_block('Feature 3', 'Layout shell — compound component',
    'Sidebar + topbar as compound components. Collapsible with localStorage. Dark mode via CSS custom properties. Full keyboard nav (a11y). Teaches component composition patterns early.')

dsa_block([
    'Arrays & hashmaps — Two Sum, Group Anagrams, Top K Frequent Elements',
    'Strings — Longest Substring Without Repeat, Valid Palindrome, Anagram Check',
    'Stack — Valid Parentheses, Min Stack, Daily Temperatures'
])

add(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
#  PHASE 2
# ═══════════════════════════════════════════════════════════════════════════════
section_header('PHASE 2 — React Internals & State Architecture', bg=colors.HexColor("#5B21B6"), subtitle='Weeks 4–6 · Go past the API surface. Understand how React decides what to re-render')

two_col(
    ['Fiber nodes: type, key, pendingProps, memoizedState', 'Work loop: beginWork → completeWork → commit',
     'Lanes & priority scheduling', 'Double buffering: current vs workInProgress tree',
     'When does React bail out of re-renders?'],
    ['useTransition — non-blocking state updates', 'useDeferredValue — stale-while-revalidate UI',
     'Suspense boundaries + streaming SSR', 'React 19: Actions, useOptimistic',
     'Error boundaries — where to place them'],
    'React Fiber & reconciler', 'Concurrent features'
)

two_col(
    ['Server state vs client state — clear separation', 'React Query: stale time, gc time, invalidation keys',
     'Zustand: slices, devtools, persist middleware', 'Optimistic updates with rollback on error',
     'Selector memoization — avoid over-subscribing'],
    ['Stale closure problem — when refs beat state', 'useEvent pattern (stable callback identity)',
     'Composing hooks — single responsibility', 'Hook testing with renderHook'],
    'State architecture at scale', 'Custom hooks — advanced'
)

add(Paragraph('<b>DevFlow Features to Build</b>', sH2))
feature_block('Feature 4', 'Kanban board — drag, drop, undo/redo',
    'Full kanban with @dnd-kit. Zustand for board state with undo/redo via Command pattern (history stack). Optimistic updates via React Query. useTransition for filter animations. Your first design pattern in production.')
feature_block('Feature 5', 'Command palette — Cmd+K global search',
    'Portal-rendered command palette. Fuzzy search with fuse.js. useDeferredValue keeps input responsive. Custom useHotkeys hook with keyboard shortcut registry (Observer pattern). Result virtualization.')
feature_block('Feature 6', 'Code snippet manager',
    'CRUD with Monaco Editor (syntax highlight). All data via React Query with optimistic adds. Custom useSnippets hook encapsulates all logic. Tag-based filtering. Demonstrates clean hook extraction seniors expect.')

dsa_block([
    'Binary search — Search Rotated Array, Find Peak Element, Koko Eating Bananas',
    'Sliding window — Longest Repeating Character, Permutation in String',
    'Two pointers — 3Sum, Container With Most Water, Trapping Rain Water'
])

add(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
#  PHASE 3
# ═══════════════════════════════════════════════════════════════════════════════
section_header('PHASE 3 — Design Patterns in Production', bg=TEAL, subtitle='Weeks 7–9 · The biggest differentiator between mid and senior — reach for the right pattern naturally')

add(Paragraph('<b>Patterns to Master — with Real Frontend Implementations</b>', sH2))

patterns = [
    ('Observer', INDIGO, 'Pub/sub event bus for cross-feature communication. Custom typed EventEmitter. React context as observable store. Cleanup: unsubscribe in useEffect return.\n→ DevFlow: real-time notification system'),
    ('Command', PURPLE, 'Encapsulate actions as objects with execute/undo. History stack for undo/redo. Macro commands for batch ops.\n→ DevFlow: kanban undo/redo + bulk task actions'),
    ('Compound Component', TEAL, 'Implicit state sharing via context. Flexible composition without prop drilling. Controlled vs uncontrolled variants.\n→ DevFlow: Modal, Tabs, Dropdown components'),
    ('Strategy', AMBER, 'Swappable algorithms at runtime. Sort/filter strategies for lists. Different validation rules per form type.\n→ DevFlow: pluggable task filter/sort engine'),
    ('Proxy & Decorator', CORAL, 'JS Proxy for reactive objects. API client decorator: logging, retry, auth. HOC as decorator in React.\n→ DevFlow: typed API client with retry + auth decorator'),
    ('Factory', BLUE, 'Abstract object creation from consumers. Component factory for dynamic rendering. Widget registry pattern.\n→ DevFlow: dashboard widget registry'),
]

for name, color, desc in patterns:
    lines = desc.split('\n')
    main_desc = lines[0]
    impl = lines[1] if len(lines) > 1 else ''
    hex_c = color.hexval()[2:]
    data = [[
        Paragraph(f'<b>{name}</b>', ParagraphStyle('pn', fontSize=10, textColor=WHITE, fontName='Helvetica-Bold')),
        [Paragraph(main_desc, sBody), Paragraph(f'<font color="#{hex_c}"><b>{impl}</b></font>', sSmall)]
    ]]
    t = Table(data, colWidths=[26*mm, None])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(0,0), color),
        ('BACKGROUND', (1,0),(1,0), GRAY_L),
        ('BOX', (0,0),(-1,-1), 0.5, GRAY_B),
        ('INNERGRID', (0,0),(-1,-1), 0.5, GRAY_B),
        ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0),(-1,-1), 7),
        ('BOTTOMPADDING', (0,0),(-1,-1), 7),
        ('LEFTPADDING', (0,0),(-1,-1), 8),
    ]))
    add(t); add(sp(4))

add(sp(6))
add(Paragraph('<b>DevFlow Features to Build</b>', sH2))
feature_block('Feature 7', 'Real-time notifications — Observer + WebSocket',
    'Custom typed EventEmitter as notification bus. WebSocket hook with reconnect strategy (exponential backoff). Toast system as compound component. Notification bell with unread count.', tag_bg=TEAL_L, tag_fg=TEAL)
feature_block('Feature 8', 'Pluggable filter engine — Strategy pattern',
    'Task filters as swappable strategy objects. Filter composition (AND/OR). URL-sync state so filters persist on share. Sorting strategies. A mini query engine showing architectural thinking.', tag_bg=TEAL_L, tag_fg=TEAL)
feature_block('Feature 9', 'Storybook component library',
    'Extract all shared components into documented Storybook. Write stories for every state. Deploy to Chromatic. This is your design system — link it in your resume and explain compound component decisions in interviews.', tag_bg=TEAL_L, tag_fg=TEAL)

dsa_block([
    'Trees — Max Depth, Level Order, Lowest Common Ancestor, Serialize/Deserialize',
    'BFS/DFS — Number of Islands, Word Ladder, Course Schedule',
    'Recursion + backtracking — Subsets, Permutations, N-Queens'
])

add(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
#  PHASE 4
# ═══════════════════════════════════════════════════════════════════════════════
section_header('PHASE 4 — Networking, APIs & Caching', bg=colors.HexColor("#7C2D12"), subtitle='Weeks 10–13 · The layer most frontend devs treat as a black box. Seniors own it.')

add(Paragraph('<b>What to Learn — Deeply</b>', sH2))

two_col(
    ['HTTP/1.1 vs HTTP/2 vs HTTP/3 — multiplexing, QUIC', 'Request lifecycle: DNS → TCP → TLS → HTTP',
     'Headers: Cache-Control, ETag, If-None-Match, Vary', 'CORS — preflight, simple requests, credentials',
     'Content negotiation, compression (gzip, br)', 'HOL blocking, connection keep-alive, pipelining'],
    ['Browser cache: memory cache vs disk cache', 'Cache-Control: max-age, s-maxage, stale-while-revalidate',
     'React Query: staleTime, gcTime, cache keys', 'Service Worker: cache-first, network-first, SWR strategies',
     'CDN caching — edge cache, cache busting with hashes', 'Cache invalidation — the hardest problem in CS'],
    'HTTP deep dive', 'Caching hierarchy'
)

two_col(
    ['WebSocket — handshake, frames, ping/pong', 'SSE — when to use over WebSocket',
     'Long polling — fallback pattern', 'Reconnect strategies — exponential backoff + jitter',
     'Message ordering, deduplication, idempotency'],
    ['REST: resource modeling, versioning, HATEOAS', 'GraphQL: queries, mutations, N+1 problem',
     'tRPC — type-safe end-to-end APIs', 'API client patterns: interceptors, fetch wrappers',
     'Rate limiting, retry with backoff, circuit breaker'],
    'Real-time protocols', 'API design & patterns'
)

# Caching hierarchy visual table
add(Paragraph('<b>The Caching Hierarchy — L1 to L5</b>', sH2))
cache_data = [
    ['Layer', 'Mechanism', 'Scope', 'Key Concept'],
    ['L1 Memory', 'Browser in-memory', 'Session only', 'Fastest — no headers needed, back/fwd nav'],
    ['L2 Disk', 'Cache-Control headers', 'Configurable TTL', 'ETag + If-None-Match for conditional GETs'],
    ['L3 Service Worker', 'Cache Storage API', 'Offline capable', 'cache-first / network-first strategies'],
    ['L4 React Query', 'In-memory JS cache', 'App lifetime', 'staleTime + gcTime + invalidation keys'],
    ['L5 CDN Edge', 'CDN servers', 'Global', 's-maxage, Surrogate-Key, content hash filenames'],
]
ct = Table(cache_data, colWidths=[28*mm, 36*mm, 34*mm, None])
ct.setStyle(TableStyle([
    ('BACKGROUND', (0,0),(-1,0), AMBER),
    ('TEXTCOLOR', (0,0),(-1,0), WHITE),
    ('FONTNAME', (0,0),(-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0),(-1,-1), 8),
    ('BACKGROUND', (0,1),(-1,1), INDIGO_L),
    ('BACKGROUND', (0,2),(-1,2), GRAY_L),
    ('BACKGROUND', (0,3),(-1,3), TEAL_L),
    ('BACKGROUND', (0,4),(-1,4), GRAY_L),
    ('BACKGROUND', (0,5),(-1,5), AMBER_L),
    ('BOX', (0,0),(-1,-1), 0.5, GRAY_B),
    ('INNERGRID', (0,0),(-1,-1), 0.5, GRAY_B),
    ('TOPPADDING', (0,0),(-1,-1), 5), ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ('LEFTPADDING', (0,0),(-1,-1), 7),
]))
add(ct); add(sp(8))

# Real-time protocol comparison
add(Paragraph('<b>Real-time Protocol Comparison</b>', sH2))
rt_data = [
    ['', 'WebSocket', 'Server-Sent Events (SSE)', 'Long Polling'],
    ['Direction', 'Full-duplex', 'Server → Client only', 'Server → Client'],
    ['Reconnect', 'Manual (write yourself)', 'Automatic built-in', 'Manual'],
    ['Scalability', 'Harder (sticky sessions)', 'Easy (HTTP/2)', 'High server load'],
    ['Use for', 'Chat, collab, games', 'Notifications, feeds', 'Legacy fallback'],
]
rtt = Table(rt_data, colWidths=[28*mm, 48*mm, 60*mm, 36*mm])
rtt.setStyle(TableStyle([
    ('BACKGROUND', (0,0),(-1,0), DARK),
    ('TEXTCOLOR', (0,0),(-1,0), WHITE),
    ('FONTNAME', (0,0),(-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1),(0,-1), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0),(-1,-1), 8),
    ('BACKGROUND', (0,1),(0,-1), GRAY_L),
    ('BOX', (0,0),(-1,-1), 0.5, GRAY_B),
    ('INNERGRID', (0,0),(-1,-1), 0.5, GRAY_B),
    ('TOPPADDING', (0,0),(-1,-1), 5), ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ('LEFTPADDING', (0,0),(-1,-1), 7),
]))
add(rtt); add(sp(8))

add(Paragraph('<b>DevFlow Features to Build</b>', sH2))
feature_block('Feature 10', 'Typed API client — Proxy + Decorator pattern',
    'Build a fully-typed HTTP client using JS Proxy. Decorator layers: auth (inject token), retry (exponential backoff), logger, error normalizer. The Proxy + Decorator patterns shipped as one production module.', tag_bg=AMBER_L, tag_fg=AMBER)
feature_block('Feature 11', 'Offline mode + service worker cache',
    'Service worker with network-first for API, cache-first for assets. IndexedDB for offline task queue (sync on reconnect). Online/offline indicator. Background sync on reconnect. Shows you understand the full browser stack.', tag_bg=AMBER_L, tag_fg=AMBER)
feature_block('Feature 12', 'Analytics dashboard — WebWorker + streaming data',
    'Heavy chart computations offloaded to Web Worker (no jank). Recharts for line, bar, pie. Streaming data via SSE for live metrics. Date range picker. CSV export. Performance at a browser-architecture level.', tag_bg=AMBER_L, tag_fg=AMBER)
feature_block('Feature 13', 'Smart caching layer — stale-while-revalidate',
    'Implement stale-while-revalidate at the app level. React Query fine-tuning per resource type (tasks: 30s stale, users: 5min stale). Cache invalidation on mutations. Document decisions in README — this is system design thinking.', tag_bg=AMBER_L, tag_fg=AMBER)

dsa_block([
    'Dynamic programming — Climbing Stairs, Coin Change, Longest Common Subsequence, Edit Distance',
    'Heaps / priority queues — Top K Elements, Kth Largest, Find Median from Stream',
    'Intervals — Merge Intervals, Meeting Rooms I & II, Insert Interval'
])

add(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
#  PHASE 5
# ═══════════════════════════════════════════════════════════════════════════════
section_header('PHASE 5 — System Design & Performance Engineering', bg=BLUE, subtitle='Weeks 14–16 · Where offers are won and lost. Senior = defensible tradeoffs + systems thinking')

add(Paragraph('<b>Frontend System Design — The Full Playbook</b>', sH2))

add(Paragraph('<b>The Answer Framework — Use Every Time</b>', sH3))
fw_data = [
    ['Step', 'What to cover', 'Time'],
    ['1. Requirements', 'Functional (what must it do?) + Non-functional (scale, perf, a11y, offline?). State what is out of scope explicitly. Clarify user count, device targets, latency budget.', '5 min'],
    ['2. Architecture', 'Component breakdown — draw the tree. Data flow — where does state live? API contracts — what does frontend need? Rendering strategy — CSR/SSR/SSG — justify it.', '10 min'],
    ['3. Deep dives', 'Caching strategy per resource. Real-time: WebSocket vs SSE vs polling. Performance: Core Web Vitals targets. Error handling + loading states.', '10 min'],
    ['4. Tradeoffs', 'What did you choose and why? What did you sacrifice? What would you do at 10x scale? Accessibility, i18n, security.', '5 min'],
]
fwt = Table(fw_data, colWidths=[35*mm, None, 18*mm])
fwt.setStyle(TableStyle([
    ('BACKGROUND', (0,0),(-1,0), BLUE),
    ('TEXTCOLOR', (0,0),(-1,0), WHITE),
    ('FONTNAME', (0,0),(-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1),(0,-1), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0),(-1,-1), 8),
    ('BACKGROUND', (0,1),(0,-1), BLUE_L),
    ('BOX', (0,0),(-1,-1), 0.5, GRAY_B),
    ('INNERGRID', (0,0),(-1,-1), 0.5, GRAY_B),
    ('VALIGN', (0,0),(-1,-1), 'TOP'),
    ('TOPPADDING', (0,0),(-1,-1), 6), ('BOTTOMPADDING', (0,0),(-1,-1), 6),
    ('LEFTPADDING', (0,0),(-1,-1), 8),
]))
add(fwt); add(sp(8))

add(Paragraph('<b>Must-Practice System Design Questions</b>', sH2))
sd_questions = [
    ('Classic', 'Design an autocomplete / typeahead component', 'Debounce, client vs server search, caching recent results, keyboard nav, ARIA, cancel in-flight requests, 1M users.'),
    ('Classic', 'Design a real-time collaborative doc editor', 'OT vs CRDT, WebSocket architecture, presence indicators, cursor sync, offline edit queue, conflict resolution.'),
    ('Classic', 'Design a design system / component library', 'Token architecture, semver, breaking change policy, Storybook, a11y guarantees, theming API, tree-shakeable exports.'),
    ('Advanced', 'Design an infinite scroll / virtualized feed', 'IntersectionObserver vs scroll events, react-virtual windowing, bi-directional scroll, data prefetching, cache eviction.'),
    ('Advanced', 'Design a file upload system', 'Chunked uploads, resumable uploads (TUS protocol), progress tracking, parallel chunks, retry, client-side validation.'),
    ('Senior', 'Design a micro-frontend platform', 'Module Federation, shared vs isolated deps, routing, shared auth, cross-MFE communication, independent deployment.'),
]
for level, q, desc in sd_questions:
    bg = INDIGO_L if level == 'Classic' else TEAL_L if level == 'Advanced' else AMBER_L
    fg = INDIGO if level == 'Classic' else TEAL if level == 'Advanced' else AMBER
    feature_block(level, q, desc, tag_bg=bg, tag_fg=fg)

add(Paragraph('<b>Architecture Topics to Study</b>', sH2))
two_col(
    ['Atomic design: atoms → molecules → organisms → pages', 'Feature boundaries — what belongs where',
     'Shared vs domain-specific components', 'Component versioning in a design system'],
    ['Module Federation with Vite/Webpack', 'Shared dependencies strategy',
     'Routing across micro-frontends', 'When NOT to use micro-frontends'],
    'Component architecture', 'Micro-frontend architecture'
)

two_col(
    ['CSR vs SSR vs SSG vs ISR — tradeoffs per use case', 'Streaming SSR with Suspense',
     'React Server Components — mental model', 'Hydration — full, partial, island architecture'],
    ['Feature flags — gradual rollout, A/B testing', 'Error boundaries + Sentry integration',
     'Monitoring: real user metrics (RUM)', 'Rollback strategies — versioned deployments'],
    'Rendering strategies', 'Scale & reliability'
)

add(Paragraph('<b>DevFlow Features to Build</b>', sH2))
feature_block('Feature 14', 'Performance engineering sprint',
    'Run Lighthouse. Document before scores. Ship: route-level code splitting, react-virtual for task lists, image lazy loading, font preloading, memoized Zustand selectors, Vite manual chunks. Target: LCP <2s, INP <200ms, 90+ Lighthouse. Write a blog post about the case study.', tag_bg=BLUE_L, tag_fg=BLUE)
feature_block('Feature 15', 'Full test suite + CI/CD pipeline',
    'RTL unit tests for all components with MSW mocking. Playwright E2E: login, create task, drag card, search, offline mode. GitHub Actions: lint → typecheck → unit → E2E → deploy to Vercel. 80%+ coverage badge. Preview deploys on every PR.', tag_bg=BLUE_L, tag_fg=BLUE)

dsa_block([
    'Graphs — Dijkstra\'s, topological sort, detect cycle, word ladder',
    'Tries — implement Trie, word search, autocomplete design',
    'Bit manipulation — Single Number, Counting Bits, Reverse Bits'
])

add(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
#  PHASE 6
# ═══════════════════════════════════════════════════════════════════════════════
section_header('PHASE 6 — Ship, Polish & Land the Offer', bg=GREEN, subtitle='Weeks 17–20 · DevFlow is live. Resume is a weapon. Offer by week 20.')

add(Paragraph('<b>Ship DevFlow like a Senior Engineer</b>', sH2))

prod_data = [
    ['Production Checklist', 'Content to Publish'],
    [
        '\n'.join([
            '✓  Deployed on Vercel with custom domain',
            '✓  CSP headers, security audit passed',
            '✓  Sentry error tracking integrated',
            '✓  90+ Lighthouse, WCAG AA accessibility',
            '✓  Storybook deployed to Chromatic',
            '✓  80%+ test coverage badge on README',
        ]),
        '\n'.join([
            '✓  README: architecture decisions, tech choices, screenshots',
            '✓  Blog 1: "Real-time kanban with WebSockets & optimistic updates"',
            '✓  Blog 2: "From 54 to 94 — a Lighthouse case study"',
            '✓  Blog 3: "Design patterns I used in production React"',
            '✓  LinkedIn: post 1 engineering insight per week',
        ])
    ]
]
pt2 = Table(prod_data, colWidths=[(W-36*mm)/2, (W-36*mm)/2])
pt2.setStyle(TableStyle([
    ('BACKGROUND', (0,0),(-1,0), GREEN),
    ('TEXTCOLOR', (0,0),(-1,0), WHITE),
    ('FONTNAME', (0,0),(-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0),(-1,-1), 8),
    ('BACKGROUND', (0,1),(-1,1), GREEN_L),
    ('BOX', (0,0),(-1,-1), 0.5, GRAY_B),
    ('INNERGRID', (0,0),(-1,-1), 0.5, GRAY_B),
    ('VALIGN', (0,0),(-1,-1), 'TOP'),
    ('TOPPADDING', (0,0),(-1,-1), 8), ('BOTTOMPADDING', (0,0),(-1,-1), 8),
    ('LEFTPADDING', (0,0),(-1,-1), 10),
]))
add(pt2); add(sp(10))

add(Paragraph('<b>Resume — Write Like a Senior Engineer</b>', sH2))
resume_pairs = [
    ('Built kanban board with React and drag and drop',
     'Architected real-time kanban with Command-pattern undo/redo, optimistic updates, and WebSocket sync — zero data loss on reconnect'),
    ('Improved app performance',
     'Drove Lighthouse score from 54 → 94: route splitting, list virtualization (react-virtual), Web Worker offload for chart computation — LCP dropped from 4.1s to 1.7s'),
    ('Used design patterns in the project',
     'Implemented Observer, Command, Strategy, and Proxy patterns to decouple feature modules — enabled independent feature shipping without merge conflicts'),
]
for bad, good in resume_pairs:
    rb_data = [[
        Paragraph(f'<font color="#A32D2D"><b>✗</b></font>  {bad}', sBody),
        Paragraph(f'<font color="#3B6D11"><b>✓</b></font>  {good}', sBody),
    ]]
    rt2 = Table(rb_data, colWidths=[(W-36*mm)/2]*2)
    rt2.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(0,0), colors.HexColor("#FEF2F2")),
        ('BACKGROUND', (1,0),(1,0), GREEN_L),
        ('BOX', (0,0),(-1,-1), 0.5, GRAY_B),
        ('INNERGRID', (0,0),(-1,-1), 0.5, GRAY_B),
        ('VALIGN', (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING', (0,0),(-1,-1), 7), ('BOTTOMPADDING', (0,0),(-1,-1), 7),
        ('LEFTPADDING', (0,0),(-1,-1), 8),
    ]))
    add(rt2); add(sp(4))

add(sp(8))
add(Paragraph('<b>Where to Apply at 15+ LPA</b>', sH2))
target_data = [
    ['Company Type', 'Examples', 'Range', 'Strategy'],
    ['Product startups (B/C)', 'Razorpay, Groww, CRED, Zepto, Slice', '18–30 LPA', 'Skill > tenure. Apply boldly.'],
    ['Mid-size product cos', 'Postman, Chargebee, Freshworks, BrowserStack', '15–22 LPA', 'More structured, good first switch.'],
    ['Remote / global', 'Toptal, arc.dev, Deel, Lemon.io, Andela', '$40–80K USD', 'Best ROI — dollar salary in India.'],
    ['Big tech adjacent', 'Google, Microsoft, Atlassian India', '25–50 LPA', 'Need strong DSA. Apply in parallel.'],
]
tgt = Table(target_data, colWidths=[38*mm, 64*mm, 28*mm, None])
tgt.setStyle(TableStyle([
    ('BACKGROUND', (0,0),(-1,0), DARK),
    ('TEXTCOLOR', (0,0),(-1,0), WHITE),
    ('FONTNAME', (0,0),(-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1),(0,-1), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0),(-1,-1), 8),
    ('BACKGROUND', (0,1),(0,-1), GRAY_L),
    ('BOX', (0,0),(-1,-1), 0.5, GRAY_B),
    ('INNERGRID', (0,0),(-1,-1), 0.5, GRAY_B),
    ('TOPPADDING', (0,0),(-1,-1), 5), ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ('LEFTPADDING', (0,0),(-1,-1), 7),
]))
add(tgt); add(sp(10))

dsa_block([
    'Full revision of all Neetcode Blind 75 — aim for 60+ solved',
    'Timed practice: mediums in under 20 min, identify pattern in first 2 min',
    'Talk through solution out loud — interviewers evaluate communication equally'
])

add(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
#  RESOURCES
# ═══════════════════════════════════════════════════════════════════════════════
section_header('RESOURCES & QUICK REFERENCE', bg=DARK)

add(Paragraph('<b>Best Learning Resources</b>', sH2))
res_data = [
    ['Area', 'Resource', 'Why'],
    ['JS/TS Deep', 'javascript.info + You Don\'t Know JS (free on GitHub)', 'Best free JS deep-dive available'],
    ['React Internals', 'react.dev + Nadia Makarevich\'s blog', 'Fiber, hooks, patterns explained clearly'],
    ['System Design', 'greatfrontend.com + frontendinterviewhandbook.com', 'Frontend-specific design questions'],
    ['DSA', 'Neetcode.io roadmap + Leetcode (sorted by frequency)', 'Structured, pattern-based approach'],
    ['Performance', 'web.dev + Harry Roberts\'s blog + Chrome DevTools docs', 'Google\'s own performance guidance'],
    ['TypeScript', 'TypeScript Deep Dive (basarat.gitbook.io)', 'Free, comprehensive, practical'],
    ['Mock Interviews', 'Pramp + Exponent', 'Practice with real people, get feedback'],
    ['Patterns', 'Patterns.dev (free book)', 'React patterns with real examples'],
]
rt3 = Table(res_data, colWidths=[36*mm, 78*mm, None])
rt3.setStyle(TableStyle([
    ('BACKGROUND', (0,0),(-1,0), INDIGO),
    ('TEXTCOLOR', (0,0),(-1,0), WHITE),
    ('FONTNAME', (0,0),(-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1),(0,-1), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0),(-1,-1), 8),
    ('BACKGROUND', (0,1),(0,-1), GRAY_L),
    ('ROWBACKGROUNDS', (0,1),(-1,-1), [WHITE, GRAY_L]),
    ('BOX', (0,0),(-1,-1), 0.5, GRAY_B),
    ('INNERGRID', (0,0),(-1,-1), 0.5, GRAY_B),
    ('TOPPADDING', (0,0),(-1,-1), 5), ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ('LEFTPADDING', (0,0),(-1,-1), 7),
]))
add(rt3); add(sp(10))

add(Paragraph('<b>The Senior Mindset — What Interviewers Are Actually Testing</b>', sH2))
mindset = [
    ('Junior says', 'Senior says'),
    ('"I used React Query for data fetching."',
     '"I chose React Query because we have a mix of server and client state. For server state, I set staleTime based on how frequently each resource changes — tasks at 30s, user profiles at 5 minutes. Cache invalidation happens on mutations. For real-time data like notifications I use WebSocket and bypass the cache layer entirely."'),
    ('"I implemented a design pattern."',
     '"I reached for the Command pattern for undo/redo because each user action needed to be reversible. Each command is a plain object with execute and undo methods. The history stack is capped at 50 to avoid memory growth. Macro commands batch related operations so users can undo a whole drag-drop sequence as one action."'),
    ('"I improved performance."',
     '"I profiled with React DevTools and Chrome Lighthouse. The task list was causing layout thrash on every scroll. I switched to react-virtual to only render visible items. Separately, I identified that our analytics computation was blocking the main thread — moved it to a Web Worker. LCP dropped from 4.1s to 1.7s."'),
]
for bad, good in mindset[1:]:
    md_data = [[
        Paragraph(f'<font color="#A32D2D"><b>Junior:</b></font> <i>{bad}</i>', sBody),
        Paragraph(f'<font color="#3B6D11"><b>Senior:</b></font> {good}', sBody),
    ]]
    mt = Table(md_data, colWidths=[(W-36*mm)*0.3, (W-36*mm)*0.7])
    mt.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(0,0), colors.HexColor("#FEF2F2")),
        ('BACKGROUND', (1,0),(1,0), GREEN_L),
        ('BOX', (0,0),(-1,-1), 0.5, GRAY_B),
        ('INNERGRID', (0,0),(-1,-1), 0.5, GRAY_B),
        ('VALIGN', (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING', (0,0),(-1,-1), 7), ('BOTTOMPADDING', (0,0),(-1,-1), 7),
        ('LEFTPADDING', (0,0),(-1,-1), 8),
    ]))
    add(mt); add(sp(4))

add(sp(10))
highlight('<b>The core insight:</b> A junior knows what tools exist. A senior knows why to pick one over another, what it costs, and how it fails. Every topic in this roadmap is framed that way. After 20 weeks, you will not just be able to answer "what is X" — you will be able to say "I chose X over Y because of Z tradeoff, and here is what I would change at 10x scale." That is what 15+ LPA answers sound like.')

# Build
doc.build(story)
print("PDF created successfully.")