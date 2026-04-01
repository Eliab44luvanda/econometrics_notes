# Properties of Time Series — Render Notes

## Render Commands

**Fresh simulation** (re-runs Julia Monte Carlo, writes new CSV):

``` bash
JULIA_NUM_THREADS=auto RUN_SPURIOUS_SIM=1 quarto render properties_of_time_series_new.qmd --to pdf
```

**Repeat render** (reuses existing `spurious_rw_sim_results.csv`):

``` bash
JULIA_NUM_THREADS=auto quarto render properties_of_time_series_new.qmd --to pdf
```

------------------------------------------------------------------------

## Optimization Stack

| Layer | Technique | Benefit |
|---------------|--------------------------|-------------------------------|
| Julia | `Threads.@threads` | Parallel replications across M4 cores |
| Julia | Scalar closed-form OLS | No matrix allocations per replication |
| Julia | One-pass streaming sums | No `x`/`y` vector storage for large N |
| Julia | Skip `tstat`/`pval` for N \> 10,000 | Less compute for large samples |
| Quarto | `cache: true` / `freeze: auto` | Unchanged chunks not re-executed |
| Workflow | CSV simulate-once pattern | Near-instant repeat renders |

------------------------------------------------------------------------

## Hardware

- MacBook Pro, M4 Max, 38 GB RAM
- Julia 1.12.5 (aarch64)
- Quarto (LuaLaTeX / PDF engine)
- R 4.5 (arm64) with JuliaCall

------------------------------------------------------------------------

## Notes

- `params:` YAML block does **not** work for Julia chunks (JuliaCall limitation). Use the `RUN_SPURIOUS_SIM` environment variable instead.
- `tstat` and `pval` columns are `missing` for N \> 10,000 in the CSV — this is intentional to reduce compute time.
- The density plot shows `N * beta_hat` for N = 50, 500, 10,000, 500,000 in a 2x2 grid to illustrate spurious regression behavior.