from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT = "output/pdf/spurious_regression_stationary_review_report.pdf"

NAVY = colors.HexColor("#16324F")
BLUE = colors.HexColor("#2E5E88")
PALE_BLUE = colors.HexColor("#EAF1F7")
PALE_RED = colors.HexColor("#FBECEC")
PALE_AMBER = colors.HexColor("#FFF5DC")
GREY = colors.HexColor("#5B6670")
LIGHT_GREY = colors.HexColor("#E4E8EB")
DARK = colors.HexColor("#20262C")


def register_fonts():
    candidates = [
        ("Body", "/System/Library/Fonts/Supplemental/Times New Roman.ttf"),
        ("Body-Bold", "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"),
        ("Body-Italic", "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf"),
    ]
    for name, path in candidates:
        try:
            pdfmetrics.registerFont(TTFont(name, path))
        except Exception:
            pass
    if "Body" not in pdfmetrics.getRegisteredFontNames():
        return "Times-Roman", "Times-Bold", "Times-Italic"
    return "Body", "Body-Bold", "Body-Italic"


BODY, BOLD, ITALIC = register_fonts()


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="ReportTitle", fontName=BOLD, fontSize=22, leading=26,
    textColor=NAVY, alignment=TA_LEFT, spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="Subtitle", fontName=BODY, fontSize=11, leading=16,
    textColor=GREY, spaceAfter=18,
))
styles.add(ParagraphStyle(
    name="H1x", fontName=BOLD, fontSize=15, leading=19,
    textColor=NAVY, spaceBefore=12, spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="H2x", fontName=BOLD, fontSize=11.5, leading=15,
    textColor=BLUE, spaceBefore=9, spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="Bodyx", fontName=BODY, fontSize=9.5, leading=13.7,
    textColor=DARK, spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="Small", fontName=BODY, fontSize=8, leading=11,
    textColor=GREY,
))
styles.add(ParagraphStyle(
    name="TableHeader", fontName=BOLD, fontSize=8, leading=10,
    textColor=colors.white,
))
styles.add(ParagraphStyle(
    name="FindingTitle", fontName=BOLD, fontSize=10, leading=13,
    textColor=NAVY, spaceAfter=3,
))
styles.add(ParagraphStyle(
    name="Bulletx", fontName=BODY, fontSize=9.3, leading=13.2,
    leftIndent=13, firstLineIndent=-8, bulletIndent=2, spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="Equation", fontName=BODY, fontSize=10, leading=15,
    leftIndent=14, textColor=DARK, spaceBefore=4, spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="Callout", fontName=BODY, fontSize=9.5, leading=14,
    textColor=DARK,
))


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(LIGHT_GREY)
    canvas.setLineWidth(0.5)
    canvas.line(20 * mm, height - 16 * mm, width - 20 * mm, height - 16 * mm)
    canvas.setFont(BODY, 7.5)
    canvas.setFillColor(GREY)
    canvas.drawString(20 * mm, height - 12.5 * mm, "Review report: spurious_regression_stationary.qmd")
    canvas.drawRightString(width - 20 * mm, 11 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=20 * mm,
    leftMargin=20 * mm,
    topMargin=22 * mm,
    bottomMargin=18 * mm,
    title="Review Report: Spurious Regression in Stationary Time Series",
    author="Codex",
)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
doc.addPageTemplates(PageTemplate(id="report", frames=[frame], onPage=header_footer))


story = []


def p(text, style="Bodyx"):
    story.append(Paragraph(text, styles[style]))


def bullet(text):
    story.append(Paragraph(text, styles["Bulletx"], bulletText="-"))


def finding(priority, title, lines, body, recommendation):
    bg = PALE_RED if priority == "P1" else PALE_AMBER
    badge = Paragraph(f"<b>{priority}</b>", styles["Small"])
    content = Paragraph(
        f"<b>{title}</b><br/><font color='#5B6670'>Source lines: {lines}</font>",
        styles["FindingTitle"],
    )
    table = Table([[badge, content]], colWidths=[13 * mm, 142 * mm], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), bg),
        ("BOX", (0, 0), (0, 0), 0.6, colors.HexColor("#D6A5A5") if priority == "P1" else colors.HexColor("#D9BE76")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 5),
        ("RIGHTPADDING", (0, 0), (0, 0), 5),
        ("TOPPADDING", (0, 0), (0, 0), 5),
        ("BOTTOMPADDING", (0, 0), (0, 0), 5),
        ("LEFTPADDING", (1, 0), (1, 0), 8),
        ("TOPPADDING", (1, 0), (1, 0), 1),
        ("BOTTOMPADDING", (1, 0), (1, 0), 2),
    ]))
    block = [table, Spacer(1, 3), Paragraph(body, styles["Bodyx"]),
             Paragraph(f"<b>Recommended revision:</b> {recommendation}", styles["Bodyx"]), Spacer(1, 4)]
    story.append(KeepTogether(block))


story.append(Spacer(1, 15 * mm))
p("Review Report", "ReportTitle")
p("<i>Is Spurious Regression a Problem in Stationary Time Series?</i>", "Subtitle")

meta = Table([
    ["Reviewed source", "spurious_regression_stationary.qmd"],
    ["Scope", "Theory, Monte Carlo design, results, conclusions, reproducibility, and presentation"],
    ["Review date", "6 August 2026"],
    ["Recommendation", "Major revision"],
], colWidths=[37 * mm, 118 * mm])
meta.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), PALE_BLUE),
    ("TEXTCOLOR", (0, 0), (0, -1), NAVY),
    ("FONTNAME", (0, 0), (0, -1), BOLD),
    ("FONTNAME", (1, 0), (1, -1), BODY),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("LEADING", (0, 0), (-1, -1), 12),
    ("GRID", (0, 0), (-1, -1), 0.35, LIGHT_GREY),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 7),
    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(meta)
story.append(Spacer(1, 12 * mm))
p("Overall assessment", "H1x")
p("The paper asks a useful question and presents a clear equal-parameter AR(1) example. The central special-case calculation - that conventional OLS standard errors cause persistent over-rejection when two independent AR(1) series share a positive autoregressive coefficient - is sound and is well illustrated by the simulation.")
p("However, the document generalizes this special result too far. Stationarity and serial correlation alone do not determine whether conventional inference over-rejects. The sign and magnitude of the long-run covariance of the score process determine the distortion: it may be positive, negative, or zero. The classical random-walk section also contains an incorrect scaling of the OLS slope. These issues affect the theorem, abstract-style introduction, and conclusion, so major revision is warranted before the report is treated as theoretically reliable.")

callout = Table([[Paragraph(
    "<b>Bottom line.</b> Retain the positive equal-phi AR(1) example, but replace universal statements about serially correlated stationary processes with statements conditional on the long-run variance ratio lambda. Correct the random-walk limit and add a HAC Monte Carlo comparison.",
    styles["Callout"]) ]], colWidths=[155 * mm])
callout.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE),
    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#A9C0D2")),
    ("LEFTPADDING", (0, 0), (-1, -1), 9),
    ("RIGHTPADDING", (0, 0), (-1, -1), 9),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.append(callout)

story.append(PageBreak())
p("1. Theoretical review", "H1x")

finding(
    "P1", "Incorrect random-walk slope scaling", "135-138",
    "The document states that T<super>-1</super> beta-hat converges to a nondegenerate Brownian functional. In a levels regression of one independent random walk on another, beta-hat is O<sub>p</sub>(1) and beta-hat itself has a nondegenerate limit. Therefore T<super>-1</super> beta-hat converges to zero. The displayed functional is also not the standard demeaned-Brownian expression for a regression with an intercept.",
    "Replace the display with the limit of beta-hat based on demeaned Brownian motions: integral[(W<sub>x</sub>-mean W<sub>x</sub>)(W<sub>y</sub>-mean W<sub>y</sub>)] divided by integral[(W<sub>x</sub>-mean W<sub>x</sub>)<super>2</super>]. Keep the separate statement that the conventional t statistic diverges."
)

finding(
    "P1", "Serial correlation does not imply lambda greater than one", "226-251",
    "The proposition is initially qualified by nonnegative autocovariances, but the subsequent interpretation drops that qualification and treats any serial correlation as implying over-rejection. In general, lambda equals one plus twice the sum of nonzero-lag score autocovariances divided by the contemporaneous variance. That sum can be positive, negative, or zero.",
    "State the result in three cases: lambda greater than one gives over-rejection; lambda less than one gives under-rejection; lambda equal to one gives correct asymptotic size. Avoid equating serial dependence with positive long-run covariance."
)

finding(
    "P1", "The if-and-only-if characterization is false", "231-234",
    "The statement that lambda equals one if and only if the product process is serially uncorrelated is too strong. Serial autocovariances can cancel in the long-run sum even when individual lag covariances are nonzero.",
    "Replace it with: serial uncorrelatedness is sufficient for lambda = 1; more generally, lambda = 1 whenever the sum of all nonzero-lag autocovariances is zero."
)

finding(
    "P1", "Long-run variance notation omits demeaning", "207-245 and 343",
    "The score process is defined as w<sub>t</sub> = (x<sub>t</sub>-mu<sub>x</sub>)u<sub>t</sub>, but later expressions use LRV(x<sub>t</sub>u<sub>t</sub>). These are not generally identical when the regressor has a nonzero mean.",
    "Use LRV((x<sub>t</sub>-mu<sub>x</sub>)u<sub>t</sub>) consistently, or explicitly impose mu<sub>x</sub> = 0."
)

story.append(PageBreak())
p("1. Theoretical review (continued)", "H1x")

finding(
    "P1", "Finite-sample exactness requires stronger conditions", "256-261 and 337-340",
    "Serially uncorrelated stationary x and y do not by themselves imply an exact Student-t statistic. Exact conditional regression inference requires, at minimum for this setup, independent Gaussian regression errors with constant variance; serial uncorrelatedness plus finite moments is insufficient. The phrase 'Gaussian innovations' is also ambiguous outside a fully specified process.",
    "Separate the asymptotic result from the exact finite-sample result. Say that lambda = 1 yields asymptotic standard normal inference. Reserve exact Student-t inference for the explicitly i.i.d. Gaussian y-error case independent of the regressor matrix."
)

finding(
    "P1", "The main theorem overgeneralizes the AR(1) example", "333-349",
    "The theorem claims that all serially correlated stationary series produce rejection strictly above 5 percent. A simple counterexample uses independent AR(1) processes with coefficients phi<sub>x</sub> and phi<sub>y</sub> of opposite signs. Then lambda = (1 + phi<sub>x</sub>phi<sub>y</sub>)/(1 - phi<sub>x</sub>phi<sub>y</sub>), which is below one, so the conventional test under-rejects.",
    "Rewrite the theorem around lambda rather than around the presence or absence of serial correlation. Present the equal-positive-phi model as an important example, not a universal stationary result."
)

finding(
    "P1", "The HAC proposition lacks sufficient regularity conditions", "313-329",
    "A central limit theorem for the score does not, by itself, guarantee consistency of a Newey-West long-run variance estimator. HAC consistency requires additional dependence and moment restrictions plus explicit kernel and bandwidth-rate conditions.",
    "Add a separate HAC-consistency assumption or cite a theorem with matching mixing, moment, kernel, and bandwidth conditions. Replace 'any stationary, mixing DGP' with a qualified class satisfying those conditions."
)

finding(
    "P2", "The unit-root exclusivity claim is too categorical", "295-309, 345-346, and 555-559",
    "The analysis establishes a contrast between fixed-parameter short-memory stationary processes and independent random walks. It does not establish that unit roots are the only source of divergent or nonstandard t statistics. Other forms of nonstationarity, long memory, parameter sequences approaching unity, structural change, and violations of the stated CLT can also invalidate conventional asymptotics.",
    "Limit the conclusion to the regimes actually analyzed. Use wording such as 'in the independent random-walk benchmark' instead of 'only for unit-root data.'"
)

story.append(PageBreak())
p("2. Monte Carlo design", "H1x")
p("The simulation engine is efficient and the revised invariant-distribution initialization correctly makes the retained AR(1) observations stationary from the first observation. The running-sum formulas for OLS with an intercept are correct. The fixed seed and 4,000 replications support reproducibility.")

design_rows = [
    [Paragraph("Element", styles["TableHeader"]), Paragraph("Assessment", styles["TableHeader"]), Paragraph("Recommended action", styles["TableHeader"])],
    [Paragraph("DGP coverage", styles["Bodyx"]), Paragraph("Only equal, positive AR coefficients are considered. This selects cases with positive score autocorrelation and over-rejection.", styles["Bodyx"]), Paragraph("Add unequal coefficients and at least one opposite-sign pair.", styles["Bodyx"])],
    [Paragraph("HAC remedy", styles["Bodyx"]), Paragraph("The paper recommends HAC inference but never simulates it.", styles["Bodyx"]), Paragraph("Report conventional and HAC rejection rates side by side.", styles["Bodyx"])],
    [Paragraph("Nested samples", styles["Bodyx"]), Paragraph("Nesting induces correlation and smoother visual comparisons, but does not eliminate between-T Monte Carlo noise.", styles["Bodyx"]), Paragraph("Revise the description; optionally add pointwise Monte Carlo bands.", styles["Bodyx"])],
    [Paragraph("Critical values", styles["Bodyx"]), Paragraph("Student-t critical values are appropriate for the finite-sample implementation and converge to the normal benchmark used in theory.", styles["Bodyx"]), Paragraph("Retain, but state the distinction clearly.", styles["Bodyx"])],
    [Paragraph("Uncertainty", styles["Bodyx"]), Paragraph("The maximum standard error calculation is correct, but curves and the table show no uncertainty intervals.", styles["Bodyx"]), Paragraph("Add 95 percent Monte Carlo intervals or a note at selected T values.", styles["Bodyx"])],
]
design_table = Table(design_rows, colWidths=[28 * mm, 74 * mm, 53 * mm], repeatRows=1)
design_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), BOLD),
    ("GRID", (0, 0), (-1, -1), 0.35, LIGHT_GREY),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FA")]),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(design_table)

p("Suggested expanded stationary design", "H2x")
bullet("Baseline: (phi<sub>x</sub>, phi<sub>y</sub>) = (0, 0), retaining the i.i.d. Gaussian case.")
bullet("Positive-product cases: (0.5, 0.5), (0.8, 0.8), and (0.9, 0.9), retaining the current comparison.")
bullet("Negative-product cases: (0.8, -0.8) and (0.9, -0.5), demonstrating asymptotic under-rejection.")
bullet("Unequal positive case: (0.9, 0.5), showing that the relevant persistence parameter is the product phi<sub>x</sub>phi<sub>y</sub>.")
bullet("For every stationary DGP, report conventional and HAC rejection frequencies, with the theoretical conventional plateau where available.")

p("General AR(1) benchmark", "H2x")
p("For independent zero-mean AR(1) processes with possibly different coefficients, the score autocorrelation at lag k is (phi<sub>x</sub>phi<sub>y</sub>)<super>k</super>. Therefore:", "Bodyx")
p("lambda = (1 + phi<sub>x</sub> phi<sub>y</sub>) / (1 - phi<sub>x</sub> phi<sub>y</sub>).", "Equation")
p("This one formula supplies a clean simulation diagnostic and directly exposes the limitation of the current equal-positive-phi design.")

story.append(PageBreak())
p("3. Review of reported results", "H1x")

saved = [
    ["DGP", "T = 50", "T = 5000", "Asymptotic"],
    ["i.i.d.", "5.20%", "4.45%", "5.00%"],
    ["phi = 0.5", "11.33%", "12.18%", "12.90%"],
    ["phi = 0.8", "33.05%", "35.63%", "35.85%"],
    ["phi = 0.9", "46.65%", "52.08%", "52.54%"],
    ["phi = 0.95", "54.63%", "65.50%", "65.73%"],
    ["I(1)", "65.25%", "96.58%", "100% limit"],
]
result_table = Table(saved, colWidths=[40 * mm, 35 * mm, 40 * mm, 40 * mm])
result_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), BOLD),
    ("FONTNAME", (0, 1), (-1, -1), BODY),
    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
    ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FA")]),
    ("GRID", (0, 0), (-1, -1), 0.35, LIGHT_GREY),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(result_table)
p("Source: saved simulation outputs in scripts/spurious_comparison_table.csv and scripts/spurious_rejection_frequency_series.csv.", "Small")

finding(
    "P2", "The 'majority at every sample size' statement is contradicted by the output", "288-293",
    "At T = 50, the phi = 0.9 rejection frequency is 46.65 percent, not a majority. The phi = 0.5 and phi = 0.8 cases are also well below one half. Only the phi = 0.95 case exceeds one half at T = 50.",
    "Say that sufficiently persistent positive-phi processes can reject a majority of the time asymptotically; do not claim this for every persistent DGP or every sample size."
)

finding(
    "P2", "A plateau is not finite-sample invariance", "491-500 and 543-547",
    "The results approach theoretical plateaus, but rejection frequencies change materially between T = 50 and T = 200 for the more persistent DGPs. Increasing sample size removes transient effects; it does not correct the conventional standard error's limiting distortion.",
    "Replace 'invariant to sample size' and 'does nothing' with 'converges to a non-nominal plateau, so increasing T alone does not eliminate the asymptotic distortion.'"
)

finding(
    "P2", "The white-noise wording should distinguish theory from simulation", "486-489 and 539-541",
    "The i.i.d. Gaussian test is theoretically exact when the conditional regression assumptions hold, but a Monte Carlo rejection frequency is not literally 5 percent at every T. For example, the saved frequency is 4.45 percent at T = 5000. This is ordinary Monte Carlo variation and is consistent with 5 percent.",
    "State that the simulated values fluctuate around 5 percent and are statistically consistent with exact theoretical size."
)

story.append(PageBreak())
p("4. Recommended revision structure", "H1x")

roadmap_raw = [
    ["Order", "Revision", "Purpose"],
    ["1", "Correct the random-walk limit", "Remove the principal mathematical error before revising surrounding prose."],
    ["2", "Restate the stationary theorem in terms of lambda", "Make over-rejection, under-rejection, and correct-size cases explicit."],
    ["3", "Strengthen HAC assumptions", "Ensure the proposed remedy follows from stated conditions."],
    ["4", "Generalize the AR(1) example to phi_x and phi_y", "Provide an intuitive counterexample and a stronger bridge to the theorem."],
    ["5", "Expand the Monte Carlo design", "Add opposite-sign persistence and HAC inference."],
    ["6", "Rewrite the results and conclusion", "Align claims with finite-sample output and the corrected theory."],
    ["7", "Clean presentation and reproducibility details", "Resolve wording, appendix completeness, and unused packages."],
]
roadmap = [[Paragraph(cell, styles["TableHeader"] if row_i == 0 else styles["Bodyx"])
            for cell in row] for row_i, row in enumerate(roadmap_raw)]
rt = Table(roadmap, colWidths=[14 * mm, 58 * mm, 83 * mm], repeatRows=1)
rt.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), BOLD),
    ("FONTNAME", (0, 1), (-1, -1), BODY),
    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
    ("LEADING", (0, 0), (-1, -1), 11),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FA")]),
    ("GRID", (0, 0), (-1, -1), 0.35, LIGHT_GREY),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ALIGN", (0, 1), (0, -1), "CENTER"),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(rt)

p("Suggested replacement for the central conclusion", "H2x")
conclusion = Table([[Paragraph(
    "For independent stationary processes satisfying an appropriate central limit theorem, the OLS slope is consistent for zero. Conventional OLS inference is nevertheless valid only when its variance estimator matches the long-run variance of the score process. If the long-run variance ratio lambda exceeds one, the conventional test over-rejects; if lambda is below one, it under-rejects; and if lambda equals one, it has correct asymptotic size. Equal, positively persistent AR(1) processes provide an important over-rejection case, while HAC inference restores asymptotic validity under additional regularity conditions.",
    styles["Callout"]) ]], colWidths=[155 * mm])
conclusion.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE),
    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#A9C0D2")),
    ("LEFTPADDING", (0, 0), (-1, -1), 9),
    ("RIGHTPADDING", (0, 0), (-1, -1), 9),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.append(conclusion)

p("Editorial and reproducibility notes", "H2x")
bullet("Change 'continuously from T = 50 to 5000' to 'on a grid from T = 50 to 5000 in increments of 50.'")
bullet("Change 'three-part answer' to 'four-part answer,' or consolidate the list.")
bullet("The Appendix claims to reproduce complete code but omits the standalone script's output-writing commands.")
bullet("dplyr and tidyr are loaded but unused in the displayed implementation.")
bullet("Use 'Monte Carlo standard error' consistently and consider reporting confidence intervals for selected rejection frequencies.")
bullet("Avoid describing all real economic time series as positively persistent; the theoretical result depends on the score's long-run covariance, not merely on persistence in each series.")

p("Final recommendation", "H1x")
p("Major revision. The paper has a valuable motivating example and a useful simulation framework, but the theoretical statements must be narrowed and corrected. Once the random-walk limit, lambda-based classification, HAC assumptions, and simulation scope are repaired, the document can make a clear contribution: stationarity secures consistency under suitable conditions, but it does not by itself validate conventional OLS inference.")

doc.build(story)
print(OUTPUT)
