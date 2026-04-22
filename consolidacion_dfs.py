import pandas as pd

def generar_consolidado(df_x, df_rss, df_csv=None):
    """
    Une los DataFrames parciales en una sola estructura homogénea.
    """
    dataframes_a_unir = []
    
    if df_x is not None and not df_x.empty:
        dataframes_a_unir.append(df_x)
    
    if df_rss is not None and not df_rss.empty:
        dataframes_a_unir.append(df_rss)
        
    if df_csv is not None and not df_csv.empty:
        dataframes_a_unir.append(df_csv)

    # 2. Unión vertical
    if not dataframes_a_unir:
        print("Advertencia: No hay datos para consolidar.")
        return pd.DataFrame()

    df_consolidado = pd.concat(dataframes_a_unir, ignore_index=True)
    
    print(f"Union de dataframes exitosa. Total de registros: {len(df_consolidado)}")
    return df_consolidado
