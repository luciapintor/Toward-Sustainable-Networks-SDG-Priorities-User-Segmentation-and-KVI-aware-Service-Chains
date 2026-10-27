import pandas as pd
from copy import deepcopy

from sdg_clustering.prepare_df import prepare_df
from sdg_clustering.clustering_DBSCAN import clustering_DBSCAN
from sdg_clustering.clustering_KMEANS import clustering_KMEANS
from sdg_clustering.print_average_sdg_array import print_average_sdg_array
from sdg_clustering.profile_users import profile_users
from sdg_clustering.analyze_economic_propension import analyze_economic_propension

def calculate_w(xlsx_file, sheet_name_sdg, sheet_support_survey, clustering_method, n_clusters, eps, min_samples, 
                replace_negatives=True, show_plots=False, show_full_plots=False, result_folder="results"):
    """This function reads the SDG and support survey data from an Excel file, 
    prepares the data, performs clustering on the SDG arrays, analyzes the economic propension, 
    and profiles the users based on the clustering results.

    Args:
        xlsx_file (_type_): _description_
        sheet_name_sdg (_type_): _description_
        sheet_support_survey (_type_): _description_
        clustering_method (_type_): _description_
        n_clusters (_type_): _description_
        eps (_type_): _description_
        min_samples (_type_): _description_
        replace_negatives (bool, optional): _description_. Defaults to True.
        show_plots (bool, optional): _description_. Defaults to False.
        show_full_plots (bool, optional): _description_. Defaults to False.
        result_folder
    """
    # reading the sheets of the xlsx file with pandas
    sdg_df = pd.read_excel(xlsx_file, sheet_name=sheet_name_sdg)
    support_df = pd.read_excel(xlsx_file, sheet_name=sheet_support_survey)

    # preparing the DataFrame for analysis
    df_sdg, df_support = prepare_df(sdg_df, support_df)

    # clustering the SDG arrays and printing the average SDG array for each cluster
    df_sdg = sdg_clustering(df_sdg, clustering_method=clustering_method, n_clusters=n_clusters, 
                            eps=eps, min_samples=min_samples, replace_negatives=replace_negatives, 
                            show_plots=show_plots, show_full_plots=show_full_plots, result_folder=result_folder)


    # studying the propension to pay
    analyze_economic_propension(df_support, df_sdg["Cluster"], result_folder=result_folder )

    return profile_users(df=df_sdg) # w

def sdg_clustering(df, clustering_method="K-Means", n_clusters=5, eps=0.3, min_samples=3, replace_negatives=True, 
                   show_plots=False, show_full_plots=False, result_folder="results"):
    """
    Clusters the SDG DataFrame.
    """
    
    if replace_negatives:
            df = df.replace(-1, 0)

    if clustering_method == "DBSCAN":
        # using DBSCAN to cluster the SDG arrays
        df = clustering_DBSCAN(eps=eps, min_samples=min_samples, X=deepcopy(df), result_folder=result_folder)
    elif clustering_method == "K-Means":
        # using K-Means to cluster the SDG arrays
        df = clustering_KMEANS(n_clusters=n_clusters, X=deepcopy(df), result_folder=result_folder)
        
    print_average_sdg_array(df, clustering_method=clustering_method, show_plots=show_plots, show_full_plots=show_full_plots, result_folder=result_folder)

    return df

if __name__ == "__main__":
    xlsx_file = "2026_10_20_survey_responses.xlsx"
    sheet_name_sdg = "sdg_arrays"
    sheet_support_survey = "support_arrays"

    clustering_method = "K-Means"  # or "DBSCAN"
    n_clusters = 5
    eps = 0.3
    min_samples = 3
    replace_negatives = True

    show_plots = False
    show_full_plots = False

    w = calculate_w(xlsx_file=xlsx_file, sheet_name_sdg=sheet_name_sdg, sheet_support_survey=sheet_support_survey,
                    clustering_method=clustering_method, n_clusters=n_clusters, eps=eps, min_samples=min_samples, 
                    replace_negatives=replace_negatives, show_plots=show_plots, show_full_plots=show_full_plots)
