import pandas as pd
import requests
import time

def buscar_posts_x(query, bearer_token, max_results=800):
    columnas_base = ["id", "fuente", "texto", "fecha", "url", "autor", "consulta"]
    
    if not bearer_token:
        return 400, pd.DataFrame(columns=columnas_base)

    url = "https://api.x.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    registros = []
    next_token = None
    
    print(f"-> Iniciando descarga definitiva. Meta: {max_results} posts...")

    while len(registros) < max_results:
        faltantes = max_results - len(registros)
        cantidad_peticion = max(10, min(faltantes, 100))
        
        params = {
            "query": query,
            "max_results": cantidad_peticion,
            "tweet.fields": "created_at,author_id,lang",
            "expansions": "author_id",
            "user.fields": "username,name"
        }
        
        if next_token:
            params["next_token"] = next_token

        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
        except requests.exceptions.RequestException:
            return 500, pd.DataFrame(columns=columnas_base)

        if response.status_code != 200:
            if len(registros) > 0:
                print(f"-> AVISO: La API se detuvo por error {response.status_code}. Devolviendo {len(registros)} posts recolectados.")
                return 200, pd.DataFrame(registros)
            return response.status_code, pd.DataFrame(columns=columnas_base)

        data = response.json()
        posts = data.get("data", [])
        users = data.get("includes", {}).get("users", [])
        user_map = {u["id"]: u.get("username", "") for u in users}

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
            
        print(f"   ... Descargados {len(registros)} de {max_results}")

        meta = data.get("meta", {})
        next_token = meta.get("next_token")
        
        if not next_token:
            print("   ... No hay más resultados recientes en X para esta consulta.")
            break
            
        time.sleep(1.5)

    return 200, pd.DataFrame(registros)