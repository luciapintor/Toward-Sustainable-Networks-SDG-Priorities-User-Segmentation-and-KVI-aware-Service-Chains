import numpy as np
import pandas as pd

from simulation.generate_marketplace import generate_marketplace
from simulation.chains import candidate_chains, select_chain


# ---------------------------------------------------------------------------
# Monte Carlo over randomly generated marketplaces
# ---------------------------------------------------------------------------
def run_monte_carlo(rng, n_marketplaces, stages, kvi_data, plans, mu, cost_noise, cost_corr):
    """
    Repeats the chain selection over n_marketplaces random marketplaces.
    In each run, all the plans are evaluated on the same marketplace, so that
    the differences between plans do not depend on the random draws.
    Returns one row per (run, plan).
    """
    records = []

    for run in range(n_marketplaces):
        marketplace = generate_marketplace(rng, stages=stages, kvi_data=kvi_data,
                                           cost_noise=cost_noise, cost_corr=cost_corr)
        chains = candidate_chains(marketplace=marketplace, kvi_data=kvi_data)

        for name, plan in plans.items():
            res = select_chain(chains, plan, kvi_data, mu=mu)

            row = {
                "run": run, "plan": name, "chain": "-".join(res["chain"]),
                "fallback": res["fallback"],
                "n_chains": len(chains), "n_feasible": res["n_feasible"],
                "n_acceptable": res["n_acceptable"], "n_admissible": res["n_admissible"],
                "delta_E": res["delta_E"], "delta_I": res["delta_I"],
                "I": res["I"], "I_baseline": res["I_baseline"],
            }
            row.update({f"s_{kvi}": value for kvi, value in res["kvis"].items()})
            row.update({f"base_{kvi}": value for kvi, value in res["kvis_baseline"].items()})
            records.append(row)

    return pd.DataFrame(records)


def summarize(results, kvi_data, plans):
    """
    Aggregated statistics per plan:
    - fallback rate: share of marketplaces where no chain is feasible and acceptable
    - mean number of feasible, acceptable, and admissible chains
    - mean and standard deviation of the premium (delta_E) and of the improvement (delta_I)
    - mean gain of each end-to-end KVI with respect to the baseline chain
    Statistics on delta_E, delta_I, and gains are computed both on all runs and
    only on the runs without fallback (where the selected chain differs from the baseline).
    """
    rows = []

    for name in plans:
        r = results[results["plan"] == name]
        ok = r[~r["fallback"]]
        n = len(r)
        fallback_rate = r["fallback"].mean()

        row = {
            "plan": name,
            "runs": n,
            "fallback_rate": fallback_rate,
            "fallback_ci95": 1.96 * np.sqrt(fallback_rate * (1 - fallback_rate) / n),
            "feasible_chains": r["n_feasible"].mean(),
            "acceptable_chains": r["n_acceptable"].mean(),
            "admissible_chains": r["n_admissible"].mean(),
            "delta_E_mean": r["delta_E"].mean(), "delta_E_std": r["delta_E"].std(),
            "delta_I_mean": r["delta_I"].mean(), "delta_I_std": r["delta_I"].std(),
            "delta_E_mean_no_fallback": ok["delta_E"].mean(),
            "delta_I_mean_no_fallback": ok["delta_I"].mean(),
        }
        for kvi in kvi_data:
            row[f"gain_{kvi}"] = (r[f"s_{kvi}"] - r[f"base_{kvi}"]).mean()
            row[f"gain_{kvi}_no_fallback"] = (ok[f"s_{kvi}"] - ok[f"base_{kvi}"]).mean()
        rows.append(row)

    summary = pd.DataFrame(rows)

    # share of marketplaces where the plans select different chains
    pivot = results.pivot(index="run", columns="plan", values="chain")
    different_chains = (pivot.nunique(axis=1) > 1).mean()

    return summary, different_chains
