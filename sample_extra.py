import pandas as pd
from sample import fit_models, DATA_FILE

STAN_FILE_GPARETO_REG = "model-gpareto-reg.stan"
STAN_FILE_NORMAL_AT_BATS = "model-normal-at-bats.stan"

if __name__ == "__main__":
    data_df = pd.read_csv(DATA_FILE)
    fit_models(
        {
            "gpareto-reg": STAN_FILE_GPARETO_REG,
            "normal-at-bats": STAN_FILE_NORMAL_AT_BATS
        },
        data_df
    )
