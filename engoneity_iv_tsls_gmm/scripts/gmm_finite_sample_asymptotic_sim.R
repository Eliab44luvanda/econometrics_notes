# =============================================================================
# Finite-sample and asymptotic properties of the linear GMM estimator
#
# Companion script for the GMM sections of "Endogeneity and Moment-Based
# Estimation". The design is an overidentified linear instrumental-variables
# model: one endogenous regressor, two excluded instruments, and
# conditionally heteroskedastic errors, so that the one-step (2SLS-weighted)
# and two-step efficient GMM estimators genuinely differ.
#
# For a grid of sample sizes it simulates:
#   1. Consistency  -- Monte Carlo bias and variance of both estimators as
#                       n grows.
#   2. Efficiency    -- the two-step estimator's variance against the
#                       one-step estimator's, at each n.
#   3. Asymptotic normality -- the finite-sample density and QQ-plot of the
#                       studentized two-step estimator against N(0,1), at a
#                       small and a large sample size.
#   4. Correct inference -- coverage of the nominal 95% confidence interval
#                       built from the estimated GMM sandwich variance.
#   5. Correct overidentification testing -- rejection frequency of Hansen's
#                       J statistic (df = 1) under a correctly specified
#                       model, which should be close to the nominal 5%.
#
# Dependencies: R (>= 4.1), ggplot2, scales. No other packages are required.
#
# Runtime: a few seconds single-threaded (linear algebra on 2x2 and 3x3
# matrices only). Set GMM_QUICK=1 in the environment for an even faster
# (and correspondingly noisier) pass while drafting.
# =============================================================================

library(ggplot2)
library(scales)

# ---- global options ---------------------------------------------------------

quick <- nzchar(Sys.getenv("GMM_QUICK"))

n_grid    <- c(50, 100, 250, 500, 1000, 2500, 5000, 10000)
Nsim      <- if (quick) 300 else 5000
alpha     <- 0.05

beta_true <- c(intercept = 1, slope = 2)   # y = beta[1] + beta[2] * x2 + eps
pi_coef   <- c(0.5, 1, 1)                  # first stage: x2 = pi0 + pi1 z1 + pi2 z2 + v
rho       <- 0.6                           # corr(v, structural error), the source of endogeneity

n_small <- 50
n_large <- 5000

set.seed(2026)

# =============================================================================
# 1. Data-generating process
#
# x2 is endogenous: its first-stage error v is correlated (rho) with the
# structural error eps. z1 and z2 are valid, relevant excluded instruments
# (one more than needed, so the model has one overidentifying restriction).
# eps is heteroskedastic through z1, which is what makes the two-step
# efficient GMM estimator genuinely more efficient than the one-step
# (2SLS-weighted) GMM estimator.
# =============================================================================

simulate_data <- function(n, beta_true, pi_coef, rho) {
  z1 <- rnorm(n)
  z2 <- rnorm(n)
  u  <- rnorm(n)
  w  <- rnorm(n)

  v   <- u
  e   <- rho * u + sqrt(1 - rho^2) * w
  x2  <- pi_coef[1] + pi_coef[2] * z1 + pi_coef[3] * z2 + v

  eps_sd <- sqrt(0.5 + z1^2)
  eps    <- eps_sd * e
  y      <- beta_true[1] + beta_true[2] * x2 + eps

  list(y = y, X = cbind(1, x2), Z = cbind(1, z1, z2))
}

# =============================================================================
# 2. Linear GMM estimator and its sandwich variance
#
# Gn = Z'X/n, Zy_n = Z'y/n are the sample moment-condition Jacobian and the
# instrument-residual cross moment. For weighting matrix Wn the closed-form
# GMM estimator and its (possibly non-optimal) sandwich variance are the
# standard extremum-estimator formulas; when Wn is the inverse of a
# consistent estimator of the moment covariance the sandwich collapses to
# solve(Gn' Wn Gn)/n, the efficient-GMM variance used for beta2 below.
# =============================================================================

gmm_beta <- function(Gn, Zy_n, Wn) {
  M <- t(Gn) %*% Wn %*% Gn
  m <- t(Gn) %*% Wn %*% Zy_n
  solve(M, m)
}

sandwich_vcov <- function(Gn, Wn, Sn, n) {
  bread <- solve(t(Gn) %*% Wn %*% Gn)
  meat  <- t(Gn) %*% Wn %*% Sn %*% Wn %*% Gn
  (bread %*% meat %*% bread) / n
}

# One replication: one-step GMM (Wn = (Z'Z/n)^{-1}, numerically the 2SLS
# estimator) followed by the two-step efficient GMM estimator that reweights
# by the inverse of the heteroskedasticity-robust moment covariance estimated
# from the one-step residuals. Returns both estimators, their sandwich
# standard errors, and the Hansen J statistic for the efficient estimator.
simulate_one <- function(n, beta_true, pi_coef, rho) {
  d <- simulate_data(n, beta_true, pi_coef, rho)
  y <- d$y; X <- d$X; Z <- d$Z

  Gn   <- crossprod(Z, X) / n
  Zy_n <- crossprod(Z, y) / n

  # --- one-step GMM (2SLS weighting matrix) ---------------------------------
  Wn1    <- solve(crossprod(Z) / n)
  beta1  <- gmm_beta(Gn, Zy_n, Wn1)
  resid1 <- y - X %*% beta1
  Sn1    <- crossprod(Z * as.vector(resid1)) / n
  V1     <- sandwich_vcov(Gn, Wn1, Sn1, n)

  # --- two-step efficient GMM (heteroskedasticity-robust weighting) --------
  Wn2   <- solve(Sn1)
  beta2 <- gmm_beta(Gn, Zy_n, Wn2)
  V2    <- solve(t(Gn) %*% Wn2 %*% Gn) / n

  gbar  <- Zy_n - Gn %*% beta2
  Jstat <- as.numeric(n * t(gbar) %*% Wn2 %*% gbar)

  list(beta1 = as.vector(beta1), se1 = sqrt(diag(V1)),
       beta2 = as.vector(beta2), se2 = sqrt(diag(V2)),
       Jstat = Jstat)
}

# =============================================================================
# 3. Main experiment: Monte Carlo distribution at each sample size
# =============================================================================

simulate_n <- function(n, Nsim, beta_true, pi_coef, rho) {
  beta1 <- matrix(NA_real_, Nsim, 2)
  se1   <- matrix(NA_real_, Nsim, 2)
  beta2 <- matrix(NA_real_, Nsim, 2)
  se2   <- matrix(NA_real_, Nsim, 2)
  Jstat <- numeric(Nsim)

  for (r in seq_len(Nsim)) {
    out <- simulate_one(n, beta_true, pi_coef, rho)
    beta1[r, ] <- out$beta1; se1[r, ] <- out$se1
    beta2[r, ] <- out$beta2; se2[r, ] <- out$se2
    Jstat[r]   <- out$Jstat
  }

  list(n = n, beta1 = beta1, se1 = se1, beta2 = beta2, se2 = se2, Jstat = Jstat)
}

raw <- lapply(n_grid, simulate_n, Nsim = Nsim,
              beta_true = beta_true, pi_coef = pi_coef, rho = rho)
names(raw) <- as.character(n_grid)

# Slope (beta[2]) is the endogenous-regressor coefficient of interest;
# the intercept behaves the same way and is omitted from the summaries below.
slope_true <- beta_true[["slope"]]

summarise_n <- function(res) {
  b1 <- res$beta1[, 2]; s1 <- res$se1[, 2]
  b2 <- res$beta2[, 2]; s2 <- res$se2[, 2]
  z  <- qnorm(1 - alpha / 2)

  data.frame(
    n            = res$n,
    bias_1step   = mean(b1) - slope_true,
    bias_2step   = mean(b2) - slope_true,
    var_1step    = var(b1),
    var_2step    = var(b2),
    rmse_1step   = sqrt(mean((b1 - slope_true)^2)),
    rmse_2step   = sqrt(mean((b2 - slope_true)^2)),
    coverage_1step = mean(abs(b1 - slope_true) < z * s1),
    coverage_2step = mean(abs(b2 - slope_true) < z * s2),
    J_rejection    = mean(res$Jstat > qchisq(1 - alpha, df = 1))
  )
}

summary_table <- do.call(rbind, lapply(raw, summarise_n))
rownames(summary_table) <- NULL

# =============================================================================
# 4. Asymptotic normality: studentized two-step estimator at a small and a
#    large sample size, against its N(0,1) limit.
# =============================================================================

studentized <- function(res) (res$beta2[, 2] - slope_true) / res$se2[, 2]

normality_data <- rbind(
  data.frame(n = n_small, z = studentized(raw[[as.character(n_small)]])),
  data.frame(n = n_large, z = studentized(raw[[as.character(n_large)]]))
)
normality_data$panel <- factor(paste0("n = ", normality_data$n),
                               levels = paste0("n = ", c(n_small, n_large)))

qq_data <- do.call(rbind, lapply(c(n_small, n_large), function(n) {
  z <- sort(studentized(raw[[as.character(n)]]))
  p <- (seq_along(z) - 0.5) / length(z)
  data.frame(n = n, theoretical = qnorm(p), sample = z)
}))
qq_data$panel <- factor(paste0("n = ", qq_data$n),
                        levels = paste0("n = ", c(n_small, n_large)))

# =============================================================================
# 5. Accessors used by the handout
#
# Fail loudly rather than returning a wrong or empty value, so a mismatch
# between prose and simulation cannot pass silently.
# =============================================================================

.one <- function(v, what) {
  if (length(v) != 1L)
    stop(sprintf("accessor '%s' matched %d records, expected 1", what, length(v)))
  v
}

pc <- function(p, digits = 1) sprintf(paste0("%.", digits, "f%%"), 100 * p)

row_at <- function(n) .one(which(summary_table$n == n), sprintf("row_at(%d)", n))

bias_of  <- function(n, estimator = "2step", digits = 4)
  sprintf(paste0("%.", digits, "f"),
          summary_table[[paste0("bias_", estimator)]][row_at(n)])
var_of   <- function(n, estimator = "2step", digits = 5)
  sprintf(paste0("%.", digits, "f"),
          summary_table[[paste0("var_", estimator)]][row_at(n)])
cov_of   <- function(n, estimator = "2step", digits = 1)
  pc(summary_table[[paste0("coverage_", estimator)]][row_at(n)], digits)
jrej_of  <- function(n, digits = 1) pc(summary_table$J_rejection[row_at(n)], digits)
efficiency_gain_of <- function(n, digits = 1)
  pc(1 - summary_table$var_2step[row_at(n)] / summary_table$var_1step[row_at(n)], digits)

# =============================================================================
# 6. Figures
# =============================================================================

base_theme <- function(base_size = 9) {
  theme_classic(base_size = base_size) +
    theme(legend.position = "bottom",
          plot.title = element_text(hjust = 0.5))
}

estimator_labels <- c(bias_1step = "One-step GMM (2SLS weight)",
                      bias_2step = "Two-step efficient GMM")

bias_long <- data.frame(
  n         = rep(summary_table$n, 2),
  bias      = c(summary_table$bias_1step, summary_table$bias_2step),
  estimator = rep(c("One-step GMM (2SLS weight)", "Two-step efficient GMM"),
                   each = nrow(summary_table))
)

p_bias <- ggplot(bias_long, aes(n, bias, colour = estimator)) +
  geom_hline(yintercept = 0, linetype = "dashed", linewidth = 0.4) +
  geom_line(linewidth = 0.6) +
  geom_point(size = 1.5) +
  scale_x_log10(breaks = n_grid, labels = n_grid) +
  base_theme() +
  labs(x = "Sample size n (log scale)", y = "Monte Carlo bias",
       colour = NULL, title = "Consistency: bias of the GMM slope estimator")

var_long <- data.frame(
  n         = rep(summary_table$n, 2),
  variance  = c(summary_table$var_1step, summary_table$var_2step),
  estimator = rep(c("One-step GMM (2SLS weight)", "Two-step efficient GMM"),
                   each = nrow(summary_table))
)

p_var <- ggplot(var_long, aes(n, variance, colour = estimator)) +
  geom_line(linewidth = 0.6) +
  geom_point(size = 1.5) +
  scale_x_log10(breaks = n_grid, labels = n_grid) +
  scale_y_log10() +
  base_theme() +
  labs(x = "Sample size n (log-log scale)", y = "Monte Carlo variance (log scale)",
       colour = NULL,
       title = "Efficiency: two-step GMM attains lower sampling variance")

normal_density <- data.frame(z = seq(-4, 4, length.out = 400))
normal_density$density <- dnorm(normal_density$z)

p_density <- ggplot(normality_data, aes(z)) +
  geom_histogram(aes(y = after_stat(density)), bins = 40,
                 fill = "grey80", colour = "white") +
  geom_line(data = normal_density, aes(z, density),
            colour = "#EE6677", linewidth = 0.7) +
  facet_wrap(~ panel) +
  base_theme() +
  labs(x = expression((hat(beta)[2] - beta[2]) / widehat(se)(hat(beta)[2])),
       y = "Density",
       title = "Asymptotic normality of the studentized two-step GMM estimator")

p_qq <- ggplot(qq_data, aes(theoretical, sample)) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", colour = "#EE6677") +
  geom_point(size = 0.5, alpha = 0.4) +
  facet_wrap(~ panel) +
  base_theme() +
  labs(x = "Theoretical N(0,1) quantiles", y = "Studentized GMM estimator quantiles",
       title = "QQ-plot of the studentized two-step GMM estimator")

coverage_long <- data.frame(
  n         = rep(summary_table$n, 2),
  coverage  = c(summary_table$coverage_1step, summary_table$coverage_2step),
  estimator = rep(c("One-step GMM (2SLS weight)", "Two-step efficient GMM"),
                   each = nrow(summary_table))
)

p_coverage <- ggplot(coverage_long, aes(n, coverage, colour = estimator)) +
  geom_hline(yintercept = 1 - alpha, linetype = "dashed", linewidth = 0.4) +
  geom_line(linewidth = 0.6) +
  geom_point(size = 1.5) +
  scale_x_log10(breaks = n_grid, labels = n_grid) +
  scale_y_continuous(labels = percent_format(accuracy = 1)) +
  coord_cartesian(ylim = c(0.8, 1)) +
  base_theme() +
  labs(x = "Sample size n (log scale)",
       y = "Coverage of the nominal 95% confidence interval",
       colour = NULL, title = "Coverage of GMM sandwich-based confidence intervals")

p_jtest <- ggplot(summary_table, aes(n, J_rejection)) +
  geom_hline(yintercept = alpha, linetype = "dashed", linewidth = 0.4) +
  geom_line(linewidth = 0.6, colour = "#4477AA") +
  geom_point(size = 1.5, colour = "#4477AA") +
  scale_x_log10(breaks = n_grid, labels = n_grid) +
  scale_y_continuous(labels = percent_format(accuracy = 1)) +
  coord_cartesian(ylim = c(0, 0.15)) +
  base_theme() +
  labs(x = "Sample size n (log scale)",
       y = "Rejection frequency at the 5% level",
       title = "Size of Hansen's J overidentification test (df = 1)")

# =============================================================================
# 7. Outputs
# =============================================================================

output_dir <- Sys.getenv("GMM_OUTPUT_DIR", unset = "scripts")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

figures <- list(
  gmm_bias        = list(plot = p_bias,     w = 5.6, h = 3.8),
  gmm_variance    = list(plot = p_var,      w = 5.6, h = 3.8),
  gmm_density     = list(plot = p_density,  w = 6.0, h = 3.4),
  gmm_qq          = list(plot = p_qq,       w = 6.0, h = 3.4),
  gmm_coverage    = list(plot = p_coverage, w = 5.6, h = 3.8),
  gmm_jtest_size  = list(plot = p_jtest,    w = 5.6, h = 3.8)
)
for (nm in names(figures)) {
  f <- figures[[nm]]
  ggsave(file.path(output_dir, paste0(nm, ".pdf")), f$plot, width = f$w, height = f$h)
}

tables <- list(
  gmm_summary_table    = summary_table,
  gmm_normality_sample = normality_data
)
for (nm in names(tables)) {
  write.csv(tables[[nm]], file.path(output_dir, paste0(nm, ".csv")), row.names = FALSE)
}

writeLines(capture.output(sessionInfo()), file.path(output_dir, "sessionInfo.txt"))

message("Simulation complete. Figures and CSV files written to ", output_dir)
