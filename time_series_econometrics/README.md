# time_series_econometrics

This repository contains Quarto handouts for time-series econometrics.

## Recommended R packages
To render the notebooks non-interactively you should pre-install the following R packages:

- showtext
- sysfonts
- ggplot2
- ggpubr
- scales

Install them from an R session or non-interactive script with:

```sh
/usr/local/bin/Rscript -e "options(repos='https://cloud.r-project.org'); pkgs <- c('showtext','sysfonts','ggplot2','ggpubr','scales'); install.packages(setdiff(pkgs, rownames(installed.packages())), dependencies=TRUE)"
```

Optional: to use the Google font `Noto Sans` for charts, install it interactively in R once:

```r
library(sysfonts)
font_add_google('Noto Sans', 'notosans')
```

Then re-run your Quarto render. This avoids interactive package/font downloads during automated rendering.

## Preheat LaTeX font DB (optional but recommended)

On first LaTeX runs LuaTeX may spend several minutes generating a font database (luaotfload). To avoid that delay and reduce intermittent hangs during interactive renders, this repo includes a small helper that pre-generates the font DB in an isolated HOME before rendering.

- Preheat manually:

```sh
./scripts/preheat_fontdb.sh
```

- The atomic renderer will call the preheat helper automatically when present. Use the atomic render wrapper to produce validated PDFs safely:

```sh
./scripts/atomic_render.sh properties_of_time_series_new.qmd
# or via Makefile
make pdf
```

Notes:
- The preheat script requires LuaTeX (`luaotfload-tool`) available from your TeX distribution (macOS: TeX Live via `/Library/TeX/texbin`).
- The preheat step is non-fatal: if it fails the renderer continues and still attempts to produce a PDF.

## Julia

This repository also contains a small Julia Monte Carlo utility that simulates the OLS estimator
for two data-generating processes (stationary AR(1) and a random walk).

Required (non-stdlib) Julia packages:

- Distributions
- StatsPlots
- LaTeXStrings

Install the packages non-interactively from a shell:

```sh
julia -e 'import Pkg; Pkg.add(["Distributions","StatsPlots","LaTeXStrings"])'
```

Run the simulation (script available at the repository root and under `scripts/`):

```sh
# example
julia simulate_ols_ar1_random_walk.jl --phi=0.7 --n=200 --reps=10000 --burnin=200 --seed=12345 --plot=ols_estimator_distributions.png

# or the copy in the scripts/ folder
julia scripts/simulate_ols_ar1_random_walk.jl --help
```

Outputs:

- A combined histogram and kernel-density image (default: `ols_estimator_distributions.png`).
- Optional CSV with replication-level results using `--csv=path`.

See the script header for full option details; the script supports `--phi`, `--n`, `--reps`,
`--burnin`, `--seed`, `--csv`, `--plot`, and `--bins`.

Recommended Julia: 1.6+ (or the current stable release).

