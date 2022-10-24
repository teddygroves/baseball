import arviz as az
from matplotlib import pyplot as plt
from scipy.special import expit

ALPHA_FORESTPLOT_FILE = "alpha-forestplot.png"

def draw_alpha_forestplot():
    idata_gpareto = az.from_json("idata-gpareto.json")
    idata_normal = az.from_json("idata-normal.json")
    alpha_means_gpareto = idata_gpareto.posterior["alpha"].mean(("chain", "draw"))
    alpha_means_normal = idata_normal.posterior["alpha"].mean(("chain", "draw"))
    sorted_alphas_gpareto, sorted_alphas_normal = (
        idata.posterior["alpha"].sortby(alpha_means).coords["alpha_dim_0"]
        for idata, alpha_means in [
            (idata_gpareto, alpha_means_gpareto),
            (idata_normal, alpha_means_normal),
        ]
    )
    az.plot_forest(
        [idata_gpareto, idata_normal],
        model_names=["gpareto", "normal"],
        var_names="alpha",
        coords={"alpha_dim_0": sorted_alphas_normal},
        kind="forestplot",
        combined=True,
        figsize=[7, 30],
        transform=expit,
    )
    f = plt.gcf()
    ax = plt.gca()
    ax.set_yticks([])
    ax.set(ylabel="batter", xlabel="hit probability", title="Results comparison")
    return f, ax


if __name__ == "__main__":
    f, ax = draw_alpha_forestplot()
    f.savefig(ALPHA_FORESTPLOT_FILE, bbox_inches="tight")
