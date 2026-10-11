# ChatPlay

ChatPlay es un chatbot de consola en español sobre videojuegos. La detección de
intenciones usa **Machine Learning supervisado** con TF-IDF y regresión
logística; no usa una red neuronal ni Deep Learning.

## Instalación y ejecución en Windows

Desde la carpeta del proyecto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python train.py
python chatbot.py
```

`train.py` imprime una evaluación estratificada de validación cruzada. ChatPlay
entrena en memoria al iniciar y vuelve a entrenar después de guardar un ejemplo
etiquetado. No es necesario generar archivos `.pkl`.

## Caché y aprendizaje revisado

- Las preguntas y respuestas se guardan localmente en `data/chatplay.sqlite3`.
- Una pregunta repetida (sin distinguir mayúsculas, acentos o puntuación) usa la
  respuesta cacheada.
- El modelo **no se entrena automáticamente con sus propias predicciones**.
  Después de una respuesta, escribe `/etiquetar <intención>` para confirmar la
  intención real de la última pregunta. Por ejemplo: `/etiquetar info_juego`.
- `/intenciones` muestra las etiquetas disponibles. Una etiqueta confirmada se
  incorpora al siguiente entrenamiento en memoria y se invalida la respuesta
  cacheada de esa pregunta.
- `/salir` termina el chat. Los ejemplos confirmados y el caché permanecen en la
  base local; esta base está excluida de Git.

Cada clase empieza con pocos ejemplos, así que la evaluación puede variar y no
garantiza acierto con frases nuevas. Agrega ejemplos variados y correctamente
etiquetados a `Datasets/intents.json`, vuelve a ejecutar `python train.py` y
compara las métricas antes de dar el modelo por bueno.
