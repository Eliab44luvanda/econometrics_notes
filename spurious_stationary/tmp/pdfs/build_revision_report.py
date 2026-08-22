import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, PageBreak, Paragraph, Spacer, Table,
    TableStyle, KeepTogether
)

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "revision_implementation_report.md"
OUTPUT = ROOT / "output/pdf/spurious_regression_revision_implementation_report.pdf"

NAVY = colors.HexColor("#16324F")
BLUE = colors.HexColor("#2E5E88")
GREY = colors.HexColor("#5B6670")
DARK = colors.HexColor("#20262C")
LIGHT = colors.HexColor("#E4E8EB")
PALE = colors.HexColor("#EAF1F7")


def fonts():
    paths = {
        "Body": "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        "Body-Bold": "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
        "Body-Italic": "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",
    }
    try:
        for name, path in paths.items():
            pdfmetrics.registerFont(TTFont(name, path))
        return "Body", "Body-Bold", "Body-Italic"
    except Exception:
        return "Times-Roman", "Times-Bold", "Times-Italic"


BODY, BOLD, ITALIC = fonts()
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleX", fontName=BOLD, fontSize=21, leading=25,
                          textColor=NAVY, spaceAfter=8))
styles.add(ParagraphStyle(name="SubX", fontName=BODY, fontSize=10.5, leading=15,
                          textColor=GREY, spaceAfter=14))
styles.add(ParagraphStyle(name="H1X", fontName=BOLD, fontSize=14.5, leading=18,
                          textColor=NAVY, spaceBefore=12, spaceAfter=6))
styles.add(ParagraphStyle(name="H2X", fontName=BOLD, fontSize=11, leading=14,
                          textColor=BLUE, spaceBefore=8, spaceAfter=4))
styles.add(ParagraphStyle(name="BodyX", fontName=BODY, fontSize=9.3, leading=13.3,
                          textColor=DARK, spaceAfter=5))
styles.add(ParagraphStyle(name="BulletX", fontName=BODY, fontSize=9.2, leading=13,
                          leftIndent=14, firstLineIndent=-8, bulletIndent=3,
                          textColor=DARK, spaceAfter=3))
styles.add(ParagraphStyle(name="SmallX", fontName=BODY, fontSize=8, leading=11,
                          textColor=GREY))
styles.add(ParagraphStyle(name="CalloutX", fontName=BODY, fontSize=9.5, leading=14,
                          textColor=DARK))


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setStrokeColor(LIGHT)
    canvas.setLineWidth(0.5)
    canvas.line(20 * mm, h - 16 * mm, w - 20 * mm, h - 16 * mm)
    canvas.setFont(BODY, 7.5)
    canvas.setFillColor(GREY)
    canvas.drawString(20 * mm, h - 12.5 * mm, "Revision implementation report")
    canvas.drawRightString(w - 20 * mm, 11 * mm, f"Page {doc.page}")
    canvas.restoreState()


def inline_markup(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", text)
    text = text.replace("\\lambda", "lambda").replace("\\phi", "phi")
    text = text.replace("\\operatorname", "operatorname")
    text = text.replace("\\[", "").replace("\\]", "")
    text = text.replace("\\(", "").replace("\\)", "")
    return text


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=22 * mm, bottomMargin=18 * mm,
    title="Revision Implementation Report", author="Codex"
)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
doc.addPageTemplates(PageTemplate(id="report", frames=[frame], onPage=header_footer))

story = [Spacer(1, 12 * mm), Paragraph("Revision Implementation Report", styles["TitleX"]),
         Paragraph("Spurious regression in stationary time series", styles["SubX"])]

summary = Table([[Paragraph(
    "<b>Outcome:</b> All substantive review findings were addressed in the theory, Monte Carlo design, results discussion, and standalone R implementation. The revised article and script now share one computational source.",
    styles["CalloutX"]) ]], colWidths=[155 * mm])
summary.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), PALE),
    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#A9C0D2")),
    ("LEFTPADDING", (0, 0), (-1, -1), 9),
    ("RIGHTPADDING", (0, 0), (-1, -1), 9),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.extend([summary, Spacer(1, 5 * mm)])

lines = SOURCE.read_text(encoding="utf-8").splitlines()
paragraph = []
in_equation = False
equation = []


def flush_paragraph():
    if paragraph:
        story.append(Paragraph(inline_markup(" ".join(paragraph)), styles["BodyX"]))
        paragraph.clear()


for raw in lines:
    line = raw.strip()
    if line == "# Revision Implementation Report":
        continue
    if line == "\\[":
        flush_paragraph()
        in_equation = True
        equation = []
        continue
    if line == "\\]":
        raw_eq = " ".join(equation)
        if "phi_x" in raw_eq:
            eq = "lambda = (1 + phi_x phi_y) / (1 - phi_x phi_y)"
        elif "LRV" in raw_eq:
            eq = "lambda = LRV[(x_t - mu_x) u_t] / {Var(x_t) Var(u_t)}"
        else:
            eq = re.sub(r"\\[a-zA-Z]+", "", raw_eq).replace("{", "").replace("}", "")
        story.append(Table([[Paragraph(eq, styles["CalloutX"])]], colWidths=[145 * mm],
                           style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F7F9FA")),
                                             ("LEFTPADDING", (0, 0), (-1, -1), 8),
                                             ("TOPPADDING", (0, 0), (-1, -1), 5),
                                             ("BOTTOMPADDING", (0, 0), (-1, -1), 5)])))
        in_equation = False
        continue
    if in_equation:
        equation.append(line)
        continue
    if line.startswith("## "):
        flush_paragraph()
        story.append(Paragraph(inline_markup(line[3:]), styles["H1X"]))
    elif line.startswith("### "):
        flush_paragraph()
        story.append(Paragraph(inline_markup(line[4:]), styles["H2X"]))
    elif line.startswith("- "):
        flush_paragraph()
        story.append(Paragraph(inline_markup(line[2:]), styles["BulletX"], bulletText="-"))
    elif re.match(r"^\d+\. ", line):
        flush_paragraph()
        number, content = line.split(". ", 1)
        story.append(Paragraph(inline_markup(content), styles["BulletX"], bulletText=number + "."))
    elif not line:
        flush_paragraph()
    else:
        paragraph.append(line)
flush_paragraph()

doc.build(story)
print(OUTPUT)
