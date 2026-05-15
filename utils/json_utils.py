import json
import pickle

def cargar_json(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def cargar_pickle(ruta):
    with open(ruta, "rb") as archivo:
        return pickle.load(archivo)