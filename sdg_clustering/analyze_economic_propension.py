import matplotlib.pyplot as plt
import os

def analyze_economic_propension(df_support, cluster_labels, fontsize_title=24, fontsize_general=20, result_folder="results"):
    """
    Analyzes the economic propension data.
    """
    # merging the cluster labels with the support DataFrame
    df_support.insert(0, "Cluster", cluster_labels)
    
    # create results folder if it does not exists
    if result_folder not in os.listdir():
        os.mkdir(result_folder)
    
    # save the DataFrame with cluster labels to a new Excel file
    df_support.to_excel(f"{result_folder}/support_with_clusters.xlsx", index=False)
    
    # for each cluster, calculate the average of each economic propension column
    cluster_means = df_support.groupby("Cluster").mean()
    
    # save the cluster means to a new Excel file
    cluster_means.to_excel(f"{result_folder}/cluster_means.xlsx", index=True)
    
    plt.figure(figsize=(10, 6))
    
    for cluster in cluster_means.index:
        plt.plot(cluster_means.columns, cluster_means.loc[cluster], marker='o', label=f'Cluster {cluster}')

    plt.xlabel("Sustainability Improvement Percentage", fontsize=fontsize_general, fontfamily="Times New Roman")
    plt.ylabel("Payment Percentage Increment", fontsize=fontsize_general, fontfamily="Times New Roman")
    plt.title("Payment Propensity by Cluster", fontsize=fontsize_title, fontfamily="Times New Roman")
    plt.xticks(ticks=[0, 1, 2], labels=["10", "20", "50"], fontsize=fontsize_general, fontfamily="Times New Roman")
    plt.yticks(fontsize=fontsize_general, fontfamily="Times New Roman")
    plt.legend(title="Cluster", title_fontsize=fontsize_general, fontsize=fontsize_general)
    plt.rcParams["font.family"] = "Times New Roman"
    
    save_path = f"{result_folder}/payment_propensity_by_cluster.png"
    plt.savefig(save_path)
    plt.close()
    
    
    