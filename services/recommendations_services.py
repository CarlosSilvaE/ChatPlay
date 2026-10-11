from utils.text_utils import clear_text


def _coincide_sistema(sistema_buscado, sistema_juego):
    buscado = clear_text(sistema_buscado)
    disponible = clear_text(sistema_juego)

    if buscado == "xbox":
        return disponible.startswith("xbox")
    if buscado == "xbox one":
        return disponible in ("xbox", "xbox one")
    if buscado == "xbox series xs":
        return disponible in (
            "xbox",
            "xbox series xs",
            "xbox series x",
            "xbox series s",
        )
    if buscado == "playstation":
        return disponible.startswith("playstation")
    if buscado in ("playstation 4", "playstation 5"):
        return disponible in ("playstation", buscado)
    return buscado in disponible


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
            if _coincide_sistema(sistema, sistema_juego):
                resultados.append(juego)
                break

    return resultados


def buscar_juegos_por_genero_y_sistema(genero, sistema, games_data):
    resultados = []

    for juego in games_data:
        coincide_genero = clear_text(juego["genero"]) == clear_text(genero)

        coincide_sistema = any(
            _coincide_sistema(sistema, sistema_juego)
            for sistema_juego in juego["sistemas"]
        )

        if coincide_genero and coincide_sistema:
            resultados.append(juego)

    return resultados