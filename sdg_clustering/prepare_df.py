def prepare_df(df_sdg, df_support):
    """
    Prepares the DataFrame for analysis by removing rows with all zeros and renaming columns.
    """
    # reordering df_sdg
    columns_to_drop_idx = list(range(0, 6)) + [-1]
    df_sdg = df_sdg.drop(df_sdg.columns[columns_to_drop_idx], axis=1)
    df_sdg.columns = ["SDG_1", "SDG_2", "SDG_3", "SDG_4", "SDG_5", "SDG_6", "SDG_7", "SDG_8", "SDG_9", "SDG_10", "SDG_11", "SDG_12", "SDG_13", "SDG_14", "SDG_15", "SDG_16", "SDG_17"]
        
    # reordering df_support
    columns_to_keep_idx = [9, 20, 31]
    df_support = df_support[df_support.columns[columns_to_keep_idx]]
    df_support.columns = ["s_10", "s_20", "s_50"]
    
    # merging the two DataFrames on their index
    df = df_sdg.merge(df_support, left_index=True, right_index=True)

    # removing rows beyond the survey responses and rows with an all-zero SDG vector
    df = df.dropna(subset=df_sdg.columns)
    df = df[(df.iloc[:, :17].replace(-1, 0) != 0).any(axis=1)]

    # removing rows with all zeros
    df = df[(df.T != 0).any()]
    
    # separating the SDG arrays and support arrays into two separate DataFrames
    df_sdg = df.iloc[:, :-3]
    df_support = df.iloc[:, -3:]

    return df_sdg, df_support
