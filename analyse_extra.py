import arviz as az
from analyse import draw_alpha_plot

if __name__ == "__main__":
    data = pd.read_csv(DATA_FILE)
    idata_gpareto = az.from_json("idata-gpareto-reg.json")
    idata_normal = az.from_json("idata-normal-at-bats.json")
    f, ax = draw_alpha_plot(idata_gpareto, idata_normal, data)
    f.savefig(ALPHA_PLOT_FILE, bbox_inches="tight")
