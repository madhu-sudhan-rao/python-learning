from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus.flowables import Flowable
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

import os

# =========================================
# COLORS
# =========================================
TEAL = colors.HexColor("#0F6E56")
TEAL_LIGHT = colors.HexColor("#E1F5EE")

BLUE = colors.HexColor("#185FA5")
BLUE_LIGHT = colors.HexColor("#E6F1FB")

AMBER = colors.HexColor("#854F0B")
AMBER_LIGHT = colors.HexColor("#FAEEDA")

GRAY = colors.HexColor("#444441")
GRAY_LIGHT = colors.HexColor("#F1EFE8")

PURPLE = colors.HexColor("#534AB7")
PURPLE_LIGHT = colors.HexColor("#EEEDFE")

CORAL = colors.HexColor("#993C1D")
CORAL_LIGHT = colors.HexColor("#FAECE7")


# =========================================
# DOCUMENT
# =========================================
doc = SimpleDocTemplate(
    "DSA_Video_Package.pdf",
    pagesize=A4,
    rightMargin=18 * mm,
    leftMargin=18 * mm,
    topMargin=18 * mm,
    bottomMargin=18 * mm,
)

styles = getSampleStyleSheet()

# =========================================
# CUSTOM STYLES
# =========================================
title_style = ParagraphStyle(
    "TitleStyle",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=28,
    leading=34,
    textColor=TEAL,
    alignment=TA_CENTER,
    spaceAfter=10,
)

subtitle_style = ParagraphStyle(
    "SubtitleStyle",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=14,
    leading=20,
    textColor=GRAY,
    alignment=TA_CENTER,
)

small_italic_style = ParagraphStyle(
    "SmallItalic",
    parent=styles["BodyText"],
    fontName="Helvetica-Oblique",
    fontSize=10,
    textColor=colors.grey,
    alignment=TA_CENTER,
    spaceAfter=20,
)

heading_style = ParagraphStyle(
    "HeadingStyle",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=20,
    leading=26,
    textColor=TEAL,
    spaceBefore=12,
    spaceAfter=8,
)

sub_heading_style = ParagraphStyle(
    "SubHeadingStyle",
    parent=styles["Heading3"],
    fontName="Helvetica-Bold",
    fontSize=15,
    leading=20,
    textColor=BLUE,
    spaceBefore=10,
    spaceAfter=6,
)

body_style = ParagraphStyle(
    "BodyStyle",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=11,
    leading=18,
    textColor=colors.black,
    spaceAfter=6,
)

script_style = ParagraphStyle(
    "ScriptStyle",
    parent=body_style,
    leftIndent=10 * mm,
    fontSize=12,
    leading=20,
)

direction_style = ParagraphStyle(
    "DirectionStyle",
    parent=body_style,
    leftIndent=10 * mm,
    fontName="Helvetica-Oblique",
    textColor=colors.grey,
)

bullet_style = ParagraphStyle(
    "BulletStyle",
    parent=body_style,
    leftIndent=6 * mm,
    bulletIndent=0,
)

center_style = ParagraphStyle(
    "CenterStyle",
    parent=body_style,
    alignment=TA_CENTER,
)

# =========================================
# HELPERS
# =========================================
elements = []


def add_spacer(h=5):
    elements.append(Spacer(1, h * mm))


def add_divider(color=TEAL):
    elements.append(
        HRFlowable(
            width="100%",
            thickness=1.5,
            color=color,
            spaceBefore=8,
            spaceAfter=8,
        )
    )


def add_body(text):
    elements.append(Paragraph(text, body_style))


def add_script(text):
    elements.append(Paragraph(text, script_style))


def add_direction(text):
    elements.append(Paragraph(f"[{text}]", direction_style))


def add_bullet(text):
    elements.append(Paragraph(f"• {text}", bullet_style))


def section_header(num, title, time, bg_color, text_color):
    data = [
        [
            Paragraph(
                f"<b>{num}</b>",
                ParagraphStyle(
                    "num",
                    alignment=TA_CENTER,
                    textColor=text_color,
                    fontSize=12,
                    fontName="Helvetica-Bold",
                ),
            ),
            Paragraph(
                f"<b>{title}</b>",
                ParagraphStyle(
                    "title",
                    textColor=text_color,
                    fontSize=12,
                    fontName="Helvetica-Bold",
                ),
            ),
            Paragraph(
                time,
                ParagraphStyle(
                    "time",
                    alignment=TA_RIGHT,
                    textColor=text_color,
                    fontSize=10,
                    fontName="Helvetica-Oblique",
                ),
            ),
        ]
    ]

    table = Table(data, colWidths=[18 * mm, 110 * mm, 35 * mm])

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg_color),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    elements.append(table)
    add_spacer(3)


# =========================================
# COVER PAGE
# =========================================
elements.append(Spacer(1, 40 * mm))

elements.append(
    Paragraph("DSA for Beginners", title_style)
)

elements.append(
    Paragraph(
        "Talking Video — Complete Production Package",
        subtitle_style,
    )
)

elements.append(
    Paragraph(
        "Script | YouTube Description | Thumbnail Concept",
        small_italic_style,
    )
)

add_divider()

# =========================================
# PART 1
# =========================================
elements.append(
    Paragraph("<b>PART 1</b>", ParagraphStyle(
        "part",
        fontSize=11,
        textColor=TEAL,
    ))
)

elements.append(
    Paragraph("Full Word-for-Word Script", heading_style)
)

elements.append(
    Paragraph(
        "Duration: ~10–12 minutes | Style: Talking head, conversational",
        small_italic_style,
    )
)

# =========================================
# SECTION 00
# =========================================
section_header(
    "00",
    "Hook & Introduction",
    "0:00 – 1:00",
    TEAL_LIGHT,
    TEAL,
)

add_direction("Look straight into the camera.")

add_script("You've probably seen it everywhere —")
add_script("LinkedIn posts, YouTube comments, college seniors telling you —")
add_script('"Learn DSA. You have to learn DSA."')

add_script("But nobody actually explains what DSA really is.")
add_script("Today, we're fixing that.")

add_divider(colors.HexColor("#CCCCCC"))

# =========================================
# SECTION 01
# =========================================
section_header(
    "01",
    "What is DSA?",
    "1:00 – 2:30",
    BLUE_LIGHT,
    BLUE,
)

add_direction("Teach calmly and confidently.")

add_script("DSA stands for Data Structures and Algorithms.")
add_script("Data Structures organize information efficiently.")
add_script("Algorithms are step-by-step solutions to problems.")

add_script("Together, they power every modern software system.")

add_divider(colors.HexColor("#CCCCCC"))

# =========================================
# SECTION 02
# =========================================
section_header(
    "02",
    "Why is DSA Needed?",
    "2:30 – 4:00",
    AMBER_LIGHT,
    AMBER,
)

add_script("Without DSA, code may work — but it won't scale well.")
add_script("DSA helps developers write optimized and efficient systems.")
add_script("It improves performance and problem-solving ability.")

add_divider(colors.HexColor("#CCCCCC"))

# =========================================
# SECTION 03
# =========================================
section_header(
    "03",
    "DSA in Interviews",
    "4:00 – 5:30",
    PURPLE_LIGHT,
    PURPLE,
)

add_script("Top companies test DSA heavily in technical interviews.")
add_script("Interviewers care about how you think and solve problems.")
add_script("Arrays and Strings are the best starting point.")

add_divider(colors.HexColor("#CCCCCC"))

# =========================================
# SECTION 04
# =========================================
section_header(
    "04",
    "DSA in Real Projects",
    "5:30 – 7:00",
    CORAL_LIGHT,
    CORAL,
)

add_script("Search systems, recommendations, queues, and caching use DSA.")
add_script("Good DSA knowledge helps apps scale efficiently.")

add_divider(colors.HexColor("#CCCCCC"))

# =========================================
# OUTRO
# =========================================
section_header(
    "05",
    "Outro",
    "7:00 – 8:00",
    TEAL_LIGHT,
    TEAL,
)

add_script("DSA is a long-term skill.")
add_script("Consistency matters more than intensity.")
add_script("Start small and improve every day.")

add_script("Subscribe for the next beginner DSA videos.")

# =========================================
# PAGE BREAK
# =========================================
elements.append(PageBreak())

# =========================================
# PART 2
# =========================================
elements.append(
    Paragraph("YouTube Description", heading_style)
)

add_body(
    "Everyone tells you to learn DSA — but nobody explains why."
)

add_body(
    "This video breaks down DSA in simple beginner-friendly language."
)

elements.append(
    Paragraph("<b>Topics Covered:</b>", sub_heading_style)
)

add_bullet("What is DSA?")
add_bullet("Why DSA matters")
add_bullet("DSA in interviews")
add_bullet("DSA in real projects")
add_bullet("DSA in the AI era")

# =========================================
# PAGE BREAK
# =========================================
elements.append(PageBreak())

# =========================================
# PART 3
# =========================================
elements.append(
    Paragraph("Thumbnail Concept", heading_style)
)

add_body(
    "Use a dark premium background with bold readable text."
)

elements.append(
    Paragraph("Thumbnail Ideas", sub_heading_style)
)

add_bullet("What is DSA?")
add_bullet("Why It Actually Matters")
add_bullet("No Code. No Jargon.")

elements.append(
    Paragraph("Do's and Don'ts", sub_heading_style)
)

add_body("<b>DO:</b>")
add_bullet("Use your face")
add_bullet("Keep text minimal")
add_bullet("Ensure mobile readability")

add_body("<b>DON'T:</b>")
add_bullet("Use cluttered backgrounds")
add_bullet("Use too much text")
add_bullet("Use generic coding stock images")

add_spacer(10)

elements.append(
    Paragraph(
        "<b>Good luck with the video!</b>",
        center_style,
    )
)

# =========================================
# BUILD PDF
# =========================================
doc.build(elements)

print("PDF generated successfully!")