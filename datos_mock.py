import pandas as pd


# no se si los post que no son de twitter siguen la misma estructura  ?
# id,fuente,texto,fecha,url,autor,consulta,texto_limpio
mock_data = [
    {"id": 1, "fuente": "X", "texto": "Probando la nueva API para el proyecto de Data Science. Deséenme suerte 💻📊", "fecha": "2026-04-14T09:15:00Z", "url": "https://x.com/dev1/status/1", "autor": "@coder_py", "consulta": "Data Science", "texto_limpio": "probando nueva api proyecto data science deseenme suerte"},
    {"id": 2, "fuente": "RSS", "texto": "El observatorio Vera C. Rubin anuncia avances en el uso de Machine Learning para el análisis de datos.", "fecha": "2026-04-14T10:00:00Z", "url": "https://latercera.com/noticia/2", "autor": "La Tercera", "consulta": "Machine Learning", "texto_limpio": "observatorio vera c rubin anuncia avances uso machine learning analisis datos"},
    {"id": 3, "fuente": "X", "texto": "¿Alguien más peleando con K-Means y la reducción con PCA? 😭 Necesito café.", "fecha": "2026-04-13T22:30:00Z", "url": "https://x.com/student/status/3", "autor": "@data_student", "consulta": "K-Means", "texto_limpio": "alguien mas peleando k-means reduccion pca necesito cafe"},
    {"id": 4, "fuente": "RSS", "texto": "Radiografía al uso de bases de datos NoSQL en aplicaciones web modernas en Chile.", "fecha": "2026-04-13T14:20:00Z", "url": "https://cooperativa.cl/tec/4", "autor": "Cooperativa", "consulta": "NoSQL", "texto_limpio": "radiografia uso bases datos nosql aplicaciones web modernas chile"},
    {"id": 5, "fuente": "X", "texto": "Hoy el clima en La Serena está perfecto para quedarse programando todo el día. ☁️", "fecha": "2026-04-14T08:05:00Z", "url": "https://x.com/local_dev/status/5", "autor": "@local_dev", "consulta": "La Serena", "texto_limpio": "hoy clima serena perfecto quedarse programando dia"},
    {"id": 6, "fuente": "RSS", "texto": "Expertos en ciberseguridad advierten sobre nuevas técnicas de ataque en redes sociales.", "fecha": "2026-04-12T11:45:00Z", "url": "https://latercera.com/noticia/6", "autor": "La Tercera", "consulta": "ciberseguridad", "texto_limpio": "expertos ciberseguridad advierten nuevas tecnicas ataque redes sociales"},
    {"id": 7, "fuente": "X", "texto": "Logré conectar MongoDB con Python sin que explote todo. Un gran paso.", "fecha": "2026-04-13T19:10:00Z", "url": "https://x.com/dev2/status/7", "autor": "@backend_ninja", "consulta": "MongoDB", "texto_limpio": "logre conectar mongodb python explote gran paso"},
    {"id": 8, "fuente": "X", "texto": "Entrenando el modelo TF-IDF con un corpus de noticias chilenas. Resultados preliminares interesantes.", "fecha": "2026-04-14T11:00:00Z", "url": "https://x.com/ml_guy/status/8", "autor": "@ml_guy", "consulta": "TF-IDF", "texto_limpio": "entrenando modelo tf-idf corpus noticias chilenas resultados preliminares interesantes"},
    {"id": 9, "fuente": "RSS", "texto": "Estudio revela que el uso de Python y Pandas lidera las preferencias de los desarrolladores.", "fecha": "2026-04-13T09:30:00Z", "url": "https://cooperativa.cl/tec/9", "autor": "Cooperativa", "consulta": "Python Pandas", "texto_limpio": "estudio revela uso python pandas lidera preferencias desarrolladores"},
    {"id": 10, "fuente": "X", "texto": "Listos los gráficos de dispersión de los clústers. Se ven hermosos los colores 📈", "fecha": "2026-04-14T12:20:00Z", "url": "https://x.com/viz_master/status/10", "autor": "@viz_master", "consulta": "Clustering", "texto_limpio": "listos graficos dispersion clusters ven hermosos colores"}
]

# Crear el DataFrame
df_mock = pd.DataFrame(mock_data)

# Exportar a CSV simulando el archivo que entregará el Integrante 1
df_mock.to_csv("mock_corpus.csv", index=False, encoding="utf-8")

print("Archivo 'mock_corpus.csv' generado con éxito. Listo para Ingeniería de Datos y Machine Learning.")