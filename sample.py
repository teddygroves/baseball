import arviz as az
import cmdstanpy
import pandas as pd
from scipy.special import logit

STAN_FILE_NORMAL = "model-normal.stan"
STAN_FILE_GPARETO = "model-gpareto.stan"
DATA_FILE = "baseball-hits-2006.csv"
SAMPLE_KWARGS = {
    "chains": 4,
    "iter_warmup": 1000,
    "iter_sampling": 1000,
    "show_progress": False
}
SAMPLE_KWARGS_GPARETO = {
    "max_treedepth": 12,
    "adapt_delta": 0.99,
}
MIN_ALPHA = logit(0.005) # you probably need a true average >0.5% to get in the dataset
MAX_ALPHA = logit(0.99)  # noone has a true average of 99%

def get_summary(idata):
    summary_ss = az.summary(idata.sample_stats, var_names=["lp", "diverging"])
    summary_vars = az.summary(idata, var_names="~alpha", filter_vars="like")
    return pd.concat([summary_ss, summary_vars])


def main():
    model_normal = cmdstanpy.CmdStanModel(stan_file=STAN_FILE_NORMAL)
    model_gpareto = cmdstanpy.CmdStanModel(stan_file=STAN_FILE_GPARETO)
    data_df = pd.read_csv(DATA_FILE)
    data_dict = {
        "N": data_df.shape[0],
        "y": data_df["y"].tolist(),
        "K": data_df["K"].tolist(),
        "min_alpha": MIN_ALPHA,
        "max_alpha": MAX_ALPHA,
    }
    for model, name in zip([model_normal, model_gpareto], ["normal", "gpareto"]):
        sample_kwargs = (
            SAMPLE_KWARGS
            if name != "gpareto"
            else {**SAMPLE_KWARGS, **SAMPLE_KWARGS_GPARETO}
        )
        print(f"Fitting model {name}")
        mcmc = model.sample(data=data_dict, **sample_kwargs)
        idata = az.from_cmdstanpy(mcmc)
        print(get_summary(idata))
        idata_file = f"idata-{name}.json"
        print(f"Saving idata to {idata_file}")
        idata.to_json(idata_file)


if __name__ == "__main__":
    main()
