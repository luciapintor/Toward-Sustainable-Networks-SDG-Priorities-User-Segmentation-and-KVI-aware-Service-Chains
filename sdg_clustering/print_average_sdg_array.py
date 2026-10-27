import pandas as pd
import matplotlib.pyplot as plt

def print_average_sdg_array(df, clustering_method, show_plots=False, show_full_plots=False, font="Times New Roman", result_folder="results"):
    clusters = df["Cluster"]
    cluster_counts = pd.Series(clusters).value_counts()
    print("Number of points in each cluster:")
    print(cluster_counts)
    
    plot_cluster_average_heatmap(df, clustering_method, show_plots=show_plots, font=font, result_folder=result_folder)

    plot_cluster_barplots(df, clustering_method, show_full_plots=show_full_plots, font=font, result_folder=result_folder)
    
            
def plot_cluster_average_heatmap(df, clustering_method, show_plots=False, font="Times New Roman", result_folder="results"):
    """
    This function creates a heatmap of the average SDG arrays for each cluster of the dataframe df.

    Args:
        df (_type_): _description_
        clustering_method (_type_): _description_
        show_plots (bool, optional): _description_. Defaults to False.
    """
    # --- average SDG array per cluster ---
    G = df.groupby("Cluster").mean()
    M = G.values                       # matrice cluster x SDG

    # --- heatmap ---
    fig, ax = plt.subplots(figsize=(13, 0.7 * len(G) + 2), constrained_layout=True)
    im = ax.imshow(M, cmap="Blues", vmin=M.min(), vmax=M.max(), aspect="auto")

    ax.set_xlabel("SDG", fontsize=16, fontfamily=font)
    ax.set_ylabel("Cluster", fontsize=16, fontfamily=font)
    ax.set_xticks(range(M.shape[1]))
    ax.set_xticklabels(G.columns, rotation=45, ha="right", fontsize=12, fontfamily=font)
    ax.set_yticks(range(M.shape[0]))
    ax.set_yticklabels(G.index, fontsize=12, fontfamily=font)

    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if M[i, j] >= 0.08:
                ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center", fontsize=12, fontfamily=font,
                        color="white" if M[i, j] > M.max() * 0.6 else "black")

    fig.colorbar(im, ax=ax, shrink=1.2, label="Mean preference score")
    ax.set_title(f"SDG preference profile by cluster ({clustering_method})", fontsize=18, fontfamily=font)
                
    plt.rcParams["font.family"] = font
        
    plt.savefig(f"{result_folder}/{clustering_method}_SDG_avg_preference.png", dpi=300, bbox_inches="tight")
    
    if show_plots:
        plt.show()
    else:
        plt.close()
        
def plot_cluster_barplots(df, clustering_method, show_full_plots=False, font="Times New Roman", result_folder="results"):
    """
    This function creates bar plots of the average SDG arrays for each cluster of the dataframe df.

    Args:
        df (_type_): _description_      
        clustering_method (_type_): _description_
        show_full_plots (bool, optional): _description_. Defaults to False.  
    """
    clusters = df["Cluster"]
    
    for cluster_id in clusters.unique():
            cluster_data = df[clusters == cluster_id].drop("Cluster", axis=1)
    
            fig, axes = plt.subplots(3, 6, figsize=(16, 8), constrained_layout=True)
            fig.suptitle(f"Samples of cluster {cluster_id} ({clustering_method})", fontsize=14)
            axes = axes.flat
    
            for i, column in enumerate(cluster_data.columns):
                ax = axes[i]
                values = cluster_data[column]
                mean_val = values.mean()
                ax.bar(range(1, len(values) + 1), values, alpha=0.6)
                ax.axhline(mean_val, color="red", linestyle="--", linewidth=1.2,
                           label=f"mean {mean_val:.2f}")
                ax.set_title(f"{column}", fontsize=8)
                ax.set_xlabel("Index", fontsize=8)
                ax.set_ylabel("Value", fontsize=8)
                ax.tick_params(labelsize=7)
                ax.set_ylim(0, 3)                 # set the y-axis limit to 0.9
                ax.set_yticks([0, 1, 2, 3])   # only these values on the y-axis
                ax.legend(fontsize=6, loc="upper right")
            
    
            # hide any unused subplots (there is a maximum of 17 SDGs, so we will have an extra subplot)
            for j in range(len(cluster_data.columns), len(axes)):
                axes[j].set_visible(False)
                            
            plt.rcParams["font.family"] = font
                
            # save the figure
            plt.savefig(f"{result_folder}\{clustering_method}_cluster_{cluster_id}.png", dpi=300, bbox_inches="tight")
    
            if show_full_plots: 
                plt.show()
                
            else:
                plt.close()