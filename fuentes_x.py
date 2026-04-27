import pandas as pd
import requests
from token_x import X_BEARER_TOKEN
from configuracion import X_QUERY,X_MAX_RESULTS


def buscar_posts_x(query, bearer_token, max_results=10):
    columnas_base = ["id", "fuente", "texto", "fecha", "url", "autor", "consulta"]
    
    if not bearer_token:
        return 400, pd.DataFrame(columns=columnas_base)

    url = "https://api.x.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    params = {
        "query": query,
        "max_results": max(10, min(max_results, 100)),
        "tweet.fields": "created_at,author_id,lang",
        "expansions": "author_id",
        "user.fields": "username,name"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
    except requests.exceptions.RequestException:
        # Si no hay internet o falla la conexión
        return 500, pd.DataFrame(columns=columnas_base)

    # Si la respuesta NO es 200 (éxito), devolvemos el código de error y df vacío
    if response.status_code != 200:
        return response.status_code, pd.DataFrame(columns=columnas_base)

    data = response.json()
    posts = data.get("data", [])
    users = data.get("includes", {}).get("users", [])
    user_map = {u["id"]: u.get("username", "") for u in users}

    registros = []
    for post in posts:
        post_id = post.get("id", "")
        author_id = post.get("author_id", "")
        username = user_map.get(author_id, "")
        
        registros.append({
            "id": post_id,
            "fuente": "x",
            "texto": post.get("text", ""),
            "fecha": post.get("created_at"),
            "url": f"https://x.com/{username}/status/{post_id}" if username and post_id else None,
            "autor": username if username else author_id,
            "consulta": query
        })

    return 200, pd.DataFrame(registros)