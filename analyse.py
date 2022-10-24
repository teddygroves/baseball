import arviz as az
import pandas as pd
from matplotlib import pyplot as plt
from scipy.special import expit

DATA_FILE = "baseball-hits-2006.csv"
ALPHA_PLOT_FILE = "alpha-plot.png"


def draw_alpha_plot():
    idata_gpareto = az.from_json("idata-gpareto.json")
    idata_normal = az.from_json("idata-normal.json")
    data = pd.read_csv(DATA_FILE).copy()
    alpha_qs_gpareto, alpha_qs_normal = (
        idata.posterior["alpha"]
        .quantile([0.05, 0.95], dim=("chain", "draw"))
        .to_series()
        .pipe(expit)
        .unstack("quantile")
        .add_prefix(name + "_")
        for idata, name in zip([idata_gpareto, idata_normal], ["gpareto", "normal"])
    )
    data = data.join(alpha_qs_gpareto).join(alpha_qs_normal)
    f, ax = plt.subplots(figsize=[12, 5])
    ax.scatter(data["K"], data["y"] / data["K"], label="Obs", color="black")
    for model, color in [("gpareto", "tab:blue"), ("normal", "tab:orange")]:
        ax.vlines(
            data["K"],
            data[f"{model}_0.05"],
            data[f"{model}_0.95"],
            label=model.capitalize() + " model 5%-95% posterior interval",
            color=color,
            zorder=0,
        )
    ax.set(
        title="Observed vs modelled batting averages",
        ylabel="Hit probability",
        xlabel="Number of at-bats",
    )
    ax.legend(frameon=False)
    return f, ax


if __name__ == "__main__":
    f, ax = draw_alpha_plot()
    f.savefig(ALPHA_PLOT_FILE, bbox_inches="tight")
