#!/bin/bash
#SBATCH --job-name=r-stats
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=01:00:00
#SBATCH --output=r-stats-%j.log

# Run a simple statistical calculation in R:
# - simulate 1M random samples
# - compute summary statistics and a linear regression
# - write results to results.csv

Rscript - <<'REOF'
set.seed(42)
n <- 1000000

x <- rnorm(n, mean = 50, sd = 10)
y <- 2.5 * x + rnorm(n, mean = 0, sd = 5)

cat("=== Summary of x ===\n")
print(summary(x))

cat("\n=== Summary of y ===\n")
print(summary(y))

model <- lm(y ~ x)
cat("\n=== Linear regression y ~ x ===\n")
print(summary(model))

results <- data.frame(
  metric = c("mean_x", "sd_x", "mean_y", "sd_y", "r_squared"),
  value  = c(mean(x), sd(x), mean(y), sd(y), summary(model)$r.squared)
)
write.csv(results, "results.csv", row.names = FALSE)
cat("\nResults written to results.csv\n")
REOF
