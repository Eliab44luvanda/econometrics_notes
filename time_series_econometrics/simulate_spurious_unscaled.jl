using Random, Distributions, CSV, DataFrames, Statistics

# Configuration
outfile = "spurious_rw_unscaled_sim.csv"
Ns = [50, 500, 10_000, 500_000]
R = 10_000

# Pre-allocate results
results_list = Vector{DataFrame}(undef, length(Ns))
# ...existing code...

Random.seed!(2026)

for (i, N) in pairs(Ns)
    beta_vec = Vector{Float64}(undef, R)
    
    Threads.@threads for r in 1:R
        rng = MersenneTwister(1_000_000 * i + r)
        
        x = 0.0
        y = 0.0
        sum_x = 0.0
        sum_y = 0.0
        sum_x2 = 0.0
        sum_xy = 0.0
        
        for _ in 1:N
            x += randn(rng)
            y += randn(rng)
            
            sum_x += x
            sum_y += y
            sum_x2 += x * x
            sum_xy += x * y
        end
        
        xbar = sum_x / N
        sxx = sum_x2 - N * xbar^2
        sxy = sum_xy - N * xbar * (sum_y / N)
        
        beta_hat = sxy / sxx
        beta_vec[r] = beta_hat
    end
    
    results_list[i] = DataFrame(
        N = fill(N, R),
        rep = collect(1:R),
        beta = beta_vec
    )
    
    @info "Completed N = $N"
end

results = vcat(results_list...)
CSV.write(outfile, results)
@info "Results saved to $outfile"