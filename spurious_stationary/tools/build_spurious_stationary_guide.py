from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
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


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "spurious_stationary_sim_explained.pdf"

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#2D6A9F")
SKY = colors.HexColor("#EAF3F8")
GOLD = colors.HexColor("#D8A13B")
INK = colors.HexColor("#24313B")
MUTED = colors.HexColor("#5E6C76")
LINE = colors.HexColor("#CBD6DD")
PALE = colors.HexColor("#F6F8FA")


class GuideDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="body",
        )
        self.addPageTemplates(PageTemplate(id="guide", frames=[frame], onPage=self.decorate))

    def decorate(self, canvas, doc):
        canvas.saveState()
        width, height = A4
        canvas.setFillColor(NAVY)
        canvas.rect(0, height - 13 * mm, width, 13 * mm, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 8.5)
        canvas.drawString(18 * mm, height - 8.5 * mm, "SPURIOUS STATIONARY SIMULATION - CODE GUIDE")
        canvas.setStrokeColor(GOLD)
        canvas.setLineWidth(1.2)
        canvas.line(18 * mm, 15 * mm, width - 18 * mm, 15 * mm)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(18 * mm, 10.2 * mm, "scripts/spurious_stationary_sim.R")
        canvas.drawRightString(width - 18 * mm, 10.2 * mm, f"Page {doc.page}")
        canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="TitleGuide", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=25, leading=29, textColor=NAVY, alignment=TA_LEFT,
    spaceAfter=9 * mm,
))
styles.add(ParagraphStyle(
    name="SubtitleGuide", parent=styles["Normal"], fontName="Helvetica",
    fontSize=12, leading=17, textColor=MUTED, spaceAfter=7 * mm,
))
styles.add(ParagraphStyle(
    name="H1Guide", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=17, leading=21, textColor=NAVY, spaceBefore=3 * mm,
    spaceAfter=4 * mm,
))
styles.add(ParagraphStyle(
    name="H2Guide", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=12, leading=15, textColor=BLUE, spaceBefore=3.5 * mm,
    spaceAfter=2 * mm,
))
styles.add(ParagraphStyle(
    name="BodyGuide", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=9.5, leading=14, textColor=INK, spaceAfter=2.8 * mm,
))
styles.add(ParagraphStyle(
    name="BulletGuide", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=9.3, leading=13.5, textColor=INK, leftIndent=5 * mm,
    firstLineIndent=-3 * mm, bulletIndent=1.5 * mm, spaceAfter=1.5 * mm,
))
styles.add(ParagraphStyle(
    name="Callout", parent=styles["BodyText"], fontName="Helvetica-Bold",
    fontSize=9.5, leading=14, textColor=NAVY, backColor=SKY,
    borderColor=BLUE, borderWidth=0.7, borderPadding=7, spaceBefore=2 * mm,
    spaceAfter=4 * mm,
))
styles.add(ParagraphStyle(
    name="CodeGuide", parent=styles["Code"], fontName="Courier",
    fontSize=8.3, leading=11, textColor=INK, backColor=PALE,
    borderColor=LINE, borderWidth=0.5, borderPadding=6, spaceAfter=3 * mm,
))
styles.add(ParagraphStyle(
    name="TableHead", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=8.3, leading=10.5, textColor=colors.white, alignment=TA_LEFT,
))
styles.add(ParagraphStyle(
    name="TableCell", parent=styles["Normal"], fontName="Helvetica",
    fontSize=8, leading=10.5, textColor=INK,
))
styles.add(ParagraphStyle(
    name="Small", parent=styles["Normal"], fontName="Helvetica",
    fontSize=8.2, leading=11.5, textColor=MUTED,
))


def p(text, style="BodyGuide"):
    return Paragraph(text, styles[style])


def bullet(text):
    return Paragraph(f"- {text}", styles["BulletGuide"])


def table(headers, rows, widths):
    data = [[p(h, "TableHead") for h in headers]]
    data += [[p(str(cell), "TableCell") for cell in row] for row in rows]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
    ]))
    return t


story = []
story += [Spacer(1, 18 * mm), p("Spurious Regression in Stationary Time Series", "TitleGuide")]
story += [p("A guided explanation of <b>spurious_stationary_sim.R</b>: what it simulates, how its inference works, and how every table and figure is produced.", "SubtitleGuide")]
story += [p("PURPOSE", "H2Guide")]
story += [p(
    "The script is the computational companion to the handout <i>Is Spurious Regression a Problem in Stationary Time Series?</i>. "
    "Its central question is whether two unrelated but serially dependent stationary series can produce misleading OLS significance. "
    "It compares conventional, heteroskedasticity-robust (HC0), and Bartlett HAC inference across several data-generating processes (DGPs)."
)]
story += [p(
    "The main conclusion encoded by the simulation is precise: stationarity alone does not guarantee that the usual OLS standard error is valid. "
    "The behavior of the score process x_t u_t matters. Conventional inference can be oversized, correctly sized, or conservative depending on its long-run variance.",
    "Callout",
)]
story += [p("AT A GLANCE", "H2Guide")]
story += [table(
    ["Layer", "Role in the script"],
    [
        ("Configuration", "Selects sample sizes, replication counts, significance level, and independent random seeds."),
        ("Primitives", "Generates AR(1) and MA(2) processes and computes Bartlett long-run variance estimators."),
        ("Inference", "Computes slope estimates plus conventional, HC0, and HAC t-ratios."),
        ("Experiments", "Runs the baseline DGP grid and four extensions: common volatility, local-to-unity, Granger tests, and local power."),
        ("Presentation", "Builds accessor functions, six ggplot figures, nine CSV tables, and a session-information file."),
    ],
    [37 * mm, 123 * mm],
)]
story += [Spacer(1, 6 * mm), p("Reading time: about 12 minutes", "Small"), PageBreak()]

story += [p("1. Configuration and reproducibility", "H1Guide")]
story += [p(
    "The opening block loads only <b>ggplot2</b> and <b>scales</b>. All HAC calculations are implemented directly, so the same covariance estimator is used throughout. "
    "The maximum path length is T = 5,000. Conventional rejection frequencies are evaluated every 50 observations, while the more expensive HAC calculations use six selected sample sizes."
)]
story += [p("quick &lt;- nzchar(Sys.getenv(\"SPURIOUS_QUICK\"))<br/>Nsim_main &lt;- if (quick) 200 else 2000", "CodeGuide")]
story += [p(
    "Setting <b>SPURIOUS_QUICK=1</b> reduces every experiment to 200 replications. This is a smoke-test and drafting mode: it exercises the complete code path, but its Monte Carlo estimates are noisier. "
    "The standard mode uses between 1,000 and 2,000 replications depending on the experiment."
)]
story += [p("Why separate seeds?", "H2Guide")]
story += [p(
    "Each experiment has its own seed. Changing the DGP list or replication count in one section therefore does not silently alter numerical results in later sections. "
    "This is an important reproducibility feature for a document whose prose retrieves simulation values dynamically."
)]
story += [table(
    ["Object", "Meaning"],
    [
        ("Tmax", "Longest simulated trajectory: 5,000 observations."),
        ("grid", "50, 100, ..., 5,000 for conventional OLS curves."),
        ("selected_T", "50, 200, 500, 1,000, 2,000, 5,000 for HAC and extensions."),
        ("alpha", "Nominal test size, fixed at 5 percent."),
        ("seeds", "Named seed vector, one entry per experiment."),
    ],
    [43 * mm, 117 * mm],
)]
story += [p("Run modes", "H2Guide")]
story += [p("SPURIOUS_QUICK=1 SPURIOUS_OUTPUT_DIR=/tmp/sim Rscript scripts/spurious_stationary_sim.R", "CodeGuide")]
story += [p(
    "Without environment variables, the full simulation runs and writes into <b>scripts/</b>. SPURIOUS_OUTPUT_DIR can redirect generated artifacts, which is useful for tests and avoids replacing tracked results."
), PageBreak()]

story += [p("2. Time-series generators and theoretical benchmark", "H1Guide")]
story += [p("Stationary AR(1)", "H2Guide")]
story += [p(
    "<b>draw_ar1(n, phi)</b> generates z_t = phi z_(t-1) + e_t. Its initial value is drawn from the invariant Gaussian distribution with variance 1/(1 - phi^2). "
    "The path is therefore stationary from its first retained observation; no burn-in is needed. The function requires |phi| &lt; 1."
)]
story += [p("Invertible MA(2)", "H2Guide")]
story += [p(
    "<b>draw_ma2</b> constructs z_t = e_t + theta1 e_(t-1) + theta2 e_(t-2) by one-sided convolution. It draws two extra innovations and drops the two leading missing values. "
    "<b>ma2_acf</b> supplies the exact autocorrelations at lags 0, 1, and 2."
)]
story += [p("The variance-ratio benchmark", "H2Guide")]
story += [p(
    "For independent stationary x_t and y_t, the conventional slope t-ratio need not converge to a standard normal distribution. Its asymptotic variance is summarized by lambda, the ratio between the score's long-run variance and the variance implicitly used by the conventional standard error. "
    "For independent AR(1) series with coefficients phi_x and phi_y:"
)]
story += [p("lambda = (1 + phi_x phi_y) / (1 - phi_x phi_y)", "Callout")]
story += [bullet("If lambda &gt; 1, conventional t-ratios are too dispersed and the test over-rejects.")]
story += [bullet("If lambda = 1, conventional inference is asymptotically correctly sized.")]
story += [bullet("If lambda &lt; 1, conventional inference is conservative.")]
story += [p(
    "The script converts lambda into a theoretical two-sided rejection probability at a nominal 5 percent critical value. This provides a population benchmark for the simulated rejection curves."
)]
story += [p("A deliberate counterexample", "H2Guide")]
story += [p(
    "The AR/MA design chooses MA(2) coefficients so that lambda equals exactly one even though both x and y are visibly autocorrelated. This demonstrates that serial correlation by itself does not imply invalid conventional inference; the relevant autocorrelation is that of the regression score."
), PageBreak()]

story += [p("3. Conventional, HC0, and HAC inference", "H1Guide")]
story += [p(
    "<b>slope_t_stats(x, y)</b> is the core inference function. It centers both series, computes the simple-regression slope, forms residuals, and defines the score as centered x multiplied by the residual. It then returns three t-ratios for the same coefficient estimate."
)]
story += [table(
    ["Method", "What the standard error assumes or estimates"],
    [
        ("Conventional OLS", "Uses residual variance divided by the centered sum of squares of x. Valid under the usual homoskedastic, serially uncorrelated score conditions."),
        ("HC0", "Uses squared observation-level scores. Allows heteroskedasticity, but does not add lagged score covariances."),
        ("HAC", "Uses a Bartlett estimate of the score's long-run variance, including weighted autocovariances through bandwidth L."),
    ],
    [38 * mm, 122 * mm],
)]
story += [p("Bartlett HAC implementation", "H2Guide")]
story += [p(
    "<b>hac_lrv</b> handles a scalar score; <b>hac_lrv_matrix</b> handles vector scores for multivariate regressions. At lag j, the Bartlett weight is 1 - j/(L + 1). "
    "The bandwidth rule is L = floor(2 T^(1/3)), which grows with T but remains small relative to T. A degrees-of-freedom multiplier T/(T-k) is applied consistently."
)]
story += [p(
    "HAC is consistent under suitable weak-dependence conditions, but it can be noisy in short samples. The code therefore distinguishes theoretical validity from finite-sample performance rather than assuming HAC must dominate at every T.",
    "Callout",
)]
story += [p("Test decisions", "H2Guide")]
story += [p(
    "<b>slope_rejections</b> compares the absolute t-ratios with a Student-t critical value using T - 2 degrees of freedom. The conventional statistic has that reference under exact Gaussian classical conditions. "
    "HC0 and HAC have standard-normal limits; using the t cutoff for them is a small finite-sample concession that becomes negligible as T grows."
)]
story += [p("Computational shortcut in the main experiment", "H2Guide")]
story += [p(
    "For each replication, <b>simulate_dgp</b> draws one length-5,000 trajectory. It evaluates every smaller T as a nested prefix. Running sums of x, y, x squared, y squared, and xy make the conventional statistic inexpensive over the full grid. "
    "HAC cannot be updated by the same simple recursion, so it is computed only at selected sample sizes."
), PageBreak()]

story += [p("4. Baseline DGP registry", "H1Guide")]
story += [p(
    "The registry stores a display name, process type, theoretical lambda, and a draw function. This design keeps simulation machinery generic: <b>simulate_dgp</b> does not need special-case logic for each process."
)]
story += [table(
    ["DGP", "Interpretation", "Expected conventional behavior"],
    [
        ("iid", "Independent white noise series.", "lambda = 1; correct size."),
        ("(0.5, 0.5)", "Independent moderately persistent AR(1) series.", "Some over-rejection."),
        ("(0.8, 0.8)", "Independent persistent AR(1) series.", "Substantial over-rejection."),
        ("(0.9, 0.9)", "Independent highly persistent AR(1) series.", "Severe over-rejection."),
        ("(0.95, 0.95)", "Independent near-unit-root stationary AR(1) series.", "Very severe over-rejection."),
        ("(0.9, 0.5)", "Unequal persistence.", "Over-rejection driven by the product of coefficients."),
        ("(0.8, -0.8)", "Opposite-signed serial dependence.", "lambda &lt; 1; conservative inference."),
        ("AR/MA lambda=1", "Autocorrelated AR(1) and MA(2), calibrated exactly.", "Correct size despite autocorrelation."),
        ("I(1)", "Independent random walks.", "Nonstationary spurious-regression benchmark."),
    ],
    [33 * mm, 73 * mm, 54 * mm],
)]
story += [p("What is saved", "H2Guide")]
story += [p(
    "The conventional results contain 100 sample-size points per DGP; the HAC results contain six. Each reported rejection proportion also receives a Monte Carlo standard error, sqrt(p(1-p)/N). "
    "Comparison tables merge simulated values with lambda and the theoretical rejection limit."
)]
story += [p(
    "Interpret curves horizontally with care: all T values within a replication use prefixes of the same path, so adjacent points are dependent. This is efficient and appropriate for showing convergence, but the plotted fluctuations are not independent Monte Carlo estimates.",
    "Callout",
), PageBreak()]

story += [p("5. Four extensions", "H1Guide")]
story += [p("A. Common stochastic volatility", "H2Guide")]
story += [p(
    "x_t and y_t share the scale s_t = exp(h_t/2) but have independent Gaussian signs. Their population projection slope is zero, yet they are dependent. "
    "The score is serially uncorrelated, while its variance is inflated by common volatility. Consequently lambda = exp(Var(h)) &gt; 1. HC0 should fix the key distortion; HAC is also valid but can be less precise."
)]
story += [p("B. Stationary-start local-to-unity sequences", "H2Guide")]
story += [p(
    "For each T, phi_T = 1 - c/T with c = 5. Every finite-T process is stationary, but the DGP changes with sample size and approaches the unit-root boundary. "
    "The initial state is drawn from the stationary distribution, giving a stationary-start limit. A zero-start design would be a different experiment with materially different finite-sample behavior."
)]
story += [p("C. Distributed lags and Granger noncausality", "H2Guide")]
story += [p(
    "Independent AR(1) x and y series are used to test jointly whether two lags of x predict y. The correct model includes lagged y; the misspecified model omits it. "
    "Because x and y are independent, the population coefficients on x remain zero even in the omitted-lag model. Thus excess rejection is a covariance-estimation problem, not omitted-variable bias."
)]
story += [p(
    "The code estimates each regression by matrix algebra, constructs conventional and matrix-HAC covariance estimates, and performs a two-degree-of-freedom Wald test. Numerically singular covariance matrices produce NA rather than stopping the simulation; those replications are omitted from the corresponding mean."
)]
story += [p("D. Size-adjusted local power", "H2Guide")]
story += [p(
    "The alternative is y_t = (b/sqrt(T)) x_t + v_t, with independent AR(1) x and v. For each method and T, the script estimates the 95th percentile of |t| under b = 0 and uses that empirical critical value for all nonzero b values. "
    "This removes size differences before comparing power. Otherwise an oversized conventional test would appear more powerful simply because it rejects too often under the null."
)]
story += [p(
    "As an additional theoretical check, the conventional empirical critical value should approach 1.96 sqrt(lambda), while the HAC critical value should approach 1.96.",
    "Callout",
), PageBreak()]

story += [p("6. Accessors, plots, and exported artifacts", "H1Guide")]
story += [p("Fail-loudly accessors", "H2Guide")]
story += [p(
    "The handout does not duplicate numerical results in prose. Functions such as <b>rp</b>, <b>asy_of</b>, <b>gr_rej</b>, and <b>pw_cv</b> retrieve exact simulation entries during rendering. "
    "The helper <b>.one</b> requires exactly one match after removing missing values. A renamed DGP, wrong sample size, or duplicated row therefore raises an error instead of silently inserting a wrong number."
)]
story += [p("Six figures", "H2Guide")]
story += [table(
    ["Object", "Question answered"],
    [
        ("p1", "How does conventional OLS rejection evolve with T across stationary and I(1) designs?"),
        ("p2", "How much does HAC repair conventional inference for stationary designs?"),
        ("p3", "Does HC0 suffice when distortion comes from contemporaneous common volatility?"),
        ("p4", "What happens along stationary sequences approaching a unit root?"),
        ("p5", "How do specification and covariance choice affect a Granger Wald test?"),
        ("p6", "How do size-adjusted conventional and HAC power compare?"),
    ],
    [24 * mm, 136 * mm],
)]
story += [p(
    "Sample size is shown on a log scale in the relevant figures, preventing the high-T range from consuming most of the horizontal space. A horizontal line marks the nominal 5 percent rejection rate."
)]
story += [p("Output contract", "H2Guide")]
story += [bullet("Six one-page PDF figures are saved with stable descriptive names.")]
story += [bullet("Nine CSV files preserve the underlying series and comparison tables.")]
story += [bullet("sessionInfo.txt records the R version, platform, and attached packages.")]
story += [bullet("The plot objects p1 through p6 remain in the sourcing environment for direct use by the handout.")]
story += [p(
    "The script intentionally does not print plot objects. Sourcing it therefore does not create an accidental Rplots.pdf. A final message confirms the chosen output directory."
), PageBreak()]

story += [p("7. How to interpret and validate the script", "H1Guide")]
story += [p("Interpretation checklist", "H2Guide")]
story += [bullet("Do not equate stationarity with valid conventional standard errors.")]
story += [bullet("Use lambda to connect serial dependence to asymptotic size distortion.")]
story += [bullet("Distinguish score autocorrelation from heteroskedasticity: HAC handles both, while HC0 handles only the latter.")]
story += [bullet("Treat local-to-unity as a triangular-array experiment, not a fixed stationary DGP convergence exercise.")]
story += [bullet("Compare local power only after controlling test size.")]
story += [p("Validation checklist", "H2Guide")]
story += [table(
    ["Check", "Evidence of success"],
    [
        ("Execution", "R exits with status 0 and prints the completion message."),
        ("Artifacts", "Six PDFs, nine CSVs, and sessionInfo.txt exist in the requested output directory."),
        ("Dimensions", "CSV row counts match the DGP, method, sample-size, and parameter grids."),
        ("Theory", "iid and AR/MA lambda=1 approach 5 percent; positive-persistence AR pairs approach their lambda-based limits."),
        ("Robustness", "HAC approaches nominal size for fixed stationary DGPs; HC0 repairs the common-volatility design."),
        ("Reproducibility", "Repeated runs in the same mode and software environment reproduce identical results."),
    ],
    [38 * mm, 122 * mm],
)]
story += [p("Practical caveats", "H2Guide")]
story += [p(
    "Quick mode is suitable for syntax, dependency, and artifact checks, but N = 200 gives a worst-case Monte Carlo standard error of about 3.54 percentage points. "
    "With N = 2,000, that bound falls to about 1.12 points. Tail probabilities and small differences should therefore be interpreted only from the full run."
)]
story += [p(
    "The simulation assumes Gaussian innovations and fixed bandwidth logic. Those choices are appropriate for the handout's controlled comparison but do not exhaust all forms of weak dependence, heavy tails, bandwidth selection, or finite-sample correction.",
    "Callout",
)]
story += [p("Bottom line", "H2Guide")]
story += [p(
    "The script is a reproducible demonstration that spurious significance is not exclusively a unit-root phenomenon. Independent stationary regressors and outcomes can yield misleading conventional t-tests whenever the long-run variance of the score differs from its one-period variance. "
    "By pairing analytic lambda benchmarks with conventional, HC0, and HAC simulations, the code separates the roles of persistence, heteroskedasticity, near-unit-root behavior, dynamic specification, and test size."
)]


OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc = GuideDocTemplate(
    str(OUTPUT), pagesize=A4,
    leftMargin=18 * mm, rightMargin=18 * mm,
    topMargin=20 * mm, bottomMargin=21 * mm,
    title="Spurious Stationary Simulation Explained",
    author="Codex",
    subject="Technical guide to scripts/spurious_stationary_sim.R",
)
doc.build(story)
print(OUTPUT)
