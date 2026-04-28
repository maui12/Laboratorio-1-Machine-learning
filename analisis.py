import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from wordcloud import WordCloud

def ejecutar_analisis(df):
    vectorizer = TfidfVectorizer(max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(df["texto_limpio"])
    n_clusters = 4
    
    # Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(tfidf_matrix)
    
    # PCA (Lineal)
    pca = PCA(n_components=2, random_state=42)
    pca_res = pca.fit_transform(tfidf_matrix.toarray())
    df["pca_1"], df["pca_2"] = pca_res[:, 0], pca_res[:, 1]
    
    # t-SNE (No Lineal)
    tsne = TSNE(n_components=2, perplexity=min(30, len(df)-1), random_state=42)
    tsne_res = tsne.fit_transform(tfidf_matrix.toarray())
    df["tsne_1"], df["tsne_2"] = tsne_res[:, 0], tsne_res[:, 1]
    
    if not os.path.exists("images"): os.makedirs("images")
        
    # Grafico PCA
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x="pca_1", y="pca_2", hue="cluster", data=df, palette="viridis")
    plt.title("Visualizacion Lineal (PCA)")
    plt.savefig("images/pca_clusters.png")
    plt.close()

    # Grafico t-SNE (No Lineal)
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x="tsne_1", y="tsne_2", hue="cluster", data=df, palette="magma")
    plt.title("Visualizacion No Lineal (t-SNE)")
    plt.savefig("images/tsne_clusters.png")
    plt.close()
    
    # Nubes de palabras 
    vocabulario = vectorizer.get_feature_names_out()
    for i in range(n_clusters):
        textos_cluster = " ".join(df[df["cluster"] == i]["texto_limpio"])
        if textos_cluster.strip():
            wc = WordCloud(width=800, height=400, background_color="white").generate(textos_cluster)
            wc.to_file(f"images/nube_cluster_{i}.png")
            
    # Datos para tabla Latex
    print("\n--- COPIAR PARA LA TABLA DE LATEX ---")
    centroides = kmeans.cluster_centers_
    for i in range(n_clusters):
        indices_top = centroides[i].argsort()[-5:][::-1]
        palabras = [vocabulario[ind] for ind in indices_top]
        print(f"{i} & {', '.join(palabras)} \\\\ \\hline")
    
    return df