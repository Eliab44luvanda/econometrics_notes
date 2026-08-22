# Revision Implementation Report

## Scope

This report explains how the findings in the review of `spurious_regression_stationary.qmd`
were addressed in the revised Quarto document and in `scripts/spurious_stationary_sim.R`.

## Summary of the revision

The document was restructured around the long-run variance ratio

\[
\lambda=
\frac{\operatorname{LRV}\{(x_t-\mu_x)u_t\}}
     {\operatorname{Var}(x_t)\operatorname{Var}(u_t)}.
\]

The revised argument no longer treats serial correlation as synonymous with over-rejection.
It distinguishes over-rejection when \(\lambda>1\), under-rejection when \(\lambda<1\), and
correct asymptotic size when \(\lambda=1\). The Monte Carlo design now contains examples of
all three cases and directly compares conventional and HAC inference.

The Quarto document now sources the standalone R script rather than maintaining a duplicated
simulation engine. This makes the script the single computational source for the figures,
tables, and CSV outputs.

## Resolution of theoretical findings

### 1. Random-walk scaling and limit

The incorrect display for \(T^{-1}\hat\beta\) was removed. The revised document states that
\(\hat\beta=O_p(1)\) and gives the correct nondegenerate limit in terms of demeaned Brownian
motions for a regression containing an intercept. The divergence of the conventional
\(t\)-ratio is retained as a separate conclusion.

### 2. Direction of conventional size distortion

The proposition, interpretation, theorem, introduction, and conclusion now classify the test
according to \(\lambda\). The document explicitly states that serial dependence can produce
over-rejection, under-rejection, or no net asymptotic distortion.

### 3. The former if-and-only-if statement

The claim that \(\lambda=1\) if and only if the score is serially uncorrelated was removed.
Serial uncorrelatedness is now presented as sufficient but not necessary, because nonzero
autocovariances can cancel in the long-run sum.

### 4. Demeaning in the score process

Long-run variance expressions now consistently use
\((x_t-\mu_x)u_t\). The former shorthand \(\operatorname{LRV}(x_tu_t)\), which was not valid
without a zero-mean restriction, was removed.

### 5. Exact finite-sample inference

A separate remark now distinguishes exact Student-\(t\) inference from asymptotic validity.
Exactness is limited to the explicitly stated i.i.d. Gaussian-error setting with independence
from the complete regressor matrix. The general theorem no longer infers finite-sample
exactness from serial uncorrelatedness alone.

### 6. General AR(1) result

The equal-coefficient proposition was generalized to separate coefficients \(\phi_x\) and
\(\phi_y\). The document derives

\[
\lambda=\frac{1+\phi_x\phi_y}{1-\phi_x\phi_y}.
\]

This formulation demonstrates directly why equal positive coefficients over-reject and
opposite-sign coefficients under-reject.

### 7. HAC assumptions

HAC consistency is now a separate assumption rather than an unsupported consequence of the
score central limit theorem. The document specifies kernel and bandwidth requirements and
states that additional moment and dependence conditions are needed for consistent long-run
variance estimation.

### 8. Scope of the nonstationary comparison

Claims that divergent spurious regression occurs only with unit roots were removed. The
discussion is now explicitly limited to the comparison between fixed-parameter,
short-memory stationary processes and the independent random-walk benchmark studied in the
document.

## Changes to the Monte Carlo design and R script

### Expanded DGP coverage

The script now simulates eight DGPs:

- i.i.d. Gaussian series;
- equal positive AR pairs \((0.5,0.5)\), \((0.8,0.8)\), \((0.9,0.9)\), and
  \((0.95,0.95)\);
- an unequal positive pair \((0.9,0.5)\);
- an opposite-sign pair \((0.8,-0.8)\); and
- independent random walks.

The opposite-sign case supplies the counterexample missing from the original design. Its
conventional test under-rejects, even though both series are serially correlated.

### Stationary initialization

Every AR(1) pre-sample state continues to be drawn from its invariant distribution. The logic
was factored into `draw_ar1()`, so unequal and negative coefficients receive the correct
coefficient-specific stationary variance.

### HAC implementation

The script now computes Bartlett-HAC standard errors at six selected sample sizes using the
score \((x_t-\bar x)\hat u_t\). The bandwidth is
\(L_T=\lfloor2T^{1/3}\rfloor\), which satisfies \(L_T\to\infty\) and
\(L_T/T\to0\). A deliberately explicit implementation makes the estimator auditable without
adding a package dependency.

The revised results show that HAC inference moves all stationary DGPs toward nominal size.
The most persistent case still rejects 10.7% of the time at \(T=5000\), and the document now
identifies this as a finite-sample long-run variance estimation issue rather than claiming an
instantaneous HAC cure.

### Reproducibility and output files

The script writes:

- `spurious_rejection_frequency_series.csv`;
- `spurious_hac_rejection_frequency_series.csv`;
- `spurious_comparison_table.csv`;
- `spurious_hac_comparison_table.csv`;
- conventional rejection-frequency plots in PNG and PDF; and
- conventional-versus-HAC plots in PNG and PDF.

The simulation uses a fixed seed and 2,000 replications. The document reports the resulting
maximum Monte Carlo standard error of 1.12 percentage points.

## Resolution of results and presentation findings

- The statement that persistent series reject a majority of the time at every sample size was
  removed.
- Rejection frequencies are described as converging to plateaus, not as invariant to sample
  size.
- The i.i.d. Monte Carlo frequency is described as fluctuating around the exact theoretical
  benchmark rather than equalling 5% mechanically.
- The description of nested samples now says that nesting correlates estimates and smooths
  comparisons; it no longer claims to eliminate between-sample-size noise.
- “Continuously” was replaced by an explicit grid from 50 to 5000 in increments of 50.
- The former duplicated Appendix code was replaced by a computational appendix pointing to the
  complete standalone script.
- Unused `dplyr` and `tidyr` dependencies were removed.
- The conclusion now contains a conditional, four-part interpretation consistent with the
  revised theorem and simulation.

## Validation performed

1. The revised R script was parsed successfully.
2. The full 2,000-replication, eight-DGP simulation completed successfully.
3. The saved CSV values were checked against the numerical statements and generated tables.
4. The Quarto document rendered successfully with LuaLaTeX.
5. All eight article pages were rendered to images and visually inspected for clipping,
   overlapping content, broken tables, unreadable figures, and page-layout problems.
6. Duplicate proof-ending symbols found during visual inspection were removed before the final
   render.

## Outcome

All substantive issues identified in the review have been addressed. The revised document is
more limited in scope but theoretically defensible: stationarity ensures slope consistency in
the stated independent short-memory setting, while validity of conventional inference depends
on the long-run variance ratio. The R script now tests the full classification and provides
direct evidence on the asymptotic HAC remedy and its finite-sample limitations.
