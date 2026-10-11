import random

from utils.text_utils import clear_text


def predecir_intencion(mensaje, modelo, vectorizer, umbral_confianza=0.12):
    mensaje_limpio = clear_text(mensaje)
    vector = vectorizer.transform([mensaje_limpio])
    if vector.nnz == 0:
        return "fallback", 0.0

    word_vectorizer = next(
        (
            transformer
            for name, transformer in getattr(vectorizer, "transformer_list", [])
            if name == "palabras"
        ),
        None,
    )
    if word_vectorizer is not None:
        word_vector = word_vectorizer.transform([mensaje_limpio])
        if word_vector.nnz == 0:
            return "fallback", 0.0

    probabilidades = modelo.predict_proba(vector)[0]
    indice = probabilidades.argmax()
    confianza = float(probabilidades[indice])
    prediccion = modelo.classes_[indice]

    if confianza < umbral_confianza:
        return "fallback", confianza

    return prediccion, confianza


def obtener_respuestas_por_tag(tag, intents_data):
    for intent in intents_data["intents"]:
        if intent["tag"] == tag:
            return intent.get("responses", [])
    return []


def respuesta_aleatoria(tag, intents_data):
    respuestas = obtener_respuestas_por_tag(tag, intents_data)

    if respuestas:
        return random.choice(respuestas)

    return "No tengo una respuesta para eso."
