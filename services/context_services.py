contexto = {
    "ultimo_juego": None,
    "ultimo_genero": None,
    "ultimo_sistema": None,
    "ultima_intencion": None
}


def guardar_juego(juego):
    contexto["ultimo_juego"] = juego


def obtener_juego():
    return contexto["ultimo_juego"]


def guardar_genero(genero):
    contexto["ultimo_genero"] = genero


def obtener_genero():
    return contexto["ultimo_genero"]


def guardar_sistema(sistema):
    contexto["ultimo_sistema"] = sistema


def obtener_sistema():
    return contexto["ultimo_sistema"]


def guardar_intencion(tag):
    contexto["ultima_intencion"] = tag


def obtener_intencion():
    return contexto["ultima_intencion"]


def limpiar_contexto():
    contexto["ultimo_juego"] = None
    contexto["ultimo_genero"] = None
    contexto["ultimo_sistema"] = None
    contexto["ultima_intencion"] = None