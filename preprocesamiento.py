import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")
STOPWORDS_ES = set(stopwords.words("spanish"))

def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\.\S+", " ", texto) # sacamos enlaces
    texto = re.sub(r"[^\w\s]", " ", texto)          # sacamos puntuacion
    tokens = texto.split()
    tokens = [t for t in tokens if t not in STOPWORDS_ES and len(t) > 2]
    return " ".join(tokens)