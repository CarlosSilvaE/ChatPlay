import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.text_utils import clear_text


def construir_features(juego):
    features = []

    if "genero" in juego:
        features.append("genero_" + clear_text(juego["genero"]))

    if "subgenero" in juego:
        features.append("subgenero_" + clear_text(juego["subgenero"]))

    if "sistemas" in juego:
        for sistema in juego["sistemas"]:
            features.append("sistema_" + clear_text(sistema))

    return features


def crear_matriz_one_hot(games_data):
    games_df = pd.DataFrame(games_data)

    games_df["features"] = games_df.apply(
        lambda fila: construir_features(fila.to_dict()),
        axis=1
    )

    mlb = MultiLabelBinarizer()
    matriz = mlb.fit_transform(games_df["features"])

    one_hot_df = pd.DataFrame(
        matriz,
        columns=mlb.classes_,
        index=games_df["juego"]
    )

    return games_df, one_hot_df


def convertir_a_lista(juegos_base):
    if isinstance(juegos_base, str):
        return [juegos_base]

    if isinstance(juegos_base, list):
        return juegos_base

    return []


def recomendar_juegos_similares(juegos_base, games_data, top_n=3):
    games_df, one_hot_df = crear_matriz_one_hot(games_data)

    juegos_normalizados = {
        clear_text(juego): juego
        for juego in one_hot_df.index
    }

    juegos_base = convertir_a_lista(juegos_base)

    juegos_base_reales = []

    for juego in juegos_base:
        juego_limpio = clear_text(juego)

        if juego_limpio in juegos_normalizados:
            juegos_base_reales.append(juegos_normalizados[juego_limpio])

    if not juegos_base_reales:
        return []

    vectores_base = one_hot_df.loc[juegos_base_reales]

    perfil_usuario = vectores_base.mean(axis=0)

    similitudes = cosine_similarity(
        [perfil_usuario],
        one_hot_df
    )[0]

    resultados = pd.DataFrame({
        "juego": one_hot_df.index,
        "similitud": similitudes
    })

    resultados = resultados[
        ~resultados["juego"].isin(juegos_base_reales)
    ]

    resultados = resultados.sort_values(
        by="similitud",
        ascending=False
    )

    return resultados.head(top_n).to_dict("records")