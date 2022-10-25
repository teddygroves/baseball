functions {
#include gpareto.stan
}
data {
  int<lower=0> N; // items
  array[N] int<lower=0> K; // trials
  array[N] int<lower=0> y; // successes
  real min_alpha; // noone worse than this would be in the dataset
  real max_alpha;
}
parameters {
  real<lower=0> sigma; // scale parameter of generalised pareto distribution
  real<lower=-sigma/(max_alpha-min_alpha)> k; // shape parameter of generalised pareto distribution
  vector<lower=min_alpha,upper=max_alpha>[N] alpha; // success log-odds
}
model {
  sigma ~ normal(0, 1); // hyperprior
  alpha ~ gpareto(min_alpha, k, sigma); // prior (hierarchical)
  alpha ~ normal(-1.38, 0.4);  // prob between 0.1 and 0.4 on prob scale
  y ~ binomial_logit(K, alpha); // likelihood
  // note no explicit prior for k
}
