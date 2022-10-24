functions {
#include gpareto.stan
}
data {
  int<lower=0> N; // items
  array[N] int<lower=0> K; // initial trials
  array[N] int<lower=0> y; // initial successes
  real min_alpha; // noone worse than this would be in the dataset
  real max_alpha;
}
parameters {
  real mu; // population mean of success log-odds
  real<lower=0> sigma; // population sd of success log-odds
  real<lower=-sigma/(max_alpha-min_alpha)> k; // shape parameter of generalised pareto distribution
  vector<lower=min_alpha,upper=max_alpha>[N] alpha; // success log-odds
}
model {
  mu ~ normal(-1, 1); // hyperprior
  sigma ~ normal(0, 1); // hyperprior
  alpha ~ gpareto(min_alpha, k, sigma); // prior (hierarchical)
  y ~ binomial_logit(K, alpha); // likelihood
  // note no explicit prior for k
}
