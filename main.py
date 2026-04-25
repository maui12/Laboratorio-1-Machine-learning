import fuentes_x
import fuentes_cooperativa
import consolidacion_dfs
import persistencia_binaria
from token_x import X_BEARER_TOKEN
from configuracion import X_QUERY,X_MAX_RESULTS

def main():
    print("=== INICIANDO PIPELINE DE EXTRACCIÓN DE DATOS ===")
    
    print("\n[1/4] Extrayendo datos de X...")
    df_x = fuentes_x.buscar_posts_x(
        query=X_QUERY,
        bearer_token=X_BEARER_TOKEN,
        max_results=X_MAX_RESULTS
    )
    
    print("\n[2/4] Extrayendo datos de RSS Cooperativa...")
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
    
    print("\n=== PIPELINE DE EXTRACCIÓN COMPLETADO CON ÉXITO ===")
    print(f"Total de registros listos para la fase de NLP: {len(df_corpus)}")

if __name__ == "__main__":
    main()