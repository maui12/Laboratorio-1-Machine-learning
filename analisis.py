import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def ejecutar_analisis(df):
    vectorizer = TfidfVectorizer(max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(df["texto_limpio"])
    
    n_clusters = 4 if len(df) >= 4 else max(1, len(df))
    
    # Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(tfidf_matrix)
    
    # PCA
    if tfidf_matrix.shape[0] >= 2 and tfidf_matrix.shape[1] >= 2:
        pca = PCA(n_components=2, random_state=42)
        pca_result = pca.fit_transform(tfidf_matrix.toarray())
        df["pca_1"] = pca_result[:, 0]
        df["pca_2"] = pca_result[:, 1]
    else:
        df["pca_1"] = 0
        df["pca_2"] = 0
        
    # Graficos para Latex
    if not os.path.exists("images"):
        os.makedirs("images")
        
    # 1. Grafico Scatter (PCA)
    plt.figure(figsize=(10, 8))
    style_param = "fuente" if df["fuente"].nunique() > 1 else None
    sns.scatterplot(
        x="pca_1", y="pca_2", hue="cluster", style=style_param, 
        data=df, palette="viridis", s=100
    )
    plt.title("Agrupamiento de Textos (K-Means + PCA)")
    plt.xlabel("Componente Principal 1")
    plt.ylabel("Componente Principal 2")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig("images/pca_clusters.png")
    plt.close()
    
    # 2. Grafico de Barras (Frecuencias TF-IDF)
    pesos_totales = np.asarray(tfidf_matrix.sum(axis=0)).ravel()
    vocabulario = vectorizer.get_feature_names_out()
    df_frec = pd.DataFrame({'Palabra': vocabulario, 'Peso': pesos_totales})
    df_frec = df_frec.sort_values(by='Peso', ascending=False).head(10)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Peso', y='Palabra', data=df_frec, palette='magma')
    plt.title("Top 10 Palabras Mas Relevantes del Corpus")
    plt.xlabel("Peso TF-IDF Acumulado")
    plt.ylabel("Palabra")
    plt.tight_layout()
    plt.savefig("images/grafico_frecuencias.png")
    plt.close()
    
    # Datos para tabla de Latex
    print("\n--- COPIAR PARA LA TABLA DE LATEX ---")
    centroides = kmeans.cluster_centers_
    for i in range(n_clusters):
        indices_top = centroides[i].argsort()[-5:][::-1]
        palabras = [vocabulario[ind] for ind in indices_top]
        print(f"{i} & {', '.join(palabras)} \\\\ \\hline")
    print("-------------------------------------\n")
    
    return df