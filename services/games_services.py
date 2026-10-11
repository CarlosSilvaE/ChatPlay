from utils.text_utils import clear_text


def _contiene_frase(texto, frase):
    return f" {frase} " in f" {texto} "


def extraer_genero(mensaje):
    generos = [
        "terror",
        "aventura",
        "supervivencia",
        "plataformas",
        "accion",
        "carreras",
        "simulacion",
        "estrategia",
        "deportes",
        "puzzle",
    ]

    mensaje_limpio = clear_text(mensaje)

    for genero in generos:
        if _contiene_frase(mensaje_limpio, genero):
            return genero

    return None


def extraer_sistema(mensaje):
    sistemas = {
        "pc": "PC",
        "computadora": "PC",
        "xbox one": "Xbox One",
        "xbox series x": "Xbox Series X/S",
        "xbox series s": "Xbox Series X/S",
        "xbox series": "Xbox Series X/S",
        "xbox": "Xbox",
        "playstation 4": "PlayStation 4",
        "playstation 5": "PlayStation 5",
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

    for clave in sorted(sistemas, key=len, reverse=True):
        if _contiene_frase(mensaje_limpio, clave):
            return sistemas[clave]

    return None


def extraer_juego(mensaje, games_data):
    mensaje_limpio = clear_text(mensaje)

    for juego in sorted(
        games_data,
        key=lambda item: len(clear_text(item["juego"])),
        reverse=True,
    ):
        nombre_juego = clear_text(juego["juego"])
        if _contiene_frase(mensaje_limpio, nombre_juego):
            return juego["juego"]

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

    for alias in sorted(aliases, key=len, reverse=True):
        if _contiene_frase(mensaje_limpio, alias):
            nombre_real = aliases[alias]
            if any(
                clear_text(juego["juego"]) == clear_text(nombre_real)
                for juego in games_data
            ):
                return nombre_real

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