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

import numpy as np

from simulation.generate_marketplace import generate_marketplace
from simulation.chains import candidate_chains, select_chain

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
plans = {
    "A": { #  (Health, cl. 4)
        "w": {"HS": 10.0, "Water": 1.6, "RE": 1.1, "GHG": 0.4, "ACT": 0.8},        # weights
        "v": {"HS": 0.60, "Water": 0.40, "RE": 0.40, "GHG": 0.40, "ACT": 0.40},    # requirements
        "pi": {0.1: 0.074, 0.2: 0.120, 0.5: 0.177},                                # willingness to pay
    },
    "B": { #  (Climate, cl. 1)
        "w": {"HS": 0.6, "Water": 1.9, "RE": 0.7, "GHG": 10.0, "ACT": 1.0},
        "v": {"HS": 0.40, "Water": 0.40, "RE": 0.40, "GHG": 0.60, "ACT": 0.40},
        "pi": {0.1: 0.059, 0.2: 0.103, 0.5: 0.192},
    },
}
 
mu = 0.5                           # trade-off sustainability / cost in R(S_m)
seed = 42

# Synthetic ranges for the marketplace entries
kvi_data = {
    "HS":     {"ranges": (0.2, 1.0), "aggregation": "min"},          # normalized provider-level scores
    "ACT":    {"ranges": (0.2, 1.0), "aggregation": "min"},          # normalized provider-level scores
    "Water":  {"ranges": (0.2, 1.0), "aggregation": "avg"},          # normalized water use efficiency of the site
    "RE":     {"ranges": (0.1, 1.0), "aggregation": "avg"},          # share of renewable energy of the site
    "GHG":    {"ranges": (0.0, 1.0), "aggregation": "sum_norm"},     # gCO2/kWh of the local grid
}

cost_noise = 0.10                           # std of the multiplicative cost noise
 
 
# ---------------------------------------------------------------------------
# Marketplace generation
# ---------------------------------------------------------------------------

rng = np.random.default_rng(seed)

marketplace = generate_marketplace(rng, stages=stages, kvi_data=kvi_data, cost_noise=cost_noise)
chains = candidate_chains(marketplace=marketplace, kvi_data=kvi_data)

records = []

for name, plan in plans.items():
    res = select_chain(chains, plan, kvi_data, mu=mu)
    res.update({"plan": name})
    records.append(res)
    
for r in records:
    print(r)