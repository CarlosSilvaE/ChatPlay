import random
from utils.text_utils import clear_text

def extraer_genero(mensaje):
    generos = [
        "terror",
        "aventura",
        "supervivencia",
        "plataformas",
        "accion",
        "carreras",
        "simulacion",
    ]

    mensaje_limpio = clear_text(mensaje)

    for genero in generos:
        if genero in mensaje_limpio:
            return genero

    return None


def extraer_sistema(mensaje):
    sistemas = {
        "pc": "PC",
        "computadora": "PC",
        "xbox": "Xbox",
        "playstation": "PlayStation",
        "ps4": "PlayStation 4",
        "ps5": "PlayStation 5",
        "switch": "Nintendo Switch",
        "nintendo": "Nintendo Switch",
        "android": "Android",
        "ios": "iOS",
        "iphone": "iOS",
    }

    mensaje_limpio = clear_text(mensaje)

    for clave, valor in sistemas.items():
        if clave in mensaje_limpio:
            return valor

    return None


def extraer_juego(mensaje, games_data):
    mensaje_limpio = clear_text(mensaje)

    aliases = {
        "minecraft": "Minecraft",
        "resident evil": "Resident Evil 4 Remake",
        "resident evil 4": "Resident Evil 4 Remake",
        "re 4": "Resident Evil 4 Remake",
        "re4": "Resident Evil 4 Remake",
        "hollow knight": "Hollow Knight",
        "terraria": "Terraria",
        "forza": "Forza Horizon 5",
        "forza horizon": "Forza Horizon 5",
        "nfs": "Need for Speed Heat",
        "need for speed": "Need for Speed Heat",
        "geometry": "Geometry Dash",
        "geometry dash": "Geometry Dash",
        "mario": "Super Mario Bros. Wonder",
        "stardew": "Stardew Valley",
    }

    for alias, nombre_real in aliases.items():
        if alias in mensaje_limpio:
            return nombre_real

    for juego in games_data:
        nombre_juego = clear_text(juego["juego"])

        if nombre_juego in mensaje_limpio:
            return juego["juego"]

    return None

def buscar_info_juego(nombre_juego, games_data):
    for juego in games_data:
        if clear_text(juego["juego"]) == clear_text(nombre_juego):
            return juego

    return None


def buscar_tips_por_juego(nombre_juego, tips_data):
    resultados = []

    for tip in tips_data:
        if clear_text(tip["juego"]) == clear_text(nombre_juego):
            resultados.append(tip)

    return resultados