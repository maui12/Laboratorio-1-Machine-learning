import pandas as pd
from configuracion import PARQUET_OUTPUT_NAME, PICKLE_OUTPUT_NAME

def guardar_corpus(df):
    df.to_parquet(PARQUET_OUTPUT_NAME, index=False)
    df.to_pickle(PICKLE_OUTPUT_NAME)
    print(f"Archivos .parquet y .pkl generados con éxito.")

def cargar_corpus():
    return pd.read_parquet(PARQUET_OUTPUT_NAME)