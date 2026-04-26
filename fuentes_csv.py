import pandas as pd
from datetime import datetime

def cargar_datos_csv(ruta_archivo, nombre_fuente="tiktok"):
    try:
        df_raw = pd.read_csv(ruta_archivo)
        
        # Intentar encontrar la columna de texto [cite: 17]
        columna_texto = next((c for c in ["texto", "caption", "descripcion"] if c in df_raw.columns), None)
        
        if not columna_texto:
            print(f"Aviso: No se encontró columna de texto en {ruta_archivo}")
            return pd.DataFrame()

        # Crear el formato estándar [cite: 17]
        df_salida = pd.DataFrame({
            "id": [f"{nombre_fuente}_{i}" for i in range(len(df_raw))],
            "fuente": nombre_fuente,
            "texto": df_raw[columna_texto].astype(str),
            "fecha": datetime.now().isoformat(), 
            "url": None,
            "autor": None,
            "consulta": None
        })
        return df_salida
    except Exception as e:
        print(f"Error al cargar el CSV: {e}")
        return pd.DataFrame()