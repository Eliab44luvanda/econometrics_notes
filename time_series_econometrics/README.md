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
