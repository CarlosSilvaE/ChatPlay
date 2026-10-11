import json
import tempfile
import unittest
from pathlib import Path

from services.cache_services import (
    guardar_ejemplo_confirmado,
    guardar_respuesta_cache,
    inicializar_cache,
    obtener_ejemplos_confirmados,
    obtener_respuesta_cacheada,
)
from services.learning_services import entrenar_modelo, preparar_datos
from services.intents_services import predecir_intencion
from services.recommendations_services import buscar_juegos_por_sistema
from services.games_services import (
    buscar_info_juego,
    buscar_tips_por_juego,
    extraer_genero,
    extraer_juego,
    extraer_sistema,
)
from utils.text_utils import clear_text


class LearningAndCacheTests(unittest.TestCase):
    def test_confirmed_example_overrides_the_original_training_label(self):
        data = {
            "intents": [
                {"tag": "saludo", "patterns": ["Hola", "Buenos días"]},
                {"tag": "ayuda", "patterns": ["Necesito ayuda"]},
            ]
        }

        texts, labels = preparar_datos(
            data,
            [{"question": " HOLA! ", "intent": "ayuda"}],
        )

        self.assertEqual(texts, ["hola", "buenos dias", "necesito ayuda"])
        self.assertEqual(labels, ["ayuda", "saludo", "ayuda"])

    def test_conflicting_source_labels_fail_loudly(self):
        data = {
            "intents": [
                {"tag": "saludo", "patterns": ["Hola"]},
                {"tag": "ayuda", "patterns": ["HOLA!"]},
            ]
        }

        with self.assertRaisesRegex(ValueError, "etiquetas incompatibles"):
            preparar_datos(data)

    def test_classifier_learns_a_known_pattern(self):
        intents_path = (
            Path(__file__).resolve().parents[1]
            / "Datasets"
            / "intents.json"
        )
        data = json.loads(intents_path.read_text(encoding="utf-8"))
        texts, labels = preparar_datos(data)
        model, vectorizer = entrenar_modelo(texts, labels)

        prediction = model.predict(vectorizer.transform(["hola"]))[0]

        self.assertEqual(prediction, "Saludo")
        self.assertEqual(
            predecir_intencion("Buenos días", model, vectorizer)[0],
            "Saludo",
        )
        self.assertEqual(
            predecir_intencion("asdasdfzzq", model, vectorizer)[0],
            "fallback",
        )

    def test_cache_is_normalized_and_removed_when_question_is_labeled(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = Path(temp_dir) / "cache.sqlite3"
            inicializar_cache(database_path)
            guardar_respuesta_cache(
                "¿Qué tal?",
                "Hola.",
                "Saludo",
                database_path,
            )

            self.assertEqual(
                obtener_respuesta_cacheada("que TAL", database_path),
                ("Hola.", "Saludo"),
            )

            guardar_ejemplo_confirmado(
                "que TAL",
                "Saludo",
                database_path,
            )

            self.assertIsNone(
                obtener_respuesta_cacheada("¿Qué tal?", database_path)
            )
            self.assertEqual(
                obtener_ejemplos_confirmados(database_path),
                [{"question": "que TAL", "intent": "Saludo"}],
            )

    def test_game_lookup_supports_minecraft_alias_and_exact_platform(self):
        root = Path(__file__).resolve().parents[1] / "Datasets"
        games = json.loads((root / "games.json").read_text(encoding="utf-8"))
        tips = json.loads((root / "tips.json").read_text(encoding="utf-8"))
        game_name = extraer_juego("Dame información de Minecraft", games)

        self.assertEqual(game_name, "Minecraft")
        self.assertIsNotNone(buscar_info_juego(game_name, games))
        self.assertTrue(buscar_tips_por_juego(game_name, tips))
        self.assertEqual(
            extraer_sistema("¿Está disponible para PlayStation 4?"),
            "PlayStation 4",
        )
        self.assertEqual(
            extraer_sistema("¿Corre en Xbox Series X?"),
            "Xbox Series X/S",
        )
        self.assertIsNone(extraer_genero("estoy teniendo una reacción"))

        series_x_games = buscar_juegos_por_sistema("Xbox Series X/S", games)
        self.assertGreater(len(series_x_games), 15)
        self.assertIn(
            "Resident Evil 4 Remake",
            [game["juego"] for game in series_x_games],
        )
        self.assertNotIn(
            "The Forest",
            [game["juego"] for game in series_x_games],
        )

    def test_added_dataset_counts_and_tip_references(self):
        root = Path(__file__).resolve().parents[1] / "Datasets"
        games = json.loads((root / "games.json").read_text(encoding="utf-8"))
        tips = json.loads((root / "tips.json").read_text(encoding="utf-8"))
        intents = json.loads((root / "intents.json").read_text(encoding="utf-8"))

        self.assertEqual(len(games), 111)
        self.assertEqual(len(tips), 122)
        self.assertEqual(
            sum(len(intent["patterns"]) for intent in intents["intents"]),
            162,
        )
        self.assertEqual(len({game["juego"] for game in games}), len(games))
        game_names = {game["juego"] for game in games}
        self.assertTrue(all(tip["juego"] in game_names for tip in tips))
        self.assertEqual(
            {game["juego"] for game in games[11:]},
            {tip["juego"] for tip in tips[22:]},
        )
        self.assertEqual(
            len(
                {
                    clear_text(pattern)
                    for intent in intents["intents"]
                    for pattern in intent["patterns"]
                }
            ),
            162,
        )
        self.assertTrue(
            all(
                game["genero"] in {
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
                }
                for game in games
            )
        )

    def test_longest_exact_game_name_wins_over_alias(self):
        games = [
            {"juego": "Super Mario Bros. Wonder"},
            {"juego": "Super Mario Odyssey"},
            {"juego": "Mario Kart 8 Deluxe"},
        ]

        self.assertEqual(
            extraer_juego("Háblame de Super Mario Odyssey", games),
            "Super Mario Odyssey",
        )
        self.assertEqual(
            extraer_juego("Quiero información de Mario Kart 8 Deluxe", games),
            "Mario Kart 8 Deluxe",
        )

    def test_all_catalog_titles_are_detectable(self):
        root = Path(__file__).resolve().parents[1] / "Datasets"
        games = json.loads((root / "games.json").read_text(encoding="utf-8"))

        for game in games:
            with self.subTest(game=game["juego"]):
                self.assertEqual(
                    extraer_juego(
                        f"Quiero información de {game['juego']}",
                        games,
                    ),
                    game["juego"],
                )


if __name__ == "__main__":
    unittest.main()
