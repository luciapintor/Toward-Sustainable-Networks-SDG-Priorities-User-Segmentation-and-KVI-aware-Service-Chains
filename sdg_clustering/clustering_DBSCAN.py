import pandas as pd
from sklearn.cluster import DBSCAN

def clustering_DBSCAN(eps=0.3, min_samples=3, X=None, result_folder="results"):
    """
    Function to perform DBSCAN clustering on the SDG arrays.
    
    Parameters:
    eps (float): The maximum distance between two samples for them to be considered as in the same neighborhood.
    min_samples (int): The number of samples in a neighborhood for a point to be considered as a core point.
    
    Returns:
    None
    """
        
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
    clusters = dbscan.fit_predict(X)
    print(f"#"*25)
    print(f"Clustering with DBSCAN using eps={eps} and min_samples={min_samples}")

    num_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
    print(f"Number of clusters found: {num_clusters}")

    # saving the results to an Excel file
    X.insert(0, "Cluster", clusters)  # Insert the cluster labels as the first column
    output_file = f"{result_folder}/sdg_clusters_dbscan.xlsx"
    X.to_excel(output_file, index=False)
    
    return X