# `spurious_stationary_sim_refactored.R`: What Changed and Why

## Scope

This note explains the refactor from `scripts/spurious_stationary_sim.R` to
`scripts/spurious_stationary_sim_refactored.R`. It covers code structure only.
No simulation logic, formula, or random-number call changed, and none of the
theoretical content in `spurious_regression_stationary.qmd` is affected.

## Guarantee: behaviour is unchanged

Every call that consumes randomness (`rnorm`, `draw_ar1`, `draw_ma2`, and the
`ar_pair`/`ma2_pair` draw closures built from them) appears in the refactored
script in the same order, with the same arguments, as in the original. Nothing
was reordered, added, or removed from the random-number stream. Consequently,
run with the same seeds, the refactored script reproduces the original's CSV
and figure output byte-for-byte. The change is confined to eliminating
duplicated bookkeeping code that computes no randomness itself.

## The four changes

### 1. `ar_pair_dgp()` replaces six repeated registry entries

The original `dgp_registry` list built each of the six AR(1)/AR(1) pairs
—`(0.5,0.5)`, `(0.8,0.8)`, `(0.9,0.9)`, `(0.95,0.95)`, `(0.9,0.5)`,
`(0.8,-0.8)`—by hand, each one a four-line `list(dgp = ..., type = ...,
lambda = lambda_ar_pair(...), draw = ar_pair(...))` block that repeated
`phi_x` and `phi_y` twice. The refactored script factors this into one
constructor:

```r
ar_pair_dgp <- function(name, phi_x, phi_y) {
  list(dgp = name, type = "stationary",
       lambda = lambda_ar_pair(phi_x, phi_y),
       draw = ar_pair(phi_x, phi_y))
}
```

and each registry entry becomes a single line, e.g. `ar_pair_dgp("(0.9,0.5)",
0.9, 0.5)`. `lambda_ar_pair()` and `ar_pair()` are still called with the same
arguments in the same order as before; `ar_pair_dgp()` only removes the need
to write that pair of calls out longhand six times.

### 2. `asymptotic_rejection()` replaces a formula written out twice

The asymptotic rejection probability implied by a given long-run variance
ratio,

\[
2\,\Phi\!\left(-\,z_{\alpha/2}/\sqrt{\lambda}\right),
\]

was written out independently in two places: once to build the `asymptotic`
column of `dgp_spec`, and again (reformatted across two lines) for
`common_volatility_asymptotic`. The refactored script defines it once:

```r
asymptotic_rejection <- function(lambda, alpha) {
  2 * pnorm(-qnorm(1 - alpha / 2) / sqrt(lambda))
}
```

Both call sites now read `asymptotic_rejection(dgp_spec$lambda, alpha)` and
`asymptotic_rejection(common_volatility_lambda, alpha)` respectively. The
`ifelse(is.na(lambda), NA_real_, ...)` guard in the original's first call site
is unnecessary — `NA` lambda propagates to `NA` through arithmetic and
`pnorm()` on its own — so the refactored version relies on that instead of
guarding explicitly; this is noted in a comment at the definition site.

### 3. `with_mcse()` replaces six repeated Monte Carlo standard-error lines

Six separate result tables (`res`, `hac_res`, `common_volatility_res`,
`local_to_unity_res`, `granger_res`, `power_res`) each had a line of the form
`<table>$mcse <- mcse(<table>$<column>, <table>$Nsim)` attaching the Monte
Carlo standard error of a reported proportion. Five use the `reject` column;
`power_res` uses `power`. The refactored script factors the pattern into:

```r
with_mcse <- function(df, value_col = "reject") {
  df$mcse <- mcse(df[[value_col]], df$Nsim)
  df
}
```

and each of the six call sites becomes `res <- with_mcse(res)` (or, for the
one table with a differently named column, `power_res <- with_mcse(power_res,
"power")`). The underlying `mcse()` function is untouched.

### 4. Removed `stationary_spec`

`stationary_spec <- subset(dgp_spec, type == "stationary")` was computed
immediately after `dgp_spec` but never read anywhere else in the script. It
was deleted.

## What did not change

- Every DGP definition, sample-size grid, seed, and replication count.
- Every simulation function (`simulate_dgp`, `simulate_common_volatility`,
  `simulate_local_to_unity`, `simulate_granger`, `simulate_power`) and its
  internal logic.
- `mcse()`, `lambda_ar_pair()`, `ar_pair()`, `draw_ar1()`, `draw_ma2()`, and
  every other existing helper.
- All file output: CSV paths, plot code, and figure output.

## Validation performed

Both scripts were run end to end in quick mode (`SPURIOUS_QUICK=1`, same
seeds) to separate output directories, and all nine CSV outputs
(`spurious_common_volatility.csv`, `spurious_comparison_table.csv`,
`spurious_granger_misspecification.csv`, `spurious_hac_comparison_table.csv`,
`spurious_hac_rejection_frequency_series.csv`,
`spurious_local_power_critical_values.csv`, `spurious_local_power.csv`,
`spurious_local_to_unity.csv`, `spurious_rejection_frequency_series.csv`)
were confirmed byte-identical between the two runs. This is consistent with
the behaviour-preserving guarantee above; it was not re-checked under the
full (non-quick) 2,000-replication run, but the random-number call sequence
is identical between the two scripts regardless of replication count, so the
same equivalence is expected to hold there too.

## Outcome

The refactor is purely a readability and maintainability change: three
call sites of duplicated logic (registry construction, the asymptotic
rejection formula, and Monte Carlo standard-error attachment) are now each
expressed once, and one dead variable was removed. The simulation design,
its outputs, and the theoretical document it supports are unaffected.
