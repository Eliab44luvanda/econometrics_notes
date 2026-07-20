library(ggplot2)

set.seed(42)
T   <- 100
phi <- 0.6

y <- numeric(T)
y[1] <- rnorm(1, mean = 0, sd = 1 / sqrt(1 - phi^2))  # draw from stationary dist
for (t in 2:T) {
  y[t] <- phi * y[t - 1] + rnorm(1)
}

df <- data.frame(t = 1:T, y = y)

ggplot(df, aes(x = t, y = y)) +
  geom_line(color = "steelblue", linewidth = 0.8) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "grey50") +
  labs(
    title    = expression("Simulated AR(1) Process:" ~ y[t] == 0.6 * y[t-1] + epsilon[t]),
    subtitle = paste0("T = ", T, ",  phi = ", phi),
    x        = "Time",
    y        = expression(y[t])
  ) +
  theme_classic()
