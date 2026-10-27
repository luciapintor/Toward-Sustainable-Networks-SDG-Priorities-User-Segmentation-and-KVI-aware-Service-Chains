from sdg_clustering.calculate_w import calculate_w

# ---------------------------------------------------------------------------
# Configuration w calculation
# ---------------------------------------------------------------------------
xlsx_file = "2026_10_20_survey_responses.xlsx"
sheet_name_sdg = "sdg_arrays"
sheet_support_survey = "support_arrays"

result_folder = "results"

clustering_method = "K-Means"  # or "DBSCAN"
n_clusters = 5
eps = 0.3
min_samples = 3
replace_negatives = True

show_plots = False
show_full_plots = False

w = calculate_w(xlsx_file=xlsx_file, sheet_name_sdg=sheet_name_sdg, sheet_support_survey=sheet_support_survey,
                clustering_method=clustering_method, n_clusters=n_clusters, eps=eps, min_samples=min_samples, 
                replace_negatives=replace_negatives, show_plots=show_plots, show_full_plots=show_full_plots,
                result_folder=result_folder)

