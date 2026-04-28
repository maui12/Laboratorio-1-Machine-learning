import pandas as pd
import feedparser
from configuracion import COOPERATIVA_RSS_URL, COOPERATIVA_MAX_ITEMS


def extraer_rss_cooperativa():
    """
    Lee el feed RSS de Cooperativa y devuelve un DataFrame con la estructura homogénea del corpus.
    """
    
    
    try:
        feed = feedparser.parse(COOPERATIVA_RSS_URL)
    except Exception as e:
        print(f"Error al conectar con el RSS: {e}")
       
        return pd.DataFrame(columns=["id", "fuente", "texto", "fecha", "url", "autor", "consulta"])

    registros = []
    
    for entry in feed.entries[:COOPERATIVA_MAX_ITEMS]:
        
        titulo = entry.get("title", "")
        resumen = entry.get("summary", "")
        
        texto_completo = f"{titulo} - {resumen}".strip()
        if texto_completo == "-":
            texto_completo = "Sin texto"
            
        registros.append({
            "id": entry.get("id", entry.get("link", "")),
            "fuente": "cooperativa",
            "texto": texto_completo,
            "fecha": entry.get("published", ""),
            "url": entry.get("link", ""),
            "autor": entry.get("author", "Radio Cooperativa"),
            "consulta": "RSS Portada" 
        })

    df_rss = pd.DataFrame(registros)
    
    # Verificación de seguridad
    if df_rss.empty:
        print("Advertencia: No se encontraron noticias en el RSS.")
        return pd.DataFrame(columns=["id", "fuente", "texto", "fecha", "url", "autor", "consulta"])
        
    return df_rss
