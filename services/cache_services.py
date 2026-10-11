from contextlib import contextmanager
import sqlite3
from pathlib import Path

from utils.text_utils import clear_text


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = PROJECT_ROOT / "data" / "chatplay.sqlite3"


def _connect(database_path=DATABASE_PATH):
    database_path = Path(database_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(database_path)


@contextmanager
def _connection(database_path=DATABASE_PATH):
    connection = _connect(database_path)
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def inicializar_cache(database_path=DATABASE_PATH):
    with _connection(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS response_cache (
                question_key TEXT PRIMARY KEY,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                intent TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS confirmed_examples (
                question_key TEXT PRIMARY KEY,
                question TEXT NOT NULL,
                intent TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def _question_key(question):
    return clear_text(question)


def obtener_respuesta_cacheada(question, database_path=DATABASE_PATH):
    key = _question_key(question)
    if not key:
        return None
    with _connection(database_path) as connection:
        row = connection.execute(
            "SELECT answer, intent FROM response_cache WHERE question_key = ?",
            (key,),
        ).fetchone()
    return tuple(row) if row else None


def guardar_respuesta_cache(question, answer, intent, database_path=DATABASE_PATH):
    key = _question_key(question)
    if not key:
        return
    with _connection(database_path) as connection:
        connection.execute(
            """
            INSERT INTO response_cache (question_key, question, answer, intent)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(question_key) DO UPDATE SET
                question = excluded.question,
                answer = excluded.answer,
                intent = excluded.intent,
                updated_at = CURRENT_TIMESTAMP
            """,
            (key, question, answer, intent),
        )


def guardar_ejemplo_confirmado(question, intent, database_path=DATABASE_PATH):
    key = _question_key(question)
    if not key:
        raise ValueError("No se puede etiquetar una pregunta vacía.")
    with _connection(database_path) as connection:
        connection.execute(
            """
            INSERT INTO confirmed_examples (question_key, question, intent)
            VALUES (?, ?, ?)
            ON CONFLICT(question_key) DO UPDATE SET
                question = excluded.question,
                intent = excluded.intent,
                updated_at = CURRENT_TIMESTAMP
            """,
            (key, question, intent),
        )
        connection.execute(
            "DELETE FROM response_cache WHERE question_key = ?",
            (key,),
        )


def obtener_ejemplos_confirmados(database_path=DATABASE_PATH):
    with _connection(database_path) as connection:
        rows = connection.execute(
            "SELECT question, intent FROM confirmed_examples ORDER BY question_key"
        ).fetchall()
    return [{"question": question, "intent": intent} for question, intent in rows]
