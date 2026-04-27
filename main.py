from getpass import getpass
import pandas as pd
import os

import fuentes_x
import fuentes_cooperativa
import consolidacion_dfs
import persistencia_binaria
import persistencia_nosql

from configuracion import (
    X_QUERY,X_MAX_RESULTS,CSV_FILE_PATH,
    MONGO_DB_NAME,MONGO_COLLECTION_NAME
)


def main():
    print("=== INICIANDO PIPELINE DE EXTRACCIÓN DE DATOS ===")
    
    print("\n[1/7] Extracción de X:")
    token_ingresado = getpass("Ingresa tu Bearer Token de X (o presiona Enter para usar respaldo local): ")
    
    columnas_vacias = ["id", "fuente", "texto", "fecha", "url", "autor", "consulta"]

    # 2. Lógica de validación
    if token_ingresado.strip() != "":
        print("-> Evaluando token y consultando API...")
        
        estado, df_x = fuentes_x.buscar_posts_x(
            query=X_QUERY,
            bearer_token=token_ingresado.strip(),
            max_results=X_MAX_RESULTS
        )
        
        if estado == 200:
            print("-> ¡Token válido y con créditos! Datos extraídos con éxito.")
            if not df_x.empty:
                df_x.to_parquet("respaldo_x_crudo.parquet", index=False)
                print("-> Respaldo local ('respaldo_x_crudo.parquet') actualizado.")
                
        # === AQUI ESTÁ EL CAMBIO: Agrupamos 401, 403 y 429 ===
        elif estado in [401, 403, 429]:
            if estado == 401:
                print("-> ERROR: El token introducido NO es válido (Error 401).")
            else:
                print("-> AVISO: Token válido, pero NO tienes créditos o alcanzaste el límite (Error 403/429).")
            
            print("-> Intentando cargar datos desde respaldo Parquet...")
            try:
                df_x = pd.read_parquet("respaldo_x_crudo.parquet")
                print(f"-> Cargados {len(df_x)} registros de X desde el archivo local.")
            except FileNotFoundError:
                print("-> AVISO: No se encontró el archivo Parquet. Se usará un DataFrame vacío.")
                df_x = pd.DataFrame(columns=columnas_vacias)
        # =======================================================
                
        else:
            print(f"-> Error inesperado de la API (Código {estado}). Siguiendo con DataFrame vacío.")
            df_x = pd.DataFrame(columns=columnas_vacias)
            
    else:
        print("-> No se ingresó token. Intentando cargar datos desde respaldo Parquet...")
        try:
            df_x = pd.read_parquet("respaldo_x_crudo.parquet")
            print(f"-> Cargados {len(df_x)} registros de X desde el archivo local.")
        except FileNotFoundError:
            print("-> AVISO: No se encontró el archivo Parquet. Se usará un DataFrame vacío.")
            df_x = pd.DataFrame(columns=columnas_vacias)


    print("\n[2/7] Extrayendo datos de RSS Cooperativa...")
    df_rss = fuentes_cooperativa.extraer_rss_cooperativa()
    
    #por si ponemos tiktok
    df_csv = None 
    
    print("\n[3/4] Consolidando el corpus de datos...")
    df_corpus = consolidacion_dfs.generar_consolidado(df_x, df_rss, df_csv)
    
    if df_corpus.empty:
        print("Error crítico: El corpus está vacío. Se aborta la ejecución.")
        return
        
    print("\n[4/4] Guardando respaldos binarios... (Parquet)")
    persistencia_binaria.guardar_corpus(df_corpus)

    print("\n[6/7] Ejecutando limpieza y análisis (TF-IDF, Clusters, PCA)...")
  
    df_corpus["texto_limpio"] = df_corpus["texto"].apply(preprocesamiento.limpiar_texto)
    #ejecutar modelos de ML
    df_corpus = analisis.ejecutar_analisis(df_corpus)
 
    print("\n[7/7] Sincronizando con MongoDB...")

    mongodb_uri = getpass("Ingresa tu URI de MongoDB (o presiona Enter para omitir): ") #[cite: 1]

    if mongodb_uri:
        persistencia_nosql.guardar_en_mongodb(
            df_corpus, 
            mongodb_uri, 
            MONGO_DB_NAME, 
            MONGO_COLLECTION_NAME
        ) #[cite: 1]
    else:
        print("Aviso: No se ingresó URI. Se omite el guardado en MongoDB.") #[cite: 1]   
    
        print("\n=== PIPELINE DE EXTRACCIÓN COMPLETADO CON ÉXITO ===")
        print(df_corpus.head())

if __name__ == "__main__":
    main()