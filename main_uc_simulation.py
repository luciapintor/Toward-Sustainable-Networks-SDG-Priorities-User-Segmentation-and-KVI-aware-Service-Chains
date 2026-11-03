"""
Use case simulation: KVI-aware selection of service function chains
under two service plans (Health and Climate), repeated over randomly
generated marketplaces.
 
The implementation follows Section III of the paper:
    s_{m,n}  end-to-end KVIs (min / avg / normalized sum)
    R(S_m)   ranking function (Eq. sigmoid), argmin
    DeltaE_m premium w.r.t. the baseline chain (Eq. dc)
    I_m      weighted sustainability level (Eq. Im)
    DeltaI_m improvement w.r.t. the baseline chain (Eq. dIm)
    acceptability: DeltaE_m <= pi(DeltaI_m) (Eq. accept)
"""
import os
import numpy as np

from simulation.monte_carlo import *
from simulation.plot_results import plot_results
from simulation.example import example_marketplace

# ---------------------------------------------------------------------------
# Configuration use case simulation
# ---------------------------------------------------------------------------
stages = {
    "1.Transport and access":     {"base_cost": 1.0, "alternatives": 2}, 
    "2.Edge rendering":           {"base_cost": 1.5, "alternatives": 3}, 
    "3.Transcoding and delivery": {"base_cost": 1.2, "alternatives": 3}
    }

# Service plans: weights from profile_users (cluster mean profile, dominant SDG = 10),
# willingness to pay from Table tab:sdg_clusters (lower bound encoding, % -> fraction)
#
# Targets (requirements) v: 0.5 on the dominant KVI of each plan, 0.25 on the others.
# These values result from a trade-off between the strictness of the requirements and the
# availability of feasible chains: since provider-level KVIs are aggregated with the minimum,
# a single non-compliant provider excludes the whole chain. With the previous targets
# (0.6 on the dominant KVI, 0.4 on the others), no candidate chain satisfied all the targets
# in about three marketplaces out of four.
plans = {
    "A": { #  (Health, cl. 4)
        "label": "Plan A (Health)",
        "color": "#2a78d6",
        "w": {"HS": 10.0, "Water": 1.6, "RE": 1.1, "GHG": 0.4, "ACT": 0.8},        # weights
        # "v": {"HS": 0.60, "Water": 0.40, "RE": 0.40, "GHG": 0.40, "ACT": 0.40},  # previous requirements
        "v": {"HS": 0.50, "Water": 0.25, "RE": 0.25, "GHG": 0.25, "ACT": 0.25},    # requirements
        "pi": {0.1: 0.074, 0.2: 0.120, 0.5: 0.177},                                # willingness to pay
    },
    "B": { #  (Climate, cl. 1)
        "label": "Plan B (Climate)",
        "color": "#eb6834",
        "w": {"HS": 0.6, "Water": 1.9, "RE": 0.7, "GHG": 10.0, "ACT": 1.0},
        # "v": {"HS": 0.40, "Water": 0.40, "RE": 0.40, "GHG": 0.60, "ACT": 0.40},  # previous requirements
        "v": {"HS": 0.25, "Water": 0.25, "RE": 0.25, "GHG": 0.50, "ACT": 0.25},    # requirements
        "pi": {0.1: 0.059, 0.2: 0.103, 0.5: 0.192},
    },
}
 
mu = 0.5                           # trade-off sustainability / cost in R(S_m)
seed = 42
n_marketplaces = 1000              # Monte Carlo repetitions

# Synthetic ranges for the marketplace entries
kvi_data = {
    "HS":     {"ranges": (0.2, 1.0), "aggregation": "min"},          # normalized provider-level scores
    "ACT":    {"ranges": (0.2, 1.0), "aggregation": "min"},          # normalized provider-level scores
    "Water":  {"ranges": (0.2, 1.0), "aggregation": "avg"},          # normalized water use efficiency of the site
    "RE":     {"ranges": (0.1, 1.0), "aggregation": "avg"},          # share of renewable energy of the site
    "GHG":    {"ranges": (0.0, 1.0), "aggregation": "sum_norm"},     # gCO2/kWh of the local grid
}

cost_noise = 0.10                           # std of the multiplicative cost noise
cost_corr = 0.4                             # extra cost per unit of sustainability score 
 
result_folder = "results"
kvi_gain_file = f"{result_folder}/uc_simulation_kvi_gain.png" 
premium_file = f"{result_folder}/uc_simulation_premium.png"
runs_file = f"{result_folder}/uc_simulation_runs.xlsx"
summary_file = f"{result_folder}/uc_simulation_summary.xlsx"
 
# ---------------------------------------------------------------------------
# Monte Carlo simulation
# ---------------------------------------------------------------------------
os.makedirs(result_folder, exist_ok=True)

rng = np.random.default_rng(seed)
 
results = run_monte_carlo(rng, n_marketplaces=n_marketplaces, stages=stages, kvi_data=kvi_data,
                          plans=plans, mu=mu, cost_noise=cost_noise, cost_corr=cost_corr)
summary, different_chains = summarize(results, kvi_data=kvi_data, plans=plans)
 
# saving the results
results.to_excel(runs_file, index=False)
summary.to_excel(summary_file, index=False)
 
pd.set_option("display.width", 200)
print(summary.round(3).T)
print(f"\nShare of marketplaces where the plans select different chains: {different_chains:.1%}")

plot_results(plans=plans, runs_file=runs_file, summary_file=summary_file, out_kvi_gain=kvi_gain_file, out_premium=premium_file)
