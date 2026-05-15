import random
from utils.text_utils import clear_text

def buscar_juegos_por_genero(genero, games_data):
    resultados = []

    for juego in games_data:
        if clear_text(juego["genero"]) == clear_text(genero):
            resultados.append(juego)

    return resultados


def buscar_juegos_por_sistema(sistema, games_data):
    resultados = []

    for juego in games_data:
        for sistema_juego in juego["sistemas"]:
            if clear_text(sistema) in clear_text(sistema_juego):
                resultados.append(juego)
                break

    return resultados


def buscar_juegos_por_genero_y_sistema(genero, sistema, games_data):
    resultados = []

    for juego in games_data:
        coincide_genero = clear_text(juego["genero"]) == clear_text(genero)

        coincide_sistema = any(
            clear_text(sistema) in clear_text(sistema_juego)
            for sistema_juego in juego["sistemas"]
        )

        if coincide_genero and coincide_sistema:
            resultados.append(juego)

    return resultados