---
abstract: |
  This handout reviews properties of stationary and integrated time
  series, covering definitions, examples, and visual illustrations. It
  provides a concise reference for students and researchers in
  time-series econometrics.
author:
- "**Eliab Luvanda**"
authors:
- "**Eliab Luvanda**"
bibliography: references.bib
date: 2026-03-27
engines:
- path: /Applications/quarto/share/extension-subtrees/julia-engine/\_extensions/julia-engine/julia-engine.js
execute:
  echo: false
  message: false
  warning: false
geometry:
- inner=1.3in
- outer=1.0in
- top=1.1in
- bottom=1.1in
- headsep=0.3in
header-includes:
- |
  \usepackage{amsmath, amssymb, amsthm, mathtools}
- |
  \usepackage{bm}
- |
  \usepackage{bbm}
- |
  \usepackage{booktabs}
- |
  \usepackage{longtable}
- |
  \usepackage{graphicx}
- |
  \usepackage{setspace}
- |
  \onehalfspacing
- |
  \theoremstyle{plain}
  \newtheorem{theorem}{Theorem}[section]
  \newtheorem{lemma}[theorem]{Lemma}
  \newtheorem{proposition}[theorem]{Proposition}
  \newtheorem{corollary}[theorem]{Corollary}
- |
  \theoremstyle{definition}
  \newtheorem{definition}[theorem]{Definition}
  \newtheorem{example}[theorem]{Example}
  \newtheorem{exercise}[theorem]{Exercise}
- |
  \theoremstyle{remark}
  \newtheorem{remark}[theorem]{Remark}
- |
  \renewcommand{\qedsymbol}{$\blacksquare$}
- |
  \newcommand{\E}{\mathbb{E}}
  \newcommand{\Var}{\mathrm{Var}}
  \newcommand{\Cov}{\mathrm{Cov}}
  \newcommand{\plim}{\mathrm{plim}}
  \newcommand{\R}{\mathbb{R}}
  \newcommand{\1}{\mathbbm{1}}
- |
- |
  \usepackage{titlesec}
- |
  \titleformat{\section}
    {\normalfont\large\bfseries}{\thesection}{1em}{}
- |
  \titleformat{\subsection}
    {\normalfont\normalsize\bfseries}{\thesubsection}{1em}{}
- |
  \usepackage{fancyhdr}
- |
  \pagestyle{fancy}
  \fancyhf{}
  \fancyhead[LE,RO]{\thepage}
  \fancyhead[LO]{Stationary and Integrated Processes}
  \fancyhead[RE]{Stationary and Integrated Processes}
- |
  \usepackage{hyperref}
- |
  \hypersetup{
    colorlinks=true,
    linkcolor=blue,
    citecolor=blue,
    urlcolor=blue
  }
keywords:
- time series
- stationarity
- econometrics
lang: en
subtitle: "**Properties of Stationary and Integrated Time Series**"
title: "**Time Series Econometrics**"
toc-title: Table of contents
---

\usepackage{amsmath, amssymb, amsthm, mathtools}

\usepackage{bm}

\usepackage{bbm}

\usepackage{booktabs}

\usepackage{longtable}

\usepackage{graphicx}

\usepackage{setspace}

\onehalfspacing

\theoremstyle{plain}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}


\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{example}[theorem]{Example}
\newtheorem{exercise}[theorem]{Exercise}


\theoremstyle{remark}
\newtheorem{remark}[theorem]{Remark}


\renewcommand{\qedsymbol}{$\blacksquare$}

\newcommand{\E}{\mathbb{E}}
\newcommand{\Var}{\mathrm{Var}}
\newcommand{\Cov}{\mathrm{Cov}}
\newcommand{\plim}{\mathrm{plim}}
\newcommand{\R}{\mathbb{R}}
\newcommand{\1}{\mathbbm{1}}




\usepackage{titlesec}

\titleformat{\section}
  {\normalfont\large\bfseries}{\thesection}{1em}{}


\titleformat{\subsection}
  {\normalfont\normalsize\bfseries}{\thesubsection}{1em}{}


\usepackage{fancyhdr}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE,RO]{\thepage}
\fancyhead[LO]{Stationary and Integrated Processes}
\fancyhead[RE]{Stationary and Integrated Processes}


\usepackage{hyperref}

\hypersetup{
  colorlinks=true,
  linkcolor=blue,
  citecolor=blue,
  urlcolor=blue
}


## Introduction

Time-series econometrics analyzes sequences of observations indexed by
time and explicitly models temporal dependence. Time-series data
commonly exhibit autocorrelation, non-stationarity, and seasonality. As
a result, the standard i.i.d. assumptions often fail and require
specialized methods. This handout summarizes core definitions and
properties of stationary and integrated processes, and gives concise
examples and illustrations.

Distinguishing stationary from integrated series is essential for
choosing models and making valid inferences. Central to these ideas is
the notion of a stochastic process, defined below.

\begin{definition}
Let $(\Omega,\mathcal{F},\mathbb{P})$ be a probability space, and let $T$ be an index set (often representing time, e.g. $T = \mathbb{N}$ for discrete time or $T = \mathbb{R}_{+}$ for continuous time).

A stochastic process is a family of random variables
$$\{X(\tau, \omega) : \tau \in T, \; \omega \in \Omega\}$$

such that for each fixed $\tau \in T$, the mapping
$$X(\tau, \cdot) : \Omega \to \mathbb{R}$$

is a random variable on $(\Omega, \mathcal{F}, \mathbb{P})$.
\end{definition}

Alternatively, we define a stochastic process as follows:

\begin{definition}
One can equivalently view a stochastic process as a function
$$X: \Omega \times T \to \mathbb{R},\qquad (\omega,\tau) \mapsto X(\omega,\tau),$$
where:

- For each $\tau \in T$, the mapping $X(\cdot,\tau):\Omega\to\mathbb{R}$ is measurable with respect to $\mathcal{F}$.

- For each $\omega\in\Omega$, the mapping $X(\omega,\cdot):T\to\mathbb{R}$ is a trajectory (sample path) of the process.
\end{definition}

**Key Perspectives**

• Random variable view: For each $\tau \in T$, $X(\tau)$ is a random
variable.

• Sample path view: For each $\omega \in \Omega$, $X(\omega, \cdot)$ is
a deterministic function of time.

• Distributional view: The finite-dimensional distributions
$X(\tau_1), \ldots, X(\tau_n)$ for $\tau_1, \ldots, \tau_n \in T$
characterize the process.

Figure 1 illustrates the concept of a stochastic process through the
simulation of multiple sample paths of a simple random walk, a canonical
example within stochastic process theory. Each trajectory corresponds to
a distinct realization of the process, associated with a particular
outcome $\omega \in \Omega$. The figure depicts the temporal evolution
of the process values across these realizations, thereby exemplifying
the intrinsic randomness and variability that are fundamental
characteristics of stochastic processes.

:::: cell
::: cell-output-display
![Multiple simple random-walk sample paths
(5)](properties_of_time_series_new_files/figure-markdown/unnamed-chunk-1-1.png)
:::
::::

A stochastic process formalizes "random evolution over time": given a
probability space $(\Omega,\mathcal{F},\mathbb{P})$, the process assigns
a random variable to each time point and, for a fixed outcome $\omega$,
a deterministic sample path. Figure 1 illustrates multiple sample paths
(realizations) of a simple random walk. Each trajectory corresponds to a
distinct realization. The figure depicts the temporal evolution of the
process values across these realizations. It exemplifies the intrinsic
randomness and variability that are fundamental characteristics of
stochastic processes.

## Weak Stationarity

\begin{definition}[Weak (second-order) stationarity]
Let $\{X_t : t \in T\}$ be a stochastic process with finite second moments. The process is said to be weakly stationary (or second-order stationary) if:

1. $\mathbb{E}[X_t] = \mu$ for all $t \in T$ (the mean is constant), and
2. $\mathrm{Cov}(X_{t+h}, X_t) = \gamma(h)$ depends only on the lag $h$ (the autocovariance is a function of lag only), for all $t,h$ for which the moments exist.
\end{definition}

Equivalently, weak stationarity implies that
$\mathrm{Var}(X_t)=\gamma(0)$ is constant over time. Many linear
time-series models with finite variance (for example, ARMA models with
appropriate coefficients) are weakly stationary. Weak stationarity is
the common assumption used in spectral analysis, autocorrelation
estimation, and linear forecasting methods.

Weak (or covariance) stationarity refers to a property of a time series
whereby, notwithstanding its apparent randomness, its fundamental
second-order characteristics remain invariant over time. Specifically,
the mean of the series is constant, and the covariance between any two
observations depends solely on the temporal distance (lag) separating
them rather than on their specific positions in time. Intuitively, if
one were to apply a fixed-length moving window across the series and
compute summary statistics such as the mean, variance, and
autocovariances at various lags (e.g., 1, 2, or 3), these measures would
remain stable and exhibit no systematic drift as the window progresses
along the time axis. The series does not exhibit systematic increases in
level, heightened volatility, or alterations in its correlation
structure over calendar time; rather, it persistently replicates an
identical variance--covariance configuration. This condition constitutes
a less stringent requirement than full (strong) stationarity, as it
disregards the complete distributional form and instead concentrates
exclusively on the first and second moments. Such a focus is frequently
sufficient for linear modeling frameworks and for a wide range of
practical time-series methodologies.

The figure below illustrates a simulated weakly stationary AR(1)
process, which is a common example of a stationary time series. The plot
demonstrates the constancy of the mean (indicated by the red dashed
line) and the stable variance over time, visually confirming the
properties of weak stationarity.

- Constancy of mean
- Stable variance

:::: cell
::: cell-output-display
![Simulated stationary AR(1) process (mean
dashed)](properties_of_time_series_new_files/figure-markdown/unnamed-chunk-3-1.png)
:::
::::

Figure 3 shows a simulated AR(1) series with coefficient $\phi = 0.8$
and unconditional mean approximately $\mu=5$. The dashed red horizontal
line marks the sample mean, and the dotted green lines mark the bands at
approximately $\pm2$ sample standard deviations. Deviations from the
mean are persistent but mean‑reverting (due to $\phi<1$), and the
overall variance remains roughly constant over time --- together these
features visually illustrate weak (second‑order) stationarity: a
constant mean and a covariance structure that does not drift over time.

\begin{remark}
Weak stationarity requires only constant mean and autocovariance, whereas strong stationarity requires full distributional invariance under time shifts. Although strict stationarity is a stronger condition, weak stationarity is often sufficient in practice, especially for linear models and analyses focused on second-order properties.
\end{remark}

## Strong Stationarity

A strongly (strictly) stationary process has the same finite-dimensional
distributions under any time shift. This is a stronger requirement than
weak stationarity, which only constrains the first two moments; strict
stationarity demands full distributional invariance.

\begin{definition}[strong stationarity]
Let $ (\Omega, \mathcal{F}, \mathbb{P}) $ be a probability space, and let $ \{X_t : t \in T\} $ be a stochastic process indexed by $ T \subseteq \mathbb{R} $. The process $ \{X_t\} $ is said to be strongly stationary (or strictly stationary) if, for every integer $ n \geq 1 $, for every choice of time points $ t_1, t_2, \ldots, t_n \in T $, and for every shift $ h \in \mathbb{R} $ such that $ t_i + h \in T $, we have
$ (X_{t_1}, X_{t_2}, \ldots, X_{t_n}) \overset{d}{=} (X_{t_1+h}, X_{t_2+h}, \ldots, X_{t_n+h}), $
where $ \overset{d}{=} $ denotes equality in distribution.
\end{definition}

Strong (or strict) stationarity denotes the property whereby the
complete probabilistic structure of a stochastic process remains
invariant under temporal translation. That is, not only the mean or
variance, but the entire joint distribution of any finite collection of
time-indexed random variables remains unchanged under any shift of the
time index. Intuitively, if one were to extract numerous short segments
of the series---such as triplets or longer contiguous subsequences---and
randomly permute their temporal order, it would be impossible to
determine whether a given segment originated earlier or later in time.
This is because all configurations of values, along with their
associated probability distributions, remain invariant under temporal
translation. This constitutes a highly stringent requirement: it
precludes not only the presence of trends and temporal variation in
variability, but also any modification in the distributional form or
dependence structure of the data. Consequently, the data-generating
process is, in a fundamental sense, temporally invariant.

**Key Points**

• Entire distribution invariance: Not just the mean, variance, or
covariance, but the full joint distribution of any finite collection of
random variables remains the same under time shifts.

• Stronger than weak stationarity: Weak stationarity only requires
invariance of first and second moments, while strong stationarity
requires invariance of all finite-dimensional distributions.

• Implication: Every strong stationary process is weakly stationary (if
moments exist), but not every weakly stationary process is strongly
stationary.

Intuitively, strict stationarity means that time shifts do not change
the joint distribution of observations.

\begin{example}
An everyday example is i.i.d. white noise: independence plus identical marginals imply that every finite-dimensional joint distribution is invariant under time shifts, so the process is strictly stationary.
\end{example}

:::: cell
::: cell-output-display
![Gaussian white noise (i.i.d.
N(0,1))](properties_of_time_series_new_files/figure-markdown/white_noise-1.png)
:::
::::

\begin{example}
The Bernoulli process (i.i.d. Bernoulli($p$)) is likewise strictly stationary.
\end{example}

These examples illustrate that identical marginal distributions and
independence across time imply strict stationarity.

A classic example of a process that is weakly stationary but not
strongly stationary is a non-Gaussian process with time-invariant mean
and covariance (often sharing the same covariance structure as a
Gaussian stationary process), since in the non-Gaussian case weak
stationarity need not imply strong stationarity. To make it concrete,
consider the following:

\begin{example}
Define $X_t=Z_tY$ with $Z_t$ i.i.d. mean-zero noise and $Y\in\{\pm1\}$ independent of the $Z_t$. The process has constant mean and lag-dependent covariance (weak stationarity), and finite-dimensional distributions are invariant under time shifts, so it is strictly stationary, as well.
\end{example}

In short: weak stationarity only cares about mean, variance, and
covariance stability, while strong stationarity requires full
distributional invariance. This example illustrates how a process can
meet the weaker conditions without satisfying the stronger ones.

Table 1 presents a compact summary of the series and models analyzed:
each row corresponds to a data series or simulated DGP and columns
report the sample size, the sample mean and variance, the estimated
AR(1) coefficient (with its standard error), the first few
autocovariances/autocorrelations, and the key test statistics with
p‑values used to assess weak stationarity and unit roots. Together these
entries show the degree of persistence and variability for each series,
allow quick comparison of estimated dynamics across models (e.g.,
stationary vs. near‑unit‑root behavior), and indicate which series
reject or fail to reject stationarity at conventional significance
levels.

  --------------------------------------------------------------------------------------------------------------------------------------
  Aspect                       Weak (second‑order) stationarity Strong (strict) stationarity
  --------------------- --------------------------------------- ------------------------------------------------------------------------
  Definition               Mean constant and covariance depends All finite‑dimensional distributions are invariant under time shifts:
                         only on lag: $\mathbb{E}[X_t]=\mu$ and for every $k$, $t_1,\dots,t_k$ and shift $h$,
                          $\mathrm{Cov}(X_{t+h},X_t)=\gamma(h)$ $(X_{t_1+h},\dots,X_{t_k+h}) \stackrel{d}{=} (X_{t_1},\dots,X_{t_k})$.
                                                 for all $t,h$. 

  Required moments       Requires existence of first and second No moment requirement in the definition.
                                                       moments. 

  Condition on                   Only first two moments must be Entire joint distributions must be time‑invariant.
  distributions                                 time‑invariant. 

  Implication relation    Does not imply strong stationarity in Implies weak stationarity if first and second moments exist.
                                                       general. 

  Gaussian case                    For Gaussian processes, weak Same as left column under Gaussianity.
                               $\Leftrightarrow$ strong (mean & 
                                     covariance determine law). 

  Typical examples         ARMA processes with finite variance. IID processes; time‑homogeneous Markov processes.

  Detectability / tests    Tests focus on mean/covariance (ADF, Hard to test directly; compares finite‑dimensional distributions.
                                             KPSS, sample ACF). 

  Practical use            Sufficient for spectral analysis and Stronger theoretical guarantees; rarely required in practice.
                                            linear forecasting. 

  Vulnerabilities         Can hide nonstationary higher moments More robust but harder to verify.
                                      or non‑Gaussian features. 
  --------------------------------------------------------------------------------------------------------------------------------------

  : Summary comparison of weak (second‑order) and strong (strict)
  stationarity: definitions, requirements, implications, and practical
  considerations.
