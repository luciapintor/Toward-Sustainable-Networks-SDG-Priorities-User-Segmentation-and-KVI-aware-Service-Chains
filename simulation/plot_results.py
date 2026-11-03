import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
 
 
def plot_results(plans, runs_file, summary_file, out_kvi_gain, out_premium, column_width=3.5, xmax=1.8,
                 fontfamily="Times New Roman", fontsize_general=12, fontsize_title=14):
    """This function plots the results of the simulation,
    including the mean gain of each end-to-end KVI over the baseline chain and
    the premium vs improvement of the selected chains, with the willingness-to-pay bound.
 
    Args:
        plans (dict): service plans, with label, color, and willingness-to-pay points of each plan
        runs_file (str): Excel file with one row per (run, plan)
        summary_file (str): Excel file with the statistics per plan
        out_kvi_gain (str): output path of the KVI gain figure
        out_premium (str): output path of the premium vs improvement figure
    """
 
    r = pd.read_excel(runs_file)
    s = pd.read_excel(summary_file).set_index("plan")
 
    kvis = [("HS", "H&S"), ("ACT", "ACT"), ("Water", "Water"), ("RE", "RE"), ("GHG", "GHG")]
 
    # the same font for every text element: labels, ticks, legend, titles, and math symbols
    style = {
        "font.family": "serif",
        "font.serif": [fontfamily],
        "mathtext.fontset": "custom",
        "mathtext.rm": fontfamily,
        "mathtext.it": f"{fontfamily}:italic",
        "mathtext.bf": f"{fontfamily}:bold",
        "mathtext.cal": fontfamily,
        "mathtext.sf": fontfamily,
        "font.size": fontsize_general,
        "axes.titlesize": fontsize_title,
        "axes.labelsize": fontsize_general,
        "xtick.labelsize": fontsize_general - 1,
        "ytick.labelsize": fontsize_general - 1,
        "legend.fontsize": fontsize_general - 1,
    }
 
    with plt.rc_context(style):
        plot_kvi_gain(s, out_kvi_gain, plans=plans, kvis=kvis, column_width=column_width)
        plot_premium(r, out_premium, plans=plans, column_width=column_width, xmax=xmax)
 
 
def save(fig, path):
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
 
 
def plot_kvi_gain(summary, out_path, plans, kvis, column_width=3.5):
    """Mean gain of each end-to-end KVI over the baseline chain (runs without fallback)."""
    fig, ax = plt.subplots(figsize=(column_width, 2.6))
    x = np.arange(len(kvis))
    width = 0.36
 
    for j, (p, info) in enumerate(plans.items()):
        vals = [summary.loc[p, f"gain_{k}_no_fallback"] for k, _ in kvis]
        pos = x + (j - 0.5) * (width + 0.02)
        ax.bar(pos, vals, width, color=info["color"], label=info["label"], zorder=3)
        k_dom = int(np.argmax(vals))           # label only the dominant KVI of each plan
        ax.text(pos[k_dom], vals[k_dom] + 0.008, f"+{vals[k_dom]:.2f}",
                ha="center", va="bottom", color="#222222")
 
    # ax.set_title("KVI gain over the baseline chain")
    ax.set_xticks(x)
    ax.set_xticklabels([lab for _, lab in kvis])
    ax.set_ylabel("Mean KVI gain")
    ax.set_ylim(0, 0.34)
    ax.grid(axis="y", color="#e6e6e6", linewidth=0.6, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="upper center")
    save(fig, out_path)
 
 
def plot_premium(runs, out_path, plans, column_width=3.5, xmax=1.8):
    """Premium vs. improvement of the selected chains, with the willingness-to-pay bound."""
    fig, ax = plt.subplots(figsize=(column_width, 2.9))
    grid = np.linspace(0, xmax, 200)
 
    for p, info in plans.items():
        d = runs[(runs["plan"] == p) & (~runs["fallback"])]
        ax.scatter(100 * d["delta_I"].clip(upper=xmax), 100 * d["delta_E"], s=5, alpha=0.35,
                   color=info["color"], edgecolors="none", zorder=3)
        pts = info["pi"]
        xs = np.array([0.0] + sorted(pts))
        ys = np.array([0.0] + [pts[k] for k in sorted(pts)])
        ax.plot(100 * grid, 100 * np.interp(grid, xs, ys), color=info["color"],
                linewidth=1.6, linestyle="--", zorder=4)
 
    # ax.set_title("Price premium vs. sustainability improvement")
    ax.set_xlim(0, 100 * xmax)
    ax.set_ylim(0, 20.5)
    ax.set_yticks([0, 5, 10, 15, 20])
    ax.set_xlabel(r"Sustainability improvement $\Delta I_m$ (%)")
    ax.set_ylabel(r"Price premium $\Delta E_m$ (%)")
    ax.grid(color="#e6e6e6", linewidth=0.6, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
 
    # legend in two columns: selected chains | willingness-to-pay bound
    handles = []
    for p in plans:
        handles.append(plt.Line2D([], [], marker="o", linestyle="", color=plans[p]["color"], markersize=4,
                                  label=f"Plan {p}: selected chains"))
        handles.append(plt.Line2D([], [], color=plans[p]["color"], linestyle="--", linewidth=1.6,
                                  label=f"Plan {p}: $\\pi(\\Delta I_m)$"))
    ax.legend(handles=handles, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.22),
              ncol=2, handletextpad=0.4, columnspacing=1.0)
    save(fig, out_path)
 
    clipped = int((runs[~runs["fallback"]]["delta_I"] > xmax).sum())
    print(f"Points with delta_I > {100 * xmax:.0f}% shown on the right edge: {clipped}")
 

