data {
  int<lower=0> N; // items
  array[N] int<lower=0> K; // trials
  array[N] int<lower=0> y; // successes  
}
transformed data {
  vector[N] log_K = log(to_vector(K));
  vector[N] log_K_std = (log_K - mean(log_K)) / sd(log_K);
}
parameters {
  real mu; // population mean of success log-odds
  real<lower=0> sigma; // population sd of success log-odds
  real a_K;
  vector[N] alpha_std; // success log-odds (standardized)
}
model {
  a_K ~ normal(0, 0.1);
  mu ~ normal(-1, 1); // hyperprior
  sigma ~ normal(0, 1); // hyperprior
  alpha_std ~ normal(0, 1); // prior (hierarchical)
  y ~ binomial_logit(K, mu + a_K * log_K_std + sigma * alpha_std); // likelihood
}
generated quantities {
  vector[N] alpha = mu + a_K * log_K_std + sigma * alpha_std;
}
