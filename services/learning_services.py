from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion

from utils.text_utils import clear_text


def crear_vectorizer():
    return FeatureUnion(
        [
            (
                "palabras",
                TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True),
            ),
            (
                "caracteres",
                TfidfVectorizer(
                    analyzer="char_wb",
                    ngram_range=(2, 5),
                    sublinear_tf=True,
                ),
            ),
        ]
    )


def crear_clasificador():
    return LogisticRegression(
        class_weight="balanced",
        max_iter=1500,
        random_state=42,
    )


def preparar_datos(data, ejemplos_confirmados=()):
    etiquetas_validas = {intent["tag"] for intent in data["intents"]}
    ejemplos = {}

    for intent in data["intents"]:
        tag = intent["tag"]
        for pattern in intent["patterns"]:
            texto = clear_text(pattern)
            if not texto:
                continue
            etiqueta_previa = ejemplos.get(texto)
            if etiqueta_previa is not None and etiqueta_previa != tag:
                raise ValueError(
                    f"El ejemplo normalizado {texto!r} aparece con etiquetas "
                    f"incompatibles: {etiqueta_previa!r} y {tag!r}."
                )
            ejemplos[texto] = tag

    for ejemplo in ejemplos_confirmados:
        texto = clear_text(ejemplo["question"])
        tag = ejemplo["intent"]
        if not texto:
            continue
        if tag not in etiquetas_validas:
            raise ValueError(f"Etiqueta de entrenamiento desconocida: {tag!r}.")
        ejemplos[texto] = tag

    textos = list(ejemplos)
    etiquetas = [ejemplos[texto] for texto in textos]
    if len(set(etiquetas)) < 2:
        raise ValueError("Se necesitan al menos dos intenciones para entrenar.")

    return textos, etiquetas


def entrenar_modelo(textos, etiquetas):
    vectorizer = crear_vectorizer()
    X = vectorizer.fit_transform(textos)
    modelo = crear_clasificador()
    modelo.fit(X, etiquetas)
    return modelo, vectorizer


def resumen_clases(etiquetas):
    return dict(sorted(Counter(etiquetas).items()))
