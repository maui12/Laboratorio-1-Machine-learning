from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def ejecutar_analisis(df):
    vectorizer = TfidfVectorizer(max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(df["texto_limpio"])
    
    # Clustering
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(tfidf_matrix)
    
    # PCA
    pca = PCA(n_components=2, random_state=42)
    pca_result = pca.fit_transform(tfidf_matrix.toarray())
    df["pca_1"] = pca_result[:, 0]
    df["pca_2"] = pca_result[:, 1]
    
    return df