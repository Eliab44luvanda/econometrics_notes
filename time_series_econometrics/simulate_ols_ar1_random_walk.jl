
#!/usr/bin/env julia

using DelimitedFiles
using Distributions
using Printf
using StatsPlots
using LaTeXStrings
using Random
using Statistics

"""
Parse command-line arguments of the form `--key=value`.
"""
function parse_args(args)
    options = Dict(
        "phi" => "0.7",
        "n" => "2000",
        "reps" => "200000",
        "burnin" => "200",
        "seed" => "12345",
        "csv" => "",
        "plot" => "ols_estimator_distributions.png",
        "bins" => "30",
    )

    for arg in args
        if arg in ("-h", "--help")
            println("""
            Usage: julia scripts/simulate_ols_ar1_random_walk.jl [options]

            Simulates the OLS estimator from the regression
                y_t = alpha + phi * y_{t-1} + u_t
            under:
            1. A stationary AR(1) process with |phi| < 1
            2. A random walk process with unit root

            Options:
              --phi=<number>     AR(1) coefficient for the stationary process
              --n=<integer>      Sample size used in each replication
              --reps=<integer>   Number of Monte Carlo replications
              --burnin=<integer> Burn-in draws for the stationary AR(1)
              --seed=<integer>   Random seed
              --csv=<path>       Optional output CSV for replication-level results
              --plot=<path>      Output image path for histograms and density overlays
              --bins=<integer>   Number of histogram bins
            """)
            exit(0)
        end

        if startswith(arg, "--") && occursin("=", arg)
            key, value = split(arg[3:end], "="; limit = 2)
            if haskey(options, key)
                options[key] = value
            else
                error("Unknown option: --$key")
            end
        else
            error("Invalid argument: $arg")
        end
    end

    return (
        phi = parse(Float64, options["phi"]),
        n = parse(Int, options["n"]),
        reps = parse(Int, options["reps"]),
        burnin = parse(Int, options["burnin"]),
        seed = parse(Int, options["seed"]),
        csv = options["csv"],
        plot = options["plot"],
        bins = parse(Int, options["bins"]),
    )
end

"""
Generate a stationary AR(1) series with burn-in:
    y_t = phi * y_{t-1} + eps_t
"""
function simulate_ar1(phi, n, burnin)
    total = n + burnin
    y = zeros(total)
    innovations = randn(total)

    for t in 2:total
        y[t] = phi * y[t - 1] + innovations[t]
    end

    return y[(burnin + 1):end]
end

"""
Generate a random walk:
    y_t = y_{t-1} + eps_t
"""
function simulate_random_walk(n)
    y = zeros(n)
    innovations = randn(n)

    for t in 2:n
        y[t] = y[t - 1] + innovations[t]
    end

    return y
end

"""
OLS for y_t on an intercept and y_{t-1}.
Returns (alpha_hat, phi_hat).
"""
function ols_ar1_estimate(y)
    ydep = @view y[2:end]
    xlag = @view y[1:(end - 1)]

    xbar = mean(xlag)
    ybar = mean(ydep)

    centered_x = xlag .- xbar
    centered_y = ydep .- ybar

    phi_hat = sum(centered_x .* centered_y) / sum(centered_x .^ 2)
    alpha_hat = ybar - phi_hat * xbar

    return alpha_hat, phi_hat
end

function summarize_estimates(name, alpha_hats, phi_hats, true_phi)
    phi_mean = mean(phi_hats)
    phi_std = std(phi_hats)
    phi_bias = phi_mean - true_phi

    alpha_mean = mean(alpha_hats)
    alpha_std = std(alpha_hats)

    println()
    println(name)
    println(repeat("-", length(name)))
    @printf("True phi           : %8.4f\n", true_phi)
    @printf("Mean(phi_hat)      : %8.4f\n", phi_mean)
    @printf("Std(phi_hat)       : %8.4f\n", phi_std)
    @printf("Bias(phi_hat)      : %8.4f\n", phi_bias)
    @printf("Mean(alpha_hat)    : %8.4f\n", alpha_mean)
    @printf("Std(alpha_hat)     : %8.4f\n", alpha_std)
end

function maybe_write_csv(path, ar1_alpha, ar1_phi, rw_alpha, rw_phi)
    if isempty(path)
        return
    end

    rows = Matrix{Any}(undef, length(ar1_phi) + length(rw_phi) + 1, 4)
    rows[1, :] = ["process", "replication", "alpha_hat", "phi_hat"]

    row = 2
    for i in eachindex(ar1_phi)
        rows[row, :] = ["stationary_ar1", i, ar1_alpha[i], ar1_phi[i]]
        row += 1
    end

    for i in eachindex(rw_phi)
        rows[row, :] = ["random_walk", i, rw_alpha[i], rw_phi[i]]
        row += 1
    end

    writedlm(path, rows, ',')
    println()
    println("Saved replication-level results to: $path")
end

function add_histogram_density_plot!(plt, estimates, title_text, true_value, bins)
    histogram!(
        plt,
        estimates;
        normalize = :pdf,
        bins = bins,
        alpha = 0.35,
        color = :steelblue,
        linecolor = :white,
        linewidth = 0.5,
        label = "Histogram",
        title = title_text,
        xlabel = L"\hat{\phi}",
        ylabel = "Density",
    )

    density!(
        plt,
        estimates;
        color = :firebrick,
        linewidth = 2,
        label = "Kernel density",
    )

    fitted_normal = Normal(mean(estimates), std(estimates))
    xgrid = range(minimum(estimates), maximum(estimates); length = 400)
    plot!(
        plt,
        xgrid,
        pdf.(fitted_normal, xgrid);
        color = :black,
        linestyle = :dash,
        linewidth = 2,
        label = "Normal fit",
    )

    vline!(
        plt,
        [true_value];
        color = :darkgreen,
        linestyle = :dot,
        linewidth = 2,
        label = "True value",
    )
end

function save_plots(path, ar1_phi, rw_phi, phi, bins)
    default(fontfamily = "sans-serif")

    p1 = plot()
        add_histogram_density_plot!(p1, ar1_phi, L"Stationary AR(1): \hat{\phi}", phi, bins)

    p2 = plot()
        add_histogram_density_plot!(p2, rw_phi, L"Random Walk: \hat{\phi}", 1.0, bins)

    combined = plot(
        p1, p2;
        layout = (1, 2),
        size = (1200, 450),
            plot_title = "",
        margin = 6Plots.mm,
    )

    # Display in interactive sessions (REPL/Julia client)
    try
        display(combined)
    catch _
        # ignore if display is not available
    end

    savefig(combined, path)
    println()
    println("Saved histogram and density plots to: $path")

    # Try to open the image using the OS default viewer for convenience
    try
        if Sys.isapple()
            run(`open $path`)
        elseif Sys.iswindows()
            run(`cmd /c start "" $path`)
        else
            run(`xdg-open $path`)
        end
    catch e
        @warn "Could not open image automatically: $e"
    end
end

function main()
    opts = parse_args(ARGS)

    if abs(opts.phi) >= 1
        error("For the stationary AR(1), --phi must satisfy |phi| < 1.")
    end
    if opts.n < 2
        error("--n must be at least 2.")
    end
    if opts.reps < 1
        error("--reps must be positive.")
    end
    if opts.bins < 1
        error("--bins must be positive.")
    end

    Random.seed!(opts.seed)

    ar1_alpha = Vector{Float64}(undef, opts.reps)
    ar1_phi = Vector{Float64}(undef, opts.reps)
    rw_alpha = Vector{Float64}(undef, opts.reps)
    rw_phi = Vector{Float64}(undef, opts.reps)

    for r in 1:opts.reps
        y_ar1 = simulate_ar1(opts.phi, opts.n, opts.burnin)
        ar1_alpha[r], ar1_phi[r] = ols_ar1_estimate(y_ar1)

        y_rw = simulate_random_walk(opts.n)
        rw_alpha[r], rw_phi[r] = ols_ar1_estimate(y_rw)
    end

    println("Monte Carlo simulation of the OLS estimator")
    println("===========================================")
    @printf("Sample size (n)    : %d\n", opts.n)
    @printf("Replications       : %d\n", opts.reps)
    @printf("Burn-in            : %d\n", opts.burnin)
    @printf("Seed               : %d\n", opts.seed)

    summarize_estimates("Stationary AR(1)", ar1_alpha, ar1_phi, opts.phi)
    summarize_estimates("Random Walk", rw_alpha, rw_phi, 1.0)

    maybe_write_csv(opts.csv, ar1_alpha, ar1_phi, rw_alpha, rw_phi)
    save_plots(opts.plot, ar1_phi, rw_phi, opts.phi, opts.bins)
end

main()
