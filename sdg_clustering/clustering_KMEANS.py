import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans

def clustering_KMEANS(X=None, n_clusters=3, random_state=42, n_init=50, result_folder="results"):
    """
    Function to perform K-Means clustering on the SDG arrays.

    Parameters:
    n_clusters (int): The number of clusters to form.
    X (pandas.DataFrame): The DataFrame containing the SDG arrays.
    random_state (int): The random state for reproducibility.
    n_init (int): The number of times the k-means algorithm will be run with different centroid seeds.
    Returns:
    None
    """
    
    Xn = normalize(X)                      # L2 (euclidean) normalization 
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=n_init)  # Initialize KMeans with specified number of clusters and random state
    clusters = kmeans.fit_predict(Xn)
    print(f"#"*25)
    print(f"Clustering with K-Means using {n_clusters} clusters")

    num_clusters = len(set(clusters))
    print(f"Number of clusters found: {num_clusters}")

    # saving the results to an Excel file
    X.insert(0, "Cluster", clusters)  # Insert the cluster labels as the first column
    output_file = f"{result_folder}/sdg_clusters_kmeans.xlsx"
    X.to_excel(output_file, index=False)
    
    return X
    