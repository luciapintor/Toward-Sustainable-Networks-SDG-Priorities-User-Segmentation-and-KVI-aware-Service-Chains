# Toward Sustainable Networks: SDG Priorities, User Segmentation, and KVI-aware Service Chains

This repository contains the code used in the paper *[title of the paper]* (doi soon available). It covers two parts of the paper:

1. **Survey analysis** (`main_w.py`): analysis of the responses to the survey *"Toward Sustainable Networks: Assessing SDG Priorities and User Preferences in Telecommunications"*. Respondents are clustered according to their SDG priorities, and for each cluster the code computes the weight vector $W$ used by the service plans and the average willingness to pay.
2. **Use case simulation** (`main_uc_simulation.py`): KVI-aware selection of service function chains for an immersive video streaming service, offered under two service plans derived from the user clusters.

## Repository structure

```
.
├── main_w.py                      # survey analysis: clustering, weights W, willingness to pay
├── main_uc_simulation.py          # use case: chain generation, ranking, and selection
├── sdg_clustering/   
│   └── analyze_economic_propension.py             # clustering of the SDG preference vectors
│   ├── calculate_w.py
│   ├── sdg_clustering.py
│   ├── clustering_KMEANS.py
│   ├── clustering_DBSCAN.py
│   └── print_average_sdg_array.py
│   └── profile_users.py 
├── simulation/                    # use case simulation
│   ├── generate_marketplace.py
│   └── chains.py
├── results/                       # output files (created by the scripts)
└── 2026_10_20_survey_responses.xlsx
```

## Requirements

- Python 3.10 or later
- `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `openpyxl`

```bash
pip install numpy pandas scikit-learn matplotlib openpyxl
```

## Data

The survey was conducted with Microsoft Forms between March 17th and October 20th, 2026, and collected 296 valid responses. 

## Survey analysis (`main_w.py`)

```bash
python main_w.py
```

Main steps:

1. The SDG preference vectors are read from `sdg_arrays`. The least important SDG (-1) can be set to 0 (`replace_negatives = True`), and respondents with a null vector are excluded.
2. The vectors are L2-normalized and clustered with K-means (`n_clusters = 5`, 50 random initializations, fixed random seed).
3. For each cluster, the mean SDG profile is rescaled so that the dominant SDG takes the value 10, giving the weight vector $W$ of the corresponding service plan.
4. For each cluster, the average willingness to pay is computed for the three levels of sustainability improvement (10%, 20%, and over 50%), excluding "I don't know" answers.

Outputs are saved in `results/`, including the cluster assignment of each respondent (`sdg_clusters_kmeans.xlsx`), the willingness to pay per cluster (`cluster_means.xlsx`), and the heatmap of the SDG profiles per cluster.

## Use case simulation (`main_uc_simulation.py`)

```bash
python main_uc_simulation.py
```

The simulation implements the framework of Section III of the paper:

1. **Marketplace generation**: each stage of the chain (transport and access, edge rendering, transcoding and delivery) is offered by alternative marketplace entries with synthetic KVI values and operational cost.
2. **Candidate chains**: all combinations of one entry per stage; the end-to-end KVIs are obtained with the aggregation operator of each indicator (`min`, `avg`, or `sum_norm`, i.e., the normalized sum).
3. **Ranking and selection** for each service plan:
   - feasibility: each end-to-end KVI must reach the target $v_n$ of the plan;
   - acceptability: the price premium $\Delta E_m$ with respect to the cheapest chain must not exceed the willingness to pay $\pi(\Delta I_m)$ of the target users, where $\Delta I_m$ is the sustainability improvement;
   - ranking: among feasible and acceptable chains, the chain with the lowest score $R(S_m)$ is selected; if none exists, the cheapest chain is used as a temporary solution.


Since certified per-function KVI data are not yet available, the marketplace entries are synthetic. All results are reproducible by keeping the same `seed`.

## Reproducibility

- K-means uses a fixed random seed and 50 initializations, so that the clusters do not depend on the initialization.
- The use case simulation uses the random generator of NumPy initialized with `seed`.

## Citation

If you use this code or the survey data, please cite:

```bibtex
@article{[key],
  author  = {Pintor, Lucia and Atzori, Luigi},
  title   = {TBD},
  journal = {IEEE Transactions on Network and Service Management},
  year    = {2026}
}
```

## License

The source code is released under the [MIT License](LICENSE).
The survey data are released under the
[Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
