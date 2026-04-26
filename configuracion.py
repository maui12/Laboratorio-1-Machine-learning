#Parámetros X
X_QUERY = "universidad OR educacion OR tecnologia lang:es -is:retweet"
X_MAX_RESULTS = 500

#RSS Parámetros
COOPERATIVA_RSS_URL = "https://www.cooperativa.cl/noticias/site/tax/port/all/rss_3___1.xml"
COOPERATIVA_MAX_ITEMS = 30

#Fuente Opcional
CSV_FILE_PATH = "mock_corpus.csv"

#Salidas
PARQUET_OUTPUT_NAME = "corpus_consolidado.parquet"
PICKLE_OUTPUT_NAME = "corpus_consolidado.pkl"

#configuracion MongoDB
MONGO_DB_NAME = "LaboratorioML"
MONGO_COLLECTION_NAME = "corpus_textos"