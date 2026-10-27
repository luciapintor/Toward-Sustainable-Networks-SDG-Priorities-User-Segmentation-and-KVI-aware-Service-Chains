import itertools
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# End-to-end aggregation (Section III-E)
# ---------------------------------------------------------------------------
def candidate_chains(marketplace, kvi_data):
    """Builds all candidate chains and their end-to-end KVIs s_{m,n} and cost E_m."""

    # find all the combinations of alternatives (each stage can appear only once in each combination)
    combos = [list(c) for c in itertools.product(*marketplace.groupby("stage")["id"].unique())]
    
    chains = []
    
    for combo in combos:
        combo_details = marketplace[marketplace["id"].isin(combo)]
        aggregation = {}
        for kvi in kvi_data:
            if kvi_data[kvi]["aggregation"] == "min":
                aggregation[kvi] = combo_details[kvi].min()
            elif kvi_data[kvi]["aggregation"] == "avg":
                aggregation[kvi] = combo_details[kvi].mean()
            elif kvi_data[kvi]["aggregation"] == "sum_norm":
                # Eq. (sum_norm): s = 1 - sum / f_max, with f_max = all functions at the maximum value
                f_max = len(combo) * kvi_data[kvi]["ranges"][1]
                aggregation[kvi] = 1.0 - combo_details[kvi].sum() / f_max
        chains.append({"ids": combo, "details": combo_details, "aggregation": aggregation, "cost": combo_details["cost"].sum()})
    return chains
 
# ---------------------------------------------------------------------------
# Ranking and selection (Section III-F, Algorithm 1)
# ---------------------------------------------------------------------------
def select_chain(chains, plan, kvi_data, mu=0.5):
    w = np.array([plan["w"][k] for k in kvi_data.keys()])
    v = np.array([plan["v"][k] for k in kvi_data.keys()])
    
    S = pd.DataFrame([c["aggregation"] for c in chains])[list(kvi_data.keys())].to_numpy()
    E = np.array([c["cost"] for c in chains])
 
    # baseline: chain selected if sustainability were not considered (cheapest)
    b = int(np.argmin(E))
    I = S @ w / w.sum()                                   # Eq. (Im)
    delta_E = (E - E[b]) / E[b]                           # Eq. (dc)
    delta_I = (I - I[b]) / I[b]                           # Eq. (dIm)
    pi = pi_function(delta_I, plan["pi"])
 
    feasible = np.all(S >= v, axis=1)                     # s_{m,n} >= v_n for all active n
    acceptable = delta_E <= pi                            # Eq. (accept)
    admissible = feasible & acceptable
 
    # ranking function (Eq. sigmoid), cost normalized to [0, 1] to be comparable
    E_norm = E / E.max()
    R = (1 - mu) / (1 + np.exp(-((v - S) * w).sum(axis=1))) + mu * E_norm
 
    if admissible.any():
        idx = np.flatnonzero(admissible)
        m = int(idx[np.argmin(R[idx])])
        fallback = False
    else:
        m = b                                             # temporary, SLA-compliant chain
        fallback = True
 
    return {
        "chain": chains[m] ["ids"], "fallback": fallback,
        "n_feasible": int(feasible.sum()), "n_acceptable": int(acceptable.sum()),
        "n_admissible": int(admissible.sum()),
        "delta_E": delta_E[m], "delta_I": delta_I[m], "I": I[m], "I_baseline": I[b],
        "kvis": chains[m]["aggregation"], 
        "kvis_baseline": chains[b]["aggregation"],
    }
 
# ---------------------------------------------------------------------------
# Willingness to pay
# ---------------------------------------------------------------------------
def pi_function(delta_i, points):
    """
    Piecewise-linear interpolation of the surveyed points.
    pi = 0 for delta_i <= 0; linear from (0, 0) to the first point;
    constant beyond the last point (no extrapolation).
    """
    x = np.array([0.0] + sorted(points))
    y = np.array([0.0] + [points[p] for p in sorted(points)])
    return np.where(delta_i <= 0, 0.0, np.interp(delta_i, x, y))
 