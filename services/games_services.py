import random
from utils.text_utils import clear_text

def extraer_genero(mensaje):
    generos = [
        "terror",
        "aventura",
        "supervivencia",
        "plataformas",
        "accion",
        "carreras",
        "simulacion",
    ]

    mensaje_limpio = clear_text(mensaje)

    for genero in generos:
        if genero in mensaje_limpio:
            return genero

    return None


def extraer_sistema(mensaje):
    sistemas = {
        "pc": "PC",
        "computadora": "PC",
        "xbox": "Xbox",
        "playstation": "PlayStation",
        "ps4": "PlayStation 4",
        "ps5": "PlayStation 5",
        "play 5": "PlayStation 5",
        "play": "PlayStation",
        "switch": "Nintendo Switch",
        "nintendo": "Nintendo Switch",
        "android": "Android",
        "celular": "Android",
        "cel": "Android",
        "ios": "iOS",
        "iphone": "iOS",
    }

    mensaje_limpio = clear_text(mensaje)

    for clave, valor in sistemas.items():
        if clave in mensaje_limpio:
            return valor

    return None


def extraer_juego(mensaje, games_data):
    mensaje_limpio = clear_text(mensaje)
    aliases = {
        "minecraft": "Minecraft",
        "terraria": "Terraria",
        "the forest": "The Forest",
        "forest": "The Forest",
        "subnautica": "Subnautica",
        "ark": "ARK: Survival Evolved",
        "ark survival": "ARK: Survival Evolved",
        "dont starve": "Don't Starve",
        "don't starve": "Don't Starve",
        "raft": "Raft",
        "resident": "Resident Evil 4 Remake",
        "resident evil": "Resident Evil 4 Remake",
        "resident evil 4": "Resident Evil 4 Remake",
        "re 4": "Resident Evil 4 Remake",
        "re4": "Resident Evil 4 Remake",
        "outlast": "Outlast",
        "amnesia": "Amnesia: The Dark Descent",
        "alien isolation": "Alien: Isolation",
        "alien": "Alien: Isolation",
        "evil within": "The Evil Within",
        "the evil within": "The Evil Within",
        "hollow knight": "Hollow Knight",
        "hollow": "Hollow Knight",
        "ori": "Ori and the Blind Forest",
        "ori and the blind forest": "Ori and the Blind Forest",
        "celeste": "Celeste",
        "zelda": "The Legend of Zelda: Breath of the Wild",
        "breath of the wild": "The Legend of Zelda: Breath of the Wild",
        "botw": "The Legend of Zelda: Breath of the Wild",
        "tomb raider": "Tomb Raider",
        "lara croft": "Tomb Raider",
        "geometry": "Geometry Dash",
        "geometry dash": "Geometry Dash",
        "gd": "Geometry Dash",
        "mario": "Super Mario Bros. Wonder",
        "mario wonder": "Super Mario Bros. Wonder",
        "wonder": "Super Mario Bros. Wonder",
        "mario bros": "Super Mario Bros. Wonder",
        "cuphead": "Cuphead",
        "rayman": "Rayman Legends",
        "rayman legends": "Rayman Legends",
        "assassins creed": "Assassin’s Creed Odyssey",
        "assassin creed": "Assassin’s Creed Odyssey",
        "odyssey": "Assassin’s Creed Odyssey",
        "ac odyssey": "Assassin’s Creed Odyssey",
        "god of war": "God of War",
        "gow": "God of War",
        "kratos": "God of War",
        "devil may cry": "Devil May Cry 5",
        "dmc": "Devil May Cry 5",
        "dmc5": "Devil May Cry 5",
        "sekiro": "Sekiro: Shadows Die Twice",
        "spiderman": "Marvel's Spider-Man Remastered",
        "spider man": "Marvel's Spider-Man Remastered",
        "spider-man": "Marvel's Spider-Man Remastered",
        "forza": "Forza Horizon 5",
        "forza horizon": "Forza Horizon 5",
        "fh5": "Forza Horizon 5",
        "nfs": "Need for Speed Heat",
        "need for speed": "Need for Speed Heat",
        "nfs heat": "Need for Speed Heat",
        "gran turismo": "Gran Turismo 7",
        "gt7": "Gran Turismo 7",
        "f1": "F1 23",
        "f1 23": "F1 23",
        "formula 1": "F1 23",
        "mario kart": "Mario Kart 8 Deluxe",
        "mk8": "Mario Kart 8 Deluxe",
        "mk8 deluxe": "Mario Kart 8 Deluxe",
        "stardew": "Stardew Valley",
        "stardew valley": "Stardew Valley",
        "sims": "The Sims 4",
        "the sims": "The Sims 4",
        "sims 4": "The Sims 4",
        "cities skylines": "Cities: Skylines",
        "cities": "Cities: Skylines",
        "flight simulator": "Microsoft Flight Simulator",
        "microsoft flight simulator": "Microsoft Flight Simulator",
        "msfs": "Microsoft Flight Simulator",
        "ets2": "Euro Truck Simulator 2",
        "euro truck": "Euro Truck Simulator 2",
        "truck simulator": "Euro Truck Simulator 2"
    }

    for alias, nombre_real in aliases.items():
        if alias in mensaje_limpio:
            return nombre_real

    for juego in games_data:
        nombre_juego = clear_text(juego["juego"])

        if nombre_juego in mensaje_limpio:
            return juego["juego"]

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

def extraer_juegos(mensaje, games_data):
    mensaje_limpio = clear_text(mensaje)
    juegos_encontrados = []

    aliases = {
        "minecraft": "Minecraft",
        "terraria": "Terraria",
        "the forest": "The Forest",
        "forest": "The Forest",
        "subnautica": "Subnautica",
        "ark": "ARK: Survival Evolved",
        "ark survival": "ARK: Survival Evolved",
        "dont starve": "Don't Starve",
        "don't starve": "Don't Starve",
        "raft": "Raft",
        "resident": "Resident Evil 4 Remake",
        "resident evil": "Resident Evil 4 Remake",
        "resident evil 4": "Resident Evil 4 Remake",
        "re 4": "Resident Evil 4 Remake",
        "re4": "Resident Evil 4 Remake",
        "outlast": "Outlast",
        "amnesia": "Amnesia: The Dark Descent",
        "alien isolation": "Alien: Isolation",
        "alien": "Alien: Isolation",
        "evil within": "The Evil Within",
        "the evil within": "The Evil Within",
        "hollow knight": "Hollow Knight",
        "hollow": "Hollow Knight",
        "ori": "Ori and the Blind Forest",
        "ori and the blind forest": "Ori and the Blind Forest",
        "celeste": "Celeste",
        "zelda": "The Legend of Zelda: Breath of the Wild",
        "breath of the wild": "The Legend of Zelda: Breath of the Wild",
        "botw": "The Legend of Zelda: Breath of the Wild",
        "tomb raider": "Tomb Raider",
        "lara croft": "Tomb Raider",
        "geometry": "Geometry Dash",
        "geometry dash": "Geometry Dash",
        "gd": "Geometry Dash",
        "mario": "Super Mario Bros. Wonder",
        "mario wonder": "Super Mario Bros. Wonder",
        "wonder": "Super Mario Bros. Wonder",
        "mario bros": "Super Mario Bros. Wonder",
        "cuphead": "Cuphead",
        "rayman": "Rayman Legends",
        "rayman legends": "Rayman Legends",
        "assassins creed": "Assassin’s Creed Odyssey",
        "assassin creed": "Assassin’s Creed Odyssey",
        "odyssey": "Assassin’s Creed Odyssey",
        "ac odyssey": "Assassin’s Creed Odyssey",
        "god of war": "God of War",
        "gow": "God of War",
        "kratos": "God of War",
        "devil may cry": "Devil May Cry 5",
        "dmc": "Devil May Cry 5",
        "dmc5": "Devil May Cry 5",
        "sekiro": "Sekiro: Shadows Die Twice",
        "spiderman": "Marvel's Spider-Man Remastered",
        "spider man": "Marvel's Spider-Man Remastered",
        "spider-man": "Marvel's Spider-Man Remastered",
        "forza": "Forza Horizon 5",
        "forza horizon": "Forza Horizon 5",
        "fh5": "Forza Horizon 5",
        "nfs": "Need for Speed Heat",
        "need for speed": "Need for Speed Heat",
        "nfs heat": "Need for Speed Heat",
        "gran turismo": "Gran Turismo 7",
        "gt7": "Gran Turismo 7",
        "f1": "F1 23",
        "f1 23": "F1 23",
        "formula 1": "F1 23",
        "mario kart": "Mario Kart 8 Deluxe",
        "mk8": "Mario Kart 8 Deluxe",
        "mk8 deluxe": "Mario Kart 8 Deluxe",
        "stardew": "Stardew Valley",
        "stardew valley": "Stardew Valley",
        "sims": "The Sims 4",
        "the sims": "The Sims 4",
        "sims 4": "The Sims 4",
        "cities skylines": "Cities: Skylines",
        "cities": "Cities: Skylines",
        "flight simulator": "Microsoft Flight Simulator",
        "microsoft flight simulator": "Microsoft Flight Simulator",
        "msfs": "Microsoft Flight Simulator",
        "ets2": "Euro Truck Simulator 2",
        "euro truck": "Euro Truck Simulator 2",
        "truck simulator": "Euro Truck Simulator 2"
    }

    for alias, nombre_real in aliases.items():
        if alias in mensaje_limpio:
            if nombre_real not in juegos_encontrados:
                juegos_encontrados.append(nombre_real)

    for juego in games_data:
        nombre_real = juego["juego"]
        nombre_limpio = clear_text(nombre_real)

        if nombre_limpio in mensaje_limpio:
            if nombre_real not in juegos_encontrados:
                juegos_encontrados.append(nombre_real)

    return juegos_encontrados