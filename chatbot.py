import random
from utils.text_utils import clear_text
from utils.json_utils import cargar_json, cargar_pickle

from services.intents_services import predecir_intencion, respuesta_aleatoria

from services.games_services import (
    extraer_genero,
    extraer_sistema,
    extraer_juego,
    buscar_info_juego,
    buscar_tips_por_juego
)

from services.recommendations_services import (
    buscar_juegos_por_genero,
    buscar_juegos_por_sistema,
    buscar_juegos_por_genero_y_sistema
)

from services.one_hot_recommendation_service import recomendar_juegos_similares

from services.context_services import (
    guardar_juego,
    obtener_juego,
    guardar_genero,
    guardar_sistema,
    guardar_intencion,
    limpiar_contexto
)


INTENTS_PATH = "Datasets/intents.json"
GAMES_PATH = "Datasets/games.json"
TIPS_PATH = "Datasets/tips.json"

MODEL_PATH = "models/modelo.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"


intents_data = cargar_json(INTENTS_PATH)
games_data = cargar_json(GAMES_PATH)
tips_data = cargar_json(TIPS_PATH)

modelo = cargar_pickle(MODEL_PATH)
vectorizer = cargar_pickle(VECTORIZER_PATH)

def responder_con_tag(mensaje):
    tag = detectar_tag(mensaje)
    respuesta = responder(mensaje)
    return respouesta, tag

def detectar_tag(mensaje):
    mensaje_limpio = clear_text(mensaje)

    palabras_despedida = [
    "adios","adiós","hasta luego","nos vemos","bye","salir","me voy"
    ]

    palabras_random = [
    "cualquier genero", "un juego", "cualquier juego", "cualquier sistema", "cualquier género","cualquiera","algo random","algo aleatorio","lo que sea","de cualquier tipo"
    ]

    palabras_similitud = [
        "jugue","jugué","parecido","parecidos", "similar", "similares", "como", "otro", "otros"
    ]

    palabras_recomendacion = [
        "recomienda","recomiendame","recomiéndame","recomendacion","recomendación","juego","juegos","algo para","que puedo jugar"
    ]

    palabras_sistemas = [
        "xbox","pc","computadora","playstation","ps4","ps5","switch","nintendo","android","ios","iphone"
    ]

    palabras_plataforma = [
        "sistema","sistemas","consola","consolas","dispositivo","dispositivos"
    ]


    nombre_juego = extraer_juego(mensaje, games_data)
    sistema = extraer_sistema(mensaje)

    if nombre_juego and any(p in mensaje_limpio for p in palabras_similitud):
        return "juegos_similares"
    
    if any(p in mensaje_limpio for p in palabras_despedida):
        return "despedida"

    if any(p in mensaje_limpio for p in palabras_plataforma):
        return "plataforma"

    if any(p in mensaje_limpio for p in palabras_random):
        return "recomendacion_random"

    if any(p in mensaje_limpio for p in palabras_recomendacion):
        return "recomendacion_genero"

    if any(p in mensaje_limpio for p in palabras_sistemas):
        return "recomendacion_genero"
    

    return predecir_intencion(mensaje, modelo, vectorizer)


def responder(mensaje):
    mensaje_limpio = clear_text(mensaje)

    tag = detectar_tag(mensaje)
    guardar_intencion(tag)

    nombre_juego_detectado = extraer_juego(mensaje, games_data)
    sistema_detectado = extraer_sistema(mensaje)

    if nombre_juego_detectado:
        guardar_juego(nombre_juego_detectado)

    if sistema_detectado:
        guardar_sistema(sistema_detectado)

    if tag == "Saludo":
        return respuesta_aleatoria(tag, intents_data)

    elif tag == "juegos_similares":
        nombre_juego = extraer_juego(mensaje, games_data)

        if not nombre_juego:
            nombre_juego = obtener_juego()

        if not nombre_juego:
            return "Dime qué juego jugaste para recomendarte algo parecido."

        recomendaciones = recomendar_juegos_similares(
            nombre_juego,
            games_data,
            sistema=sistema_detectado,
            top_n=5
        )

        if recomendaciones:
            nombres = [j["juego"] for j in recomendaciones]
            guardar_juego(nombres[0])
            return f"Si jugaste {nombre_juego}, te recomiendo: " + ", ".join(nombres)

        if sistema_detectado:
            return f"No encontré juegos similares a {nombre_juego} para {sistema_detectado}."

        return f"No encontré juegos similares a {nombre_juego}."

    elif tag == "recomendacion_random":
        cantidad = min(5, len(games_data))
        juegos = random.sample(games_data, cantidad)

        nombres = [j["juego"] for j in juegos]

        guardar_juego(juegos[0]["juego"])

        return "Te recomiendo estos juegos: " + ", ".join(nombres)

    elif tag == "recomendacion_genero":
        genero = extraer_genero(mensaje)
        sistema = extraer_sistema(mensaje)

        if genero:
            guardar_genero(genero)

        if sistema:
            guardar_sistema(sistema)

        if genero and sistema:
            juegos = buscar_juegos_por_genero_y_sistema(genero, sistema, games_data)
        elif genero:
            juegos = buscar_juegos_por_genero(genero, games_data)
        elif sistema:
            juegos = buscar_juegos_por_sistema(sistema, games_data)
        else:
            return "Dime qué género o sistema te interesa para recomendarte un juego."

        if juegos:
            nombres = [j["juego"] for j in juegos]
            guardar_juego(juegos[0]["juego"])
            return "Te recomiendo estos juegos: " + ", ".join(nombres)

        return "No encontré juegos con esas características."

    elif tag == "info_juego":
        nombre_juego = extraer_juego(mensaje, games_data)

        if not nombre_juego:
            nombre_juego = obtener_juego()

        if not nombre_juego:
            return "Dime el nombre del juego sobre el que quieres información."

        juego = buscar_info_juego(nombre_juego, games_data)

        if juego:
            guardar_juego(juego["juego"])
            return f"{juego['juego']}: {juego['descripcion']}"

        return "No encontré información sobre ese juego."

    elif tag == "plataforma":
        nombre_juego = extraer_juego(mensaje, games_data)

        if not nombre_juego:
            nombre_juego = obtener_juego()

        if not nombre_juego:
            return "Dime el nombre del juego del que quieres saber los sistemas disponibles."

        juego = buscar_info_juego(nombre_juego, games_data)

        if juego:
            guardar_juego(juego["juego"])
            sistemas = ", ".join(juego["sistemas"])
            return f"{juego['juego']} está disponible en: {sistemas}"

        return "No encontré ese juego en la base de datos."

    elif tag in ["trucos", "ayuda_nivel"]:
        nombre_juego = extraer_juego(mensaje, games_data)

        if not nombre_juego:
            nombre_juego = obtener_juego()

        if not nombre_juego:
            return "Dime el nombre del juego para darte tips o ayuda."

        tips = buscar_tips_por_juego(nombre_juego, tips_data)

        if tips:
            guardar_juego(nombre_juego)
            lista_tips = [f"- {t['tip']}" for t in tips[:3]]
            return f"Aquí tienes algunos tips para {nombre_juego}:\n" + "\n".join(lista_tips)

        return "No encontré tips para ese juego."

    elif tag == "despedida":
        limpiar_contexto()
        return respuesta_aleatoria(tag, intents_data)

    else:
        return respuesta_aleatoria("fallback", intents_data)
        
if __name__ == "__main__":
    iniciar_chat()