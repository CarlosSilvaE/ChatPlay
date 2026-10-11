import json
from pathlib import Path

from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline

from services.cache_services import (
    inicializar_cache,
    obtener_ejemplos_confirmados,
)
from services.learning_services import (
    crear_clasificador,
    crear_vectorizer,
    entrenar_modelo as ajustar_modelo,
    preparar_datos,
    resumen_clases,
)


PROJECT_ROOT = Path(__file__).resolve().parent
INTENTS_PATH = PROJECT_ROOT / "Datasets" / "intents.json"


def cargar_intenciones(ruta_json=INTENTS_PATH):
    with open(ruta_json, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def evaluar_y_entrenar():
    inicializar_cache()
    data = cargar_intenciones()
    textos, etiquetas = preparar_datos(
        data,
        obtener_ejemplos_confirmados(),
    )
    conteo = resumen_clases(etiquetas)
    menor_clase = min(conteo.values())
    if menor_clase < 2:
        raise ValueError(
            "Se necesitan al menos dos ejemplos por intención para evaluar "
            "el modelo con validación cruzada."
        )

    pliegues = min(5, menor_clase)
    validacion = StratifiedKFold(
        n_splits=pliegues,
        shuffle=True,
        random_state=42,
    )
    evaluador = make_pipeline(crear_vectorizer(), crear_clasificador())
    predicciones = cross_val_predict(
        evaluador,
        textos,
        etiquetas,
        cv=validacion,
    )
    print(f"Ejemplos por intención: {conteo}")
    print(f"Evaluación estratificada ({pliegues} pliegues):")
    print(
        classification_report(
            etiquetas,
            predicciones,
            zero_division=0,
        )
    )

    modelo, vectorizer = ajustar_modelo(textos, etiquetas)
    print(
        f"Modelo final entrenado en memoria: {len(textos)} ejemplos, "
        f"{len(modelo.classes_)} intenciones."
    )
    return modelo, vectorizer


if __name__ == "__main__":
    evaluar_y_entrenar()