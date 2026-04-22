import pandas as pd
import requests
from token_x import X_BEARER_TOKEN
from configuracion import X_QUERY,X_MAX_RESULTS


def buscar_posts_x(query, bearer_token, max_results=10):
    """
    Busca publicaciones recientes en X y devuelve un DataFrame.

    Parámetros:
    - query: texto de búsqueda en sintaxis de X.
    - bearer_token: token Bearer para autenticación.
    - max_results: cantidad de publicaciones a recuperar.

    Retorna:
    - DataFrame con columnas estandarizadas para el laboratorio.
    """
    if not bearer_token:
        print("No se ingresó Bearer Token. Se devolverá un DataFrame vacío.")
        return pd.DataFrame(columns=["id", "fuente", "texto", "fecha", "url", "autor", "consulta"])

    url = "https://api.x.com/2/tweets/search/recent"

    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    params = {
        "query": query,
        "max_results": max(10, min(max_results, 100)),
        "tweet.fields": "created_at,author_id,lang",
        "expansions": "author_id",
        "user.fields": "username,name"
    }

    response = requests.get(url, headers=headers, params=params, timeout=30)

    if response.status_code != 200:
        print("Error al consultar X:")
        print("Código:", response.status_code)
        print("Detalle:", response.text[:1000])
        return pd.DataFrame(columns=["id", "fuente", "texto", "fecha", "url", "autor", "consulta"])

    data = response.json()
    posts = data.get("data", [])
    users = data.get("includes", {}).get("users", [])

    # Mapa author_id -> username
    user_map = {u["id"]: u.get("username", "") for u in users}

    registros = []
    for post in posts:
        post_id = post.get("id", "")
        author_id = post.get("author_id", "")
        username = user_map.get(author_id, "")
        texto = post.get("text", "")

        registros.append({
            "id": post_id,
            "fuente": "x",
            "texto": texto,
            "fecha": post.get("created_at"),
            "url": f"https://x.com/{username}/status/{post_id}" if username and post_id else None,
            "autor": username if username else author_id,
            "consulta": query
        })

    return pd.DataFrame(registros)


#ejemplo
df_x = buscar_posts_x(
    query=X_QUERY,
    bearer_token=X_BEARER_TOKEN,
    max_results=X_MAX_RESULTS
)

print("Cantidad de publicaciones recuperadas desde X:", len(df_x))
df_x.head()


df_x.head(100)

#df_x.to_parquet("df_x.parquet", index=False)