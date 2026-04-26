from getpass import getpass
import fuentes_x
import fuentes_cooperativa
import fuentes_csv   
import preprocesamiento
import analisis
import consolidacion_dfs
import persistencia_binaria
import persistencia_nosql

from token_x import X_BEARER_TOKEN
from configuracion import (
    X_QUERY,X_MAX_RESULTS,CSV_FILE_PATH,
    MONGO_DB_NAME,MONGO_COLLECTION_NAME
)

import os

from fuentes_csv import cargar_datos_csv

def main():
    print("=== INICIANDO PIPELINE DE EXTRACCIÓN DE DATOS ===")
    
    print("\n[1/7] Extrayendo datos de X...")
    df_x = fuentes_x.buscar_posts_x(
        query=X_QUERY,
        bearer_token=X_BEARER_TOKEN,
        max_results=X_MAX_RESULTS
    )
    
    print("\n[2/7] Extrayendo datos de RSS Cooperativa...")
    df_rss = fuentes_cooperativa.extraer_rss_cooperativa()
    
    print(f"\n[3/7] Cargando fuente opcional CSV ({CSV_FILE_PATH})...")
    df_csv = fuentes_csv.cargar_datos_csv(CSV_FILE_PATH)
    
    print("\n[4/7] Consolidando el corpus de datos...")
    df_corpus = consolidacion_dfs.generar_consolidado(df_x, df_rss, df_csv)
    
    if df_corpus.empty:
        print("Error crítico: El corpus está vacío. Se aborta la ejecución.")
        return
        
    print("\n[5/7] Guardando respaldos binarios... (Parquet)")
    persistencia_binaria.guardar_corpus(df_corpus)

    print("\n[6/7] Ejecutando limpieza y análisis (TF-IDF, Clusters, PCA)...")
  
    df_corpus["texto_limpio"] = df_corpus["texto"].apply(preprocesamiento.limpiar_texto)
    # Ejecutar modelos de ML
    df_corpus = analisis.ejecutar_analisis(df_corpus)
 
    print("\n[7/7] Sincronizando con MongoDB...")

    mongodb_uri = getpass("Ingresa tu URI de MongoDB (o presiona Enter para omitir): ") [cite: 1]

    if mongodb_uri:
        persistencia_nosql.guardar_en_mongodb(
            df_corpus, 
            mongodb_uri, 
            MONGO_DB_NAME, 
            MONGO_COLLECTION_NAME
        ) [cite: 1]
    else:
        print("Aviso: No se ingresó URI. Se omite el guardado en MongoDB.") [cite: 1]   
    
        print("\n=== PIPELINE DE EXTRACCIÓN COMPLETADO CON ÉXITO ===")
        print(f"Total de registros listos para la fase de NLP: {len(df_corpus)}")

if __name__ == "__main__":
    main()