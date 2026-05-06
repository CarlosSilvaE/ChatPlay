import json
import pickle
import random

from utils import clear_text


INTENTS_PATH = "Datasets/intents.json"
GAMES_PATH = "Datasets/games.json"
TIPS_PATH = "Datasets/tips.json"

MODEL_PATH = "models/modelo.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"


def cargar_json(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def cargar_pickle(ruta):
    with open(ruta, "rb") as archivo:
        return pickle.load(archivo)


intents_data = cargar_json(INTENTS_PATH)
games_data = cargar_json(GAMES_PATH)
tips_data = cargar_json(TIPS_PATH)

modelo = cargar_pickle(MODEL_PATH)
vectorizer = cargar_pickle(VECTORIZER_PATH)


def predecir_intencion(mensaje):
    mensaje_limpio = clear_text(mensaje)
    vector = vectorizer.transform([mensaje_limpio])
    prediccion = modelo.predict(vector)[0]
    return prediccion


def obtener_respuestas_por_tag(tag):
    for intent in intents_data["intents"]:
        if intent["tag"] == tag:
            return intent.get("responses", [])
    return []


def respuesta_aleatoria(tag):
    respuestas = obtener_respuestas_por_tag(tag)
    if respuestas:
        return random.choice(respuestas)
    return "No tengo una respuesta para eso."


def extraer_genero(mensaje):
    generos = ["terror", "aventura", "supervivencia", "plataformas", "accion", "carreras", "simulacion"]
    mensaje_limpio = clear_text(mensaje)

    for genero in generos:
        if genero in mensaje_limpio:
            return genero

    return None


def extraer_plataforma(mensaje):
    plataformas = {
        "pc": "PC",
        "xbox": "Xbox",
        "playstation": "PlayStation",
        "ps4": "PlayStation 4",
        "ps5": "PlayStation 5",
        "switch": "Nintendo Switch",
        "android": "Android",
        "ios": "iOS"
    }

    mensaje_limpio = clear_text(mensaje)

    for clave, valor in plataformas.items():
        if clave in mensaje_limpio:
            return valor

    return None


def extraer_juego(mensaje):
    mensaje_limpio = clear_text(mensaje)

    for juego in games_data:
        nombre_juego = clear_text(juego["juego"])
        if nombre_juego in mensaje_limpio:
            return juego["juego"]

    return None


def buscar_juegos_por_genero(genero):
    resultados = []

    for juego in games_data:
        if clear_text(juego["genero"]) == clear_text(genero):
            resultados.append(juego)

    return resultados


def buscar_juegos_por_plataforma(plataforma):
    resultados = []

    for juego in games_data:
        for p in juego["plataformas"]:
            if clear_text(plataforma) in clear_text(p):
                resultados.append(juego)
                break

    return resultados


def buscar_juegos_por_genero_y_plataforma(genero, plataforma):
    resultados = []

    for juego in games_data:
        coincide_genero = clear_text(juego["genero"]) == clear_text(genero)
        coincide_plataforma = any(
            clear_text(plataforma) in clear_text(p)
            for p in juego["plataformas"]
        )

        if coincide_genero and coincide_plataforma:
            resultados.append(juego)

    return resultados


def buscar_info_juego(nombre_juego):
    for juego in games_data:
        if clear_text(juego["juego"]) == clear_text(nombre_juego):
            return juego
    return None


def buscar_tips_por_juego(nombre_juego):
    resultados = []

    for tip in tips_data:
        if clear_text(tip["juego"]) == clear_text(nombre_juego):
            resultados.append(tip)

    return resultados


def responder(mensaje):
    tag = predecir_intencion(mensaje)

    if tag == "Saludo":
        return respuesta_aleatoria(tag)

    elif tag == "recomendacion_genero":
        genero = extraer_genero(mensaje)
        plataforma = extraer_plataforma(mensaje)

        if genero and plataforma:
            juegos = buscar_juegos_por_genero_y_plataforma(genero, plataforma)
        elif genero:
            juegos = buscar_juegos_por_genero(genero)
        elif plataforma:
            juegos = buscar_juegos_por_plataforma(plataforma)
        else:
            return "Dime qué género o plataforma te interesa para recomendarte un juego."

        if juegos:
            nombres = [j["juego"] for j in juegos]
            return "Te recomiendo estos juegos: " + ", ".join(nombres)
        else:
            return "No encontré juegos con esas características."

    elif tag == "info_juego":
        nombre_juego = extraer_juego(mensaje)

        if not nombre_juego:
            return "Dime el nombre del juego sobre el que quieres información."

        juego = buscar_info_juego(nombre_juego)

        if juego:
            return f"{juego['juego']}: {juego['descripcion']}"
        else:
            return "No encontré información sobre ese juego."

    elif tag == "plataforma":
        nombre_juego = extraer_juego(mensaje)

        if not nombre_juego:
            return "Dime el nombre del juego del que quieres saber las plataformas."

        juego = buscar_info_juego(nombre_juego)

        if juego:
            plataformas = ", ".join(juego["plataformas"])
            return f"{juego['juego']} está disponible en: {plataformas}"
        else:
            return "No encontré ese juego en la base de datos."

    elif tag in ["trucos", "ayuda_nivel"]:
        nombre_juego = extraer_juego(mensaje)

        if not nombre_juego:
            return "Dime el nombre del juego para darte tips o ayuda."

        tips = buscar_tips_por_juego(nombre_juego)

        if tips:
            lista_tips = [f"- {t['tip']}" for t in tips[:3]]
            return f"Aquí tienes algunos tips para {nombre_juego}:\n" + "\n".join(lista_tips)
        else:
            return "No encontré tips para ese juego."

    elif tag == "despedida":
        return respuesta_aleatoria(tag)

    else:
        return respuesta_aleatoria("fallback")


def iniciar_chat():
    print("ChatPlay 🎮 iniciado. Escribe 'salir' para terminar.")

    while True:
        mensaje = input("Tú: ")

        if clear_text(mensaje) == "salir":
            print("ChatPlay: ¡Hasta luego!")
            break

        respuesta = responder(mensaje)
        print("ChatPlay:", respuesta)


if __name__ == "__main__":
    iniciar_chat()