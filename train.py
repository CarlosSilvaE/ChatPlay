import json
import os
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from utils import clear_text

INTENTS_PATH = "Datasets/intents.json"
MODELS_DIR = "models"
MODELS_PATH = os.path.join(MODELS_DIR, "modelo.pkl")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "vectorizer.pkl")

def cargar_intenciones(ruta_json):
    with open(ruta_json, "r", encoding="utf-8") as archivo:
        data = json.load(archivo)
    return data


def preparar_datos(data):
    textos = []
    etiquetas = []

    for intent in data["intents"]:
        tag = intent["tag"]

        for pattern in intent["patterns"]:
            texto_limpio = clear_text(pattern)
            textos.append(texto_limpio)
            etiquetas.append(tag)

    return textos, etiquetas


def entrenar_modelo():
    data = cargar_intenciones(INTENTS_PATH)
    textos, etiquetas = preparar_datos(data)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(textos)

    modelo = LogisticRegression(max_iter=1000)
    modelo.fit(X, etiquetas)

    os.makedirs(MODELS_DIR, exist_ok=True)

    with open(VECTORIZER_PATH, "wb") as archivo_vectorizer:
        pickle.dump(vectorizer, archivo_vectorizer)

    with open(MODELS_PATH, "wb") as archivo_modelo:
        pickle.dump(modelo, archivo_modelo)

    print("Modelo entrenado correctamente.")
    print(f"Modelo guardado en: {MODELS_PATH}")
    print(f"Vectorizador guardado en: {VECTORIZER_PATH}")


if __name__ == "__main__":
    entrenar_modelo()