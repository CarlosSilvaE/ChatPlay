import random
from utils.text_utils import clear_text

def predecir_intencion(mensaje, modelo, vectorizer):
    mensaje_limpio = clear_text(mensaje)
    vector = vectorizer.transform([mensaje_limpio])
    prediccion = modelo.predict(vector)[0]
    return prediccion


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