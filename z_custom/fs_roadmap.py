from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas
import os

# ── Colour Palette ─────────────────────────────────────────────────────────────
PURPLE_DARK   = colors.HexColor("#3C3489")
PURPLE_MID    = colors.HexColor("#7F77DD")
PURPLE_LIGHT  = colors.HexColor("#EEEDFE")

TEAL_DARK     = colors.HexColor("#085041")
TEAL_MID      = colors.HexColor("#1D9E75")
TEAL_LIGHT    = colors.HexColor("#E1F5EE")

AMBER_DARK    = colors.HexColor("#633806")
AMBER_MID     = colors.HexColor("#BA7517")
AMBER_LIGHT   = colors.HexColor("#FAEEDA")

BLUE_DARK     = colors.HexColor("#0C447C")
BLUE_MID      = colors.HexColor("#378ADD")
BLUE_LIGHT    = colors.HexColor("#E6F1FB")

GREEN_DARK    = colors.HexColor("#27500A")
GREEN_MID     = colors.HexColor("#639922")
GREEN_LIGHT   = colors.HexColor("#EAF3DE")

CORAL_DARK    = colors.HexColor("#712B13")
CORAL_MID     = colors.HexColor("#D85A30")
CORAL_LIGHT   = colors.HexColor("#FAECE7")

GRAY_DARK     = colors.HexColor("#2C2C2A")
GRAY_MID      = colors.HexColor("#5F5E5A")
GRAY_LIGHT    = colors.HexColor("#F1EFE8")

WHITE         = colors.white
BLACK         = colors.HexColor("#1A1A1A")

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm

# Phase colour map: (dot_bg, dot_fg, header_bg, header_fg, pill_bg, pill_fg, accent)
PHASE_COLORS = [
    (PURPLE_MID,  WHITE, PURPLE_DARK,  WHITE, PURPLE_LIGHT, PURPLE_DARK,  PURPLE_MID),
    (TEAL_MID,    WHITE, TEAL_DARK,    WHITE, TEAL_LIGHT,   TEAL_DARK,    TEAL_MID),
    (AMBER_MID,   WHITE, AMBER_DARK,   WHITE, AMBER_LIGHT,  AMBER_DARK,   AMBER_MID),
    (BLUE_MID,    WHITE, BLUE_DARK,    WHITE, BLUE_LIGHT,   BLUE_DARK,    BLUE_MID),
    (GREEN_MID,   WHITE, GREEN_DARK,   WHITE, GREEN_LIGHT,  GREEN_DARK,   GREEN_MID),
    (CORAL_MID,   WHITE, CORAL_DARK,   WHITE, CORAL_LIGHT,  CORAL_DARK,   CORAL_MID),
    (GRAY_MID,    WHITE, GRAY_DARK,    WHITE, GRAY_LIGHT,   GRAY_DARK,    GRAY_MID),
    (PURPLE_MID,  WHITE, PURPLE_DARK,  WHITE, PURPLE_LIGHT, PURPLE_DARK,  PURPLE_MID),
]

# ── Custom Flowables ────────────────────────────────────────────────────────────

class PhaseHeader(Flowable):
    """Coloured phase header bar with number badge."""
    def __init__(self, number, title, subtitle, duration, colors_tuple, width):
        super().__init__()
        self.number = number
        self.title = title
        self.subtitle = subtitle
        self.duration = duration
        self.colors = colors_tuple
        self._width = width
        self.height = 18 * mm

    def draw(self):
        c = self.canv
        w, h = self._width, self.height
        dot_bg, dot_fg, hdr_bg, hdr_fg, *_ = self.colors

        # Header background
        c.setFillColor(hdr_bg)
        c.roundRect(0, 0, w, h, 5, fill=1, stroke=0)

        # Circle badge
        r = 7 * mm
        cx, cy = r + 3 * mm, h / 2
        c.setFillColor(dot_bg)
        c.circle(cx, cy, r, fill=1, stroke=0)

        # Badge number/star
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 11)
        label = self.number if self.number != "8" else "★"
        c.drawCentredString(cx, cy - 3.5, label)

        # Title
        tx = cx + r + 4 * mm
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(tx, cy + 1 * mm, self.title)

        # Duration badge (right side)
        dur_text = self.duration
        c.setFont("Helvetica", 8)
        dur_w = c.stringWidth(dur_text, "Helvetica", 8) + 8
        dur_x = w - dur_w - 3 * mm
        c.setFillColor(colors.HexColor("#FFFFFF40") if False else colors.HexColor("#00000030"))
        c.roundRect(dur_x, cy - 3 * mm, dur_w, 6 * mm, 3, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.drawString(dur_x + 4, cy - 1 * mm, dur_text)

        # Subtitle
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.HexColor("#FFFFFFB0") if False else colors.HexColor("#FFFFFF99"))
        c.setFillColor(colors.HexColor("#CCCCCC"))
        c.drawString(tx, cy - 4 * mm, self.subtitle)

    def wrap(self, availW, availH):
        return self._width, self.height


class PillRow(Flowable):
    """A wrapping row of coloured pill badges."""
    def __init__(self, pills, pill_bg, pill_fg, width, pill_font_size=7.5):
        super().__init__()
        self.pills = pills
        self.pill_bg = pill_bg
        self.pill_fg = pill_fg
        self._width = width
        self.pill_font_size = pill_font_size
        self._lines = []
        self._compute_height()

    def _compute_height(self):
        pad_x, pad_y, gap_x, gap_y = 5, 2.5, 4, 3
        pill_h = self.pill_font_size + 2 * pad_y + 1
        x, lines, line = 0, 1, []
        for pill in self.pills:
            # Approximate width: each char ~5.2pt at 7.5pt font
            pw = len(pill) * self.pill_font_size * 0.6 + 2 * pad_x
            if x + pw > self._width and line:
                lines += 1
                line = [pill]
                x = pw + gap_x
            else:
                line.append(pill)
                x += pw + gap_x
        self.num_lines = lines
        self.pill_h = pill_h
        self.gap_y = gap_y
        self.height = lines * (pill_h + gap_y) + gap_y

    def draw(self):
        c = self.canv
        pad_x, pad_y, gap_x, gap_y = 5, 2.5, 4, 3
        pill_h = self.pill_h

        # Draw pills bottom-up (ReportLab y=0 is bottom)
        x, row, rows = 0, [], []
        for pill in self.pills:
            pw = len(pill) * self.pill_font_size * 0.6 + 2 * pad_x
            if x + pw > self._width and row:
                rows.append(row)
                row = [(pill, pw)]
                x = pw + gap_x
            else:
                row.append((pill, pw))
                x += pw + gap_x
        if row:
            rows.append(row)

        total_rows = len(rows)
        for ri, row in enumerate(rows):
            y = (total_rows - 1 - ri) * (pill_h + gap_y) + gap_y
            x = 0
            for pill, pw in row:
                c.setFillColor(self.pill_bg)
                c.roundRect(x, y, pw, pill_h, 3, fill=1, stroke=0)
                c.setFillColor(self.pill_fg)
                c.setFont("Helvetica", self.pill_font_size)
                c.drawString(x + pad_x, y + pad_y + 0.5, pill)
                x += pw + gap_x

    def wrap(self, availW, availH):
        return self._width, self.height


class SectionLabel(Flowable):
    """Small ALL-CAPS muted section label."""
    def __init__(self, text, width):
        super().__init__()
        self.text = text.upper()
        self._width = width
        self.height = 8 * mm

    def draw(self):
        c = self.canv
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(GRAY_MID)
        c.drawString(0, 3, self.text)

    def wrap(self, availW, availH):
        return self._width, self.height


class ProjectBox(Flowable):
    """Highlighted project card box."""
    def __init__(self, icon_char, name, description, features, badge_text, accent, width, is_capstone=False):
        super().__init__()
        self.icon_char = icon_char
        self.name = name
        self.description = description
        self.features = features
        self.badge_text = badge_text
        self.accent = accent
        self._width = width
        self.is_capstone = is_capstone
        self._compute_height()

    def _compute_height(self):
        # Estimate: header + desc lines + features
        desc_lines = max(1, len(self.description) // 80 + 1)
        feat_lines = len(self.features)
        self.height = (10 + 5 + desc_lines * 9 + 4 + feat_lines * 9 + 8) * 0.9 + 16

    def draw(self):
        c = self.canv
        w, h = self._width, self.height
        border_color = self.accent

        # Box background
        c.setFillColor(colors.HexColor("#F8F8F6"))
        c.setStrokeColor(border_color)
        c.setLineWidth(1.2 if self.is_capstone else 0.5)
        c.roundRect(0, 0, w, h, 5, fill=1, stroke=1)

        y = h - 10

        # Project name
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(BLACK)
        c.drawString(8, y, self.name)

        # Badge
        if self.badge_text:
            badge_parts = self.badge_text.split(" | ")
            bx = w - 8
            for bp in reversed(badge_parts):
                bw = len(bp) * 5.5 + 8
                bx -= bw
                bg = GREEN_LIGHT if "Portfolio" in bp else AMBER_LIGHT
                fg = GREEN_DARK if "Portfolio" in bp else AMBER_DARK
                c.setFillColor(bg)
                c.roundRect(bx, y - 2, bw, 9, 3, fill=1, stroke=0)
                c.setFillColor(fg)
                c.setFont("Helvetica-Bold", 6)
                c.drawString(bx + 4, y + 0.5, bp)
                bx -= 3

        y -= 12
        # Description
        c.setFont("Helvetica", 8)
        c.setFillColor(GRAY_MID)
        desc_words = self.description.split()
        line, lines = [], []
        for w_text in desc_words:
            test = " ".join(line + [w_text])
            if c.stringWidth(test, "Helvetica", 8) > w - 16:
                lines.append(" ".join(line))
                line = [w_text]
            else:
                line.append(w_text)
        if line:
            lines.append(" ".join(line))
        for ln in lines:
            c.drawString(8, y, ln)
            y -= 9

        y -= 3
        # Features
        c.setFillColor(self.accent)
        c.rect(6, y - len(self.features) * 9 + 6, 2, len(self.features) * 9, fill=1, stroke=0)

        for feat in self.features:
            c.setFont("Helvetica", 7.5)
            c.setFillColor(GRAY_MID)
            # Arrow
            c.setFillColor(self.accent)
            c.drawString(10, y, "→")
            c.setFillColor(BLACK)
            c.drawString(19, y, feat[:95])
            y -= 9

    def wrap(self, availW, availH):
        return self._width, self.height


class CoverPage(Flowable):
    """Full decorative cover page."""
    def __init__(self, width, height):
        super().__init__()
        self._width = width
        self._height = height
        self.height = height

    def draw(self):
        c = self.canv
        # w, h = self._width, self._height
        w, h = PAGE_W, PAGE_H - 22 * mm

        # Background gradient bands
        band_colors = [PURPLE_DARK, colors.HexColor("#2D2870"), colors.HexColor("#1A1560")]
        band_h = h / 3
        for i, bc in enumerate(band_colors):
            c.setFillColor(bc)
            c.rect(0, h - (i + 1) * band_h, w, band_h, fill=1, stroke=0)

        # Decorative circles (abstract design elements)
        import math
        c.setFillColor(colors.HexColor("#FFFFFF08"))
        c.circle(w * 0.85, h * 0.75, 120, fill=1, stroke=0)
        c.circle(w * 0.1, h * 0.2, 80, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#FFFFFF05"))
        c.circle(w * 0.5, h * 0.55, 200, fill=1, stroke=0)

        # Accent bar
        c.setFillColor(PURPLE_MID)
        c.rect(MARGIN, h * 0.52, 50, 4, fill=1, stroke=0)

        # Main title
        c.setFont("Helvetica-Bold", 36)
        c.setFillColor(WHITE)
        c.drawString(MARGIN, h * 0.56, "Full-Stack Developer")
        c.drawString(MARGIN, h * 0.49, "Roadmap")

        # Subtitle
        c.setFont("Helvetica", 14)
        c.setFillColor(colors.HexColor("#CCCCDD"))
        c.drawString(MARGIN, h * 0.44, "3 YOE → Senior Full-Stack Engineer")

        # Tag pills on cover
        tags = ["React / Angular", "Node.js", "PostgreSQL", "Redis",
                "WebSockets", "SSE", "System Design", "DevOps"]
        tx = MARGIN
        ty = h * 0.37
        for tag in tags:
            tw = len(tag) * 6.5 + 16
            if tx + tw > w - MARGIN:
                tx = MARGIN
                ty -= 16
            c.setFillColor(colors.HexColor("#FFFFFF20"))
            c.roundRect(tx, ty, tw, 13, 4, fill=1, stroke=0)
            c.setFont("Helvetica", 8)
            c.setFillColor(WHITE)
            c.drawString(tx + 8, ty + 3, tag)
            tx += tw + 6

        # Timeline
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(WHITE)
        c.drawString(MARGIN, h * 0.28, "18-Month Project-Based Learning Plan")

        stats = [("5", "Portfolio Projects"), ("8", "Learning Phases"), ("18", "Months")]
        sx = MARGIN
        for val, label in stats:
            c.setFillColor(colors.HexColor("#FFFFFF15"))
            c.roundRect(sx, h * 0.20, 80, 36, 6, fill=1, stroke=0)
            c.setFont("Helvetica-Bold", 20)
            c.setFillColor(PURPLE_MID)
            c.drawString(sx + 8, h * 0.20 + 18, val)
            c.setFont("Helvetica", 8)
            c.setFillColor(colors.HexColor("#CCCCDD"))
            c.drawString(sx + 8, h * 0.20 + 7, label)
            sx += 92

        # Bottom note
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.HexColor("#9999AA"))
        c.drawString(MARGIN, h * 0.12, "Each phase builds on the last. Topics become features in real portfolio projects.")
        c.drawString(MARGIN, h * 0.09, "Ship code you can demo in every interview.")

    def wrap(self, availW, availH):
        return self._width, self._height


# ── Roadmap Data ───────────────────────────────────────────────────────────────

PHASES = [
    {
        "num": "1",
        "title": "Senior Frontend Mastery",
        "subtitle": "Deep-dive Angular/React + modern tooling",
        "duration": "Months 1–3",
        "topics": [
            "React 19 patterns", "Server components", "Angular signals",
            "Micro-frontends", "Zustand / NgRx", "Code splitting",
            "Lazy loading", "Bundle analysis", "Tree shaking",
            "CSR / SSR / ISR / SSG", "Accessibility (WCAG 2.2)",
            "Web Vitals (LCP/CLS/INP)", "Testing (Vitest, Cypress)",
        ],
        "project": {
            "name": "Project 1: DevFlow Dashboard",
            "description": "A GitHub-like developer dashboard displaying repos, activity, and streaks. Built with Next.js (App Router) + Angular micro-frontend widget.",
            "features": [
                "Server components + client islands for hybrid rendering",
                "Real-time GitHub stats via Server-Sent Events (SSE)",
                "Full Lighthouse 100 score — measure and fix every Web Vital",
                "Keyboard-navigable, WCAG 2.2 AA compliant throughout",
                "Vitest unit tests + Cypress E2E coverage",
            ],
            "badge": "Portfolio | Resume",
        },
    },
    {
        "num": "2",
        "title": "Design Systems & UI Engineering",
        "subtitle": "Component libraries, tokens, Storybook",
        "duration": "Months 3–5",
        "topics": [
            "Design tokens", "Storybook 8", "Radix / shadcn/ui",
            "Compound components", "Polymorphic components", "CSS custom properties",
            "Tailwind v4", "Figma tokens plugin", "Visual regression tests",
            "Theme switching", "Animation (Framer Motion)", "Chromatic CI",
        ],
        "project": {
            "name": "Project 2: Forge UI — Component Library",
            "description": "A publishable npm component library with 20+ components, design token system, dark mode, and Storybook docs. Stands out heavily on resumes.",
            "features": [
                "Design token pipeline: Figma → JSON → CSS vars → Tailwind",
                "Polymorphic Button, Card, Modal, Form, DataTable components",
                "Storybook with interactive docs, a11y addon, viewport controls",
                "Automated visual regression via Chromatic on every PR",
                "Published to npm with semantic versioning + changelog",
            ],
            "badge": "Portfolio | Resume",
        },
    },
    {
        "num": "3",
        "title": "Frontend Performance Engineering",
        "subtitle": "Perf profiling, memory, rendering pipeline",
        "duration": "Months 5–6",
        "topics": [
            "Chrome DevTools deep dive", "Rendering pipeline", "Memory profiling",
            "Layout thrashing", "Virtualization (TanStack)", "Image optimization",
            "Font subsetting", "HTTP/2 + HTTP/3", "Resource hints (preload/prefetch)",
            "Service workers", "Web Workers", "WASM basics", "RUM (Sentry/Datadog)",
        ],
        "project": {
            "name": "Add-on to Project 1: Performance Audit Report",
            "description": "Take the DevFlow Dashboard and ship a documented performance transformation — before/after metrics you can show in interviews.",
            "features": [
                "TanStack Virtual for activity feed — 10,000 rows smooth scroll",
                "Web Worker for heavy data processing (GitHub stats aggregation)",
                "Service worker + cache-first strategy for offline support",
                "Document LCP improvement from baseline (target: under 1.5s)",
                "Write a technical blog post about the optimisation journey",
            ],
            "badge": "Resume",
        },
    },
    {
        "num": "4",
        "title": "Backend Foundations (Node.js)",
        "subtitle": "APIs, databases, auth, security",
        "duration": "Months 6–9",
        "topics": [
            "Node.js / Bun runtime", "REST API design", "Hono / Fastify / Express",
            "PostgreSQL", "Drizzle ORM / Prisma", "Redis",
            "JWT + refresh tokens", "OAuth 2.0 / OIDC", "Session management",
            "Bcrypt / Argon2", "CORS, CSRF, XSS", "Input validation (Zod)",
            "Rate limiting", "API versioning", "Swagger / OpenAPI",
        ],
        "project": {
            "name": "Project 3: Collab — Real-time Workspace",
            "description": "A Notion-like collaborative workspace. Ship the full backend: REST + WebSocket + auth + database — then connect your frontend from Phases 1 and 2.",
            "features": [
                "Auth: JWT + refresh token rotation, Google OAuth, magic links",
                "PostgreSQL schema with Drizzle ORM + proper migrations",
                "WebSockets for real-time collaborative document editing",
                "Redis for session cache + pub/sub across instances",
                "Rate limiting middleware per user, per IP address",
                "OpenAPI spec with Swagger UI, auto-generated from Zod schemas",
                "Full OWASP Top 10 audit checklist in README",
            ],
            "badge": "Portfolio | Resume",
        },
    },
    {
        "num": "5",
        "title": "Real-time, Sockets & Streaming",
        "subtitle": "WebSockets, SSE, queues",
        "duration": "Months 9–10",
        "topics": [
            "WebSocket protocol", "Socket.io", "Server-Sent Events",
            "Long polling (legacy)", "Message queues (BullMQ)",
            "Event-driven architecture", "Presence systems",
            "Operational transforms (OT)", "CRDT basics", "Reconnect strategies",
        ],
        "project": {
            "name": "Add-on to Project 3: Live Features Sprint",
            "description": "Extend Collab with production-grade real-time features that demonstrate deep understanding of async systems.",
            "features": [
                "Presence indicators — who is online, live cursors on documents",
                "SSE-based notification system (no polling overhead)",
                "BullMQ background jobs: email, exports, AI processing pipeline",
                "Graceful reconnection with exponential backoff on the client",
            ],
            "badge": "Resume",
        },
    },
    {
        "num": "6",
        "title": "DevOps, Infra & Production Deployment",
        "subtitle": "Docker, CI/CD, cloud, monitoring",
        "duration": "Months 10–12",
        "topics": [
            "Docker + compose", "GitHub Actions CI/CD", "AWS / GCP / Railway",
            "Nginx / reverse proxy", "SSL/TLS (Let's Encrypt)", "Kubernetes basics",
            "Environment secrets", "Sentry error tracking", "Grafana + Prometheus",
            "Log aggregation", "Zero-downtime deploys", "Database backups", "CDN (Cloudflare)",
        ],
        "project": {
            "name": "Ship Collab to Production",
            "description": "Take the full Collab app and ship it with a production-grade infrastructure setup — something you can demo live in any interview.",
            "features": [
                "Dockerize frontend + backend + worker + Redis + Postgres",
                "GitHub Actions: lint → test → build → deploy pipeline",
                "Deploy to Railway / Render / AWS with custom domain + SSL",
                "Grafana dashboard: requests/sec, error rate, p95 latency",
                "Runbook + architecture diagram in repo wiki",
            ],
            "badge": "Portfolio | Resume",
        },
    },
    {
        "num": "7",
        "title": "System Design & Scalability",
        "subtitle": "Caching, scaling, architecture patterns",
        "duration": "Months 12–15",
        "topics": [
            "CAP theorem", "Horizontal scaling", "Load balancing",
            "DB replication", "Read replicas", "Sharding",
            "Caching strategies", "Cache invalidation", "CDN strategy",
            "API Gateway", "Circuit breakers", "Idempotency",
            "gRPC basics", "Message brokers (Kafka)",
        ],
        "project": {
            "name": "Project 4: Scale Collab to 10k Users",
            "description": "Design and partially implement how Collab would scale. The architecture document alone is a strong portfolio piece for senior roles.",
            "features": [
                "Multi-layer caching: Redis L1 (hot data) + CDN L2 (static assets)",
                "DB read replica for analytics queries, reducing write DB load",
                "Distributed rate limiting with Redis sliding window algorithm",
                "Write system design doc: How to scale Collab to 100k users",
                "Load test with k6: measure break points, document results",
            ],
            "badge": "Resume",
        },
    },
    {
        "num": "8",
        "title": "Capstone: Ship a SaaS from Scratch",
        "subtitle": "Your magnum opus — every skill integrated",
        "duration": "Months 15–18",
        "topics": [],
        "project": {
            "name": "Project 5: PulseMetrics — Analytics SaaS",
            "description": "A lightweight Plausible/PostHog alternative. Every skill from every phase ships together into one production product with real users.",
            "features": [
                "Design system: custom component library from Phase 2",
                "Auth: email/password + Google OAuth + org/team multi-tenancy",
                "Billing: Stripe subscriptions, webhooks, usage metering",
                "Event ingestion: high-throughput endpoint + Kafka queue",
                "Real-time dashboard: WebSocket live visitor counts",
                "SSE alerts: notify when traffic spikes are detected",
                "Redis caching for dashboard queries (cache-aside pattern)",
                "Rate limiting per API key + per org subscription tier",
                "Full CI/CD: test → build → deploy → smoke test",
                "Monitoring: Sentry + Grafana + uptime checks",
                "Public landing page (Next.js) with Lighthouse 100 score",
                "Write-up: architecture decisions + trade-offs document",
            ],
            "badge": "Portfolio | Resume",
        },
        "is_capstone": True,
    },
]

STUDY_RESOURCES = [
    ("Books", [
        "Alex Xu — System Design Interview Vol 1 & 2",
        "Kyle Simpson — You Don't Know JS (YDKJS) series",
        "Addy Osmani — Learning Patterns (free online)",
        "Designing Data-Intensive Applications — Martin Kleppmann",
    ]),
    ("Practice", [
        "Neetcode 150 — DSA for technical interviews",
        "roadmap.sh/frontend + roadmap.sh/backend",
        "Frontend Masters — Advanced courses",
        "Build in public — tweet your progress weekly",
    ]),
    ("Visibility", [
        "Write technical articles on dev.to or personal blog",
        "Contribute to open-source (good first issues)",
        "Record Loom walkthroughs of each project",
        "LinkedIn posts about what you shipped each month",
    ]),
]


# ── Page Template ──────────────────────────────────────────────────────────────

def make_canvas_decorator(doc):
    def decorator(canvas_obj, doc_obj):
        canvas_obj.saveState()
        w = PAGE_W

        # Header bar
        canvas_obj.setFillColor(PURPLE_DARK)
        canvas_obj.rect(0, PAGE_H - 8 * mm, w, 8 * mm, fill=1, stroke=0)
        canvas_obj.setFillColor(WHITE)
        canvas_obj.setFont("Helvetica-Bold", 7)
        canvas_obj.drawString(MARGIN, PAGE_H - 5 * mm, "Full-Stack Developer Roadmap")
        canvas_obj.setFont("Helvetica", 7)
        canvas_obj.drawRightString(w - MARGIN, PAGE_H - 5 * mm, "3 YOE → Senior Engineer")

        # Footer
        canvas_obj.setFillColor(GRAY_LIGHT)
        canvas_obj.rect(0, 0, w, 7 * mm, fill=1, stroke=0)
        canvas_obj.setFillColor(GRAY_MID)
        canvas_obj.setFont("Helvetica", 7)
        canvas_obj.drawString(MARGIN, 2.5 * mm, "Project-Based Learning | Ship real apps, not tutorials")
        canvas_obj.drawRightString(w - MARGIN, 2.5 * mm, f"Page {doc_obj.page}")

        # Thin accent line at top of content area
        canvas_obj.setStrokeColor(PURPLE_MID)
        canvas_obj.setLineWidth(0.5)
        canvas_obj.line(MARGIN, PAGE_H - 8.5 * mm, w - MARGIN, PAGE_H - 8.5 * mm)

        canvas_obj.restoreState()
    return decorator


# ── Build PDF ──────────────────────────────────────────────────────────────────

def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=12 * mm,
        bottomMargin=10 * mm,
        title="Full-Stack Developer Roadmap",
        author="Generated Roadmap",
    )

    content_width = PAGE_W - 2 * MARGIN
    styles = getSampleStyleSheet()

    def style(name, **kwargs):
        return ParagraphStyle(name, **kwargs)

    s_normal = style("sNormal", fontName="Helvetica", fontSize=8.5, leading=13, textColor=BLACK)
    s_h2 = style("sH2", fontName="Helvetica-Bold", fontSize=13, leading=18, textColor=PURPLE_DARK, spaceAfter=4)
    s_body = style("sBody", fontName="Helvetica", fontSize=8.5, leading=13, textColor=GRAY_DARK)
    s_caption = style("sCaption", fontName="Helvetica", fontSize=7.5, leading=11, textColor=GRAY_MID)
    s_intro = style("sIntro", fontName="Helvetica", fontSize=9.5, leading=15, textColor=GRAY_DARK)

    story = []

    # ── Cover ──
    # story.append(CoverPage(PAGE_W, PAGE_H))
    # story.append(CoverPage(content_width, PAGE_H - 22 * mm))
    story.append(CoverPage(content_width, 240 * mm))
    story.append(PageBreak())

    # ── Intro ──
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("About This Roadmap", s_h2))
    story.append(HRFlowable(width=content_width, thickness=0.5, color=PURPLE_LIGHT, spaceAfter=6))
    intro_text = (
        "This is an 18-month, project-based learning plan designed to take you from 3 years of frontend experience "
        "to a well-rounded senior full-stack engineer. Every phase combines concrete topics to learn with a real "
        "project that implements those topics as features — so you always have working code to show, not just notes. "
        "By the end, you will have shipped 5 portfolio projects, a published npm library, a live SaaS product, "
        "and the system design knowledge to confidently interview for senior and full-stack roles."
    )
    story.append(Paragraph(intro_text, s_intro))
    story.append(Spacer(1, 4 * mm))

    # Summary stats table
    stat_data = [["5 Projects", "8 Phases", "18 Months", "1 Live SaaS"]]
    stat_table = Table(stat_data, colWidths=[content_width / 4] * 4, rowHeights=[14 * mm])
    stat_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), PURPLE_LIGHT),
        ("BACKGROUND", (1, 0), (1, 0), TEAL_LIGHT),
        ("BACKGROUND", (2, 0), (2, 0), AMBER_LIGHT),
        ("BACKGROUND", (3, 0), (3, 0), BLUE_LIGHT),
        ("TEXTCOLOR", (0, 0), (0, 0), PURPLE_DARK),
        ("TEXTCOLOR", (1, 0), (1, 0), TEAL_DARK),
        ("TEXTCOLOR", (2, 0), (2, 0), AMBER_DARK),
        ("TEXTCOLOR", (3, 0), (3, 0), BLUE_DARK),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("ROUNDEDCORNERS", [6, 6, 6, 6]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0, colors.white),
    ]))
    story.append(stat_table)
    story.append(Spacer(1, 6 * mm))

    # ── Phases ──
    for i, phase in enumerate(PHASES):
        pc = PHASE_COLORS[i]
        _, _, _, _, pill_bg, pill_fg, accent = pc

        block = []
        block.append(Spacer(1, 3 * mm))
        block.append(PhaseHeader(
            phase["num"], phase["title"], phase["subtitle"],
            phase["duration"], pc, content_width
        ))
        block.append(Spacer(1, 3 * mm))

        if phase["topics"]:
            block.append(SectionLabel("Topics to learn", content_width))
            block.append(Spacer(1, 1 * mm))
            block.append(PillRow(phase["topics"], pill_bg, pill_fg, content_width))
            block.append(Spacer(1, 3 * mm))

        proj = phase["project"]
        block.append(SectionLabel("Project / Implementation", content_width))
        block.append(Spacer(1, 1 * mm))
        block.append(ProjectBox(
            "→",
            proj["name"],
            proj["description"],
            proj["features"],
            proj.get("badge", ""),
            accent,
            content_width,
            is_capstone=phase.get("is_capstone", False),
        ))
        block.append(Spacer(1, 2 * mm))

        story.append(KeepTogether(block[:4]))
        for item in block[4:]:
            story.append(item)

    story.append(PageBreak())

    # ── Study Resources ──
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("Study Alongside Every Phase", s_h2))
    story.append(HRFlowable(width=content_width, thickness=0.5, color=PURPLE_LIGHT, spaceAfter=6))
    story.append(Paragraph(
        "These resources run in parallel with your project work — 30 minutes a day compounds dramatically over 18 months.",
        s_body
    ))
    story.append(Spacer(1, 4 * mm))

    res_colors = [(PURPLE_LIGHT, PURPLE_DARK, PURPLE_MID),
                  (TEAL_LIGHT, TEAL_DARK, TEAL_MID),
                  (AMBER_LIGHT, AMBER_DARK, AMBER_MID)]

    for (cat, items), (bg, fg, mid) in zip(STUDY_RESOURCES, res_colors):
        cat_data = [[Paragraph(f"<b>{cat}</b>", style("rc", fontName="Helvetica-Bold", fontSize=9, textColor=fg))]]
        for item in items:
            cat_data.append([Paragraph(f"→  {item}", style("ri", fontName="Helvetica", fontSize=8, textColor=GRAY_DARK, leading=12))])
        t = Table(cat_data, colWidths=[content_width / 3 - 4])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), bg),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FAFAF8")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("LINEBELOW", (0, 0), (-1, -2), 0.3, bg),
            ("BOX", (0, 0), (-1, -1), 0.5, mid),
            ("ROUNDEDCORNERS", [6, 6, 6, 6]),
        ]))
        story.append(t)
        story.append(Spacer(1, 3 * mm))

    # ── Final tips ──
    story.append(PageBreak())
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("Interview Strategy & Career Tips", s_h2))
    story.append(HRFlowable(width=content_width, thickness=0.5, color=PURPLE_LIGHT, spaceAfter=6))

    tips = [
        ("Resume", [
            "List the 5 projects with impact metrics: 'Reduced LCP from 4.2s to 0.9s', 'Published npm package with 500+ downloads'",
            "Headline skill: Full-Stack Engineer (React / Node.js / PostgreSQL)",
            "Add a GitHub profile link — every project should have a clean README with live demo link",
        ]),
        ("Interviews", [
            "For system design: use the Collab scaling doc as a template — you have already solved this problem once",
            "For coding rounds: Neetcode 150 covers 90% of patterns. Focus on arrays, trees, graphs, dynamic programming",
            "For frontend rounds: be ready to implement a debounce, a virtual list, or a state machine from scratch",
        ]),
        ("Job Search", [
            "Target companies that list both frontend and full-stack roles — they value frontend depth + backend breadth",
            "Your PulseMetrics SaaS is a conversation starter: 'I built and shipped this — here is the architecture'",
            "Aim for: Mid-level Full-Stack, Senior Frontend, or Full-Stack Engineer titles at 8-15 person eng teams",
        ]),
    ]

    tip_colors = [
        (BLUE_LIGHT, BLUE_DARK, BLUE_MID),
        (GREEN_LIGHT, GREEN_DARK, GREEN_MID),
        (CORAL_LIGHT, CORAL_DARK, CORAL_MID),
    ]

    for (section, tip_list), (bg, fg, mid) in zip(tips, tip_colors):
        rows = [[Paragraph(f"<b>{section}</b>", style("ts", fontName="Helvetica-Bold", fontSize=9, textColor=fg))]]
        for tip in tip_list:
            rows.append([Paragraph(f"→  {tip}", style("ti", fontName="Helvetica", fontSize=8, textColor=GRAY_DARK, leading=12))])
        t = Table(rows, colWidths=[content_width])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), bg),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FAFAF8")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("LINEBELOW", (0, 0), (-1, -2), 0.3, bg),
            ("BOX", (0, 0), (-1, -1), 0.5, mid),
            ("ROUNDEDCORNERS", [6, 6, 6, 6]),
        ]))
        story.append(t)
        story.append(Spacer(1, 4 * mm))

    # ── Closing ──
    story.append(Spacer(1, 4 * mm))
    closing_style = style("closing", fontName="Helvetica-Bold", fontSize=12,
                          textColor=PURPLE_DARK, alignment=TA_CENTER, leading=18)
    story.append(Paragraph("Ship code. Write about it. Get hired.", closing_style))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(
        "Every week you are building — not just studying. That is what separates you from the crowd.",
        style("cs2", fontName="Helvetica", fontSize=9, textColor=GRAY_MID, alignment=TA_CENTER)
    ))

    # Build
    decorator = make_canvas_decorator(doc)
    doc.build(story, onFirstPage=decorator, onLaterPages=decorator)
    print(f"PDF saved: {output_path}")


if __name__ == "__main__":
    output = "C:/Users/Madhusudhan Rao/workspace/python/fullstack_roadmap.pdf"
    build_pdf(output)