import json
from pathlib import Path

from services.cache_services import (
    DATABASE_PATH,
    guardar_ejemplo_confirmado,
    guardar_respuesta_cache,
    inicializar_cache,
    obtener_ejemplos_confirmados,
    obtener_respuesta_cacheada,
)
from services.context_services import (
    guardar_genero,
    guardar_intencion,
    guardar_juego,
    guardar_sistema,
    limpiar_contexto,
    obtener_juego,
)
from services.games_services import (
    buscar_info_juego,
    buscar_tips_por_juego,
    extraer_genero,
    extraer_juego,
    extraer_sistema,
)
from services.intents_services import predecir_intencion, respuesta_aleatoria
from services.learning_services import entrenar_modelo, preparar_datos
from services.recommendations_services import (
    buscar_juegos_por_genero,
    buscar_juegos_por_genero_y_sistema,
    buscar_juegos_por_sistema,
)
from utils.text_utils import clear_text


PROJECT_ROOT = Path(__file__).resolve().parent
INTENTS_PATH = PROJECT_ROOT / "Datasets" / "intents.json"
GAMES_PATH = PROJECT_ROOT / "Datasets" / "games.json"
TIPS_PATH = PROJECT_ROOT / "Datasets" / "tips.json"


def cargar_json(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def _entrenar_modelo_actual():
    textos, etiquetas = preparar_datos(
        intents_data,
        obtener_ejemplos_confirmados(DATABASE_PATH),
    )
    return entrenar_modelo(textos, etiquetas)


intents_data = cargar_json(INTENTS_PATH)
games_data = cargar_json(GAMES_PATH)
tips_data = cargar_json(TIPS_PATH)
inicializar_cache(DATABASE_PATH)
modelo, vectorizer = _entrenar_modelo_actual()


def _generar_respuesta(tag, mensaje):
    nombre_juego_detectado = extraer_juego(mensaje, games_data)
    if nombre_juego_detectado:
        guardar_juego(nombre_juego_detectado)

    if tag == "Saludo":
        return respuesta_aleatoria(tag, intents_data)

    if tag == "agradecimiento":
        return respuesta_aleatoria(tag, intents_data)

    if tag == "recomendacion_genero":
        genero = extraer_genero(mensaje)
        sistema = extraer_sistema(mensaje)

        if genero:
            guardar_genero(genero)
        if sistema:
            guardar_sistema(sistema)

        if genero and sistema:
            juegos = buscar_juegos_por_genero_y_sistema(
                genero,
                sistema,
                games_data,
            )
        elif genero:
            juegos = buscar_juegos_por_genero(genero, games_data)
        elif sistema:
            juegos = buscar_juegos_por_sistema(sistema, games_data)
        else:
            return "Dime qué género o sistema te interesa para recomendarte un juego."

        if juegos:
            nombres = [juego["juego"] for juego in juegos]
            guardar_juego(juegos[0]["juego"])
            return "Te recomiendo estos juegos: " + ", ".join(nombres)
        return "No encontré juegos con esas características."

    if tag == "info_juego":
        nombre_juego = extraer_juego(mensaje, games_data) or obtener_juego()
        if not nombre_juego:
            return "Dime el nombre del juego sobre el que quieres información."

        juego = buscar_info_juego(nombre_juego, games_data)
        if juego:
            return f"{juego['juego']}: {juego['descripcion']}"
        return "No encontré información sobre ese juego."

    if tag == "sistema":
        nombre_juego = extraer_juego(mensaje, games_data) or obtener_juego()
        if not nombre_juego:
            return "Dime el nombre del juego del que quieres saber los sistemas disponibles."

        juego = buscar_info_juego(nombre_juego, games_data)
        if juego:
            sistemas = ", ".join(juego["sistemas"])
            return f"{juego['juego']} está disponible en: {sistemas}"
        return "No encontré ese juego en la base de datos."

    if tag in ("trucos", "ayuda_nivel"):
        nombre_juego = extraer_juego(mensaje, games_data) or obtener_juego()
        if not nombre_juego:
            return "Dime el nombre del juego para darte tips o ayuda."

        tips = buscar_tips_por_juego(nombre_juego, tips_data)
        if tips:
            lista_tips = [f"- {tip['tip']}" for tip in tips[:3]]
            return (
                f"Aquí tienes algunos tips para {nombre_juego}:\n"
                + "\n".join(lista_tips)
            )
        return "No encontré tips para ese juego."

    if tag == "despedida":
        return respuesta_aleatoria(tag, intents_data)

    return respuesta_aleatoria("fallback", intents_data)


def responder(mensaje):
    if not clear_text(mensaje):
        return "Escribe una pregunta para poder ayudarte."

    respuesta_cacheada = obtener_respuesta_cacheada(mensaje, DATABASE_PATH)
    if respuesta_cacheada:
        respuesta, tag = respuesta_cacheada
        guardar_intencion(tag)
        return respuesta

    tag, _ = predecir_intencion(mensaje, modelo, vectorizer)
    guardar_intencion(tag)
    respuesta = _generar_respuesta(tag, mensaje)
    guardar_respuesta_cache(mensaje, respuesta, tag, DATABASE_PATH)
    return respuesta


def etiquetar_ultima_pregunta(pregunta, tag):
    tags_validos = {intent["tag"] for intent in intents_data["intents"]}
    if tag not in tags_validos:
        return False

    guardar_ejemplo_confirmado(pregunta, tag, DATABASE_PATH)
    global modelo, vectorizer
    modelo, vectorizer = _entrenar_modelo_actual()
    return True


def iniciar_chat():
    print("ChatPlay iniciado. Escribe '/salir' para terminar.")
    print("Comandos: /intenciones, /etiquetar <intención>, /salir")
    ultima_pregunta = None
    tags_validos = [intent["tag"] for intent in intents_data["intents"]]

    while True:
        mensaje = input("Tú: ").strip()

        if clear_text(mensaje) in ("/salir", "salir"):
            limpiar_contexto()
            print("ChatPlay: ¡Hasta luego!")
            break

        if mensaje.lower() == "/intenciones":
            print("Intenciones:", ", ".join(tags_validos))
            continue

        if mensaje.lower().startswith("/etiquetar"):
            partes = mensaje.split(maxsplit=1)
            if len(partes) != 2 or not ultima_pregunta:
                print("ChatPlay: Primero escribe una pregunta y luego /etiquetar <intención>.")
                continue

            tag = partes[1].strip()
            if etiquetar_ultima_pregunta(ultima_pregunta, tag):
                print(
                    f"ChatPlay: Etiqueta '{tag}' guardada; el modelo se volvió "
                    "a entrenar con este ejemplo confirmado."
                )
            else:
                print("ChatPlay: Intención no válida. Opciones:", ", ".join(tags_validos))
            continue

        if not clear_text(mensaje):
            continue

        ultima_pregunta = mensaje
        print("ChatPlay:", responder(mensaje))


if __name__ == "__main__":
    iniciar_chat()
