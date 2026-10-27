def profile_users(df, max_value=10):
    """
    Computes the weight vector W of each cluster: mean SDG profile of the
    cluster, rescaled so that the dominant SDG takes the value 10.
    """
    
    w = {}
    
    sdg_columns = [c for c in df.columns if c.startswith("SDG_")]

    for cluster in sorted(df["Cluster"].unique()):
        mean_profile = df.loc[df["Cluster"] == cluster, sdg_columns].mean()
        w[cluster] = (max_value * mean_profile / mean_profile.max()).round(1)
        print(f"Cluster {cluster}: w: {w[cluster].tolist()}")
        
    return w