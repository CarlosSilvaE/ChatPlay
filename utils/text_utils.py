import re
import unicodedata

def clear_text(text):
    text = text.lower()

    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")

    # 3. quitar caracteres raros y signos
    text = re.sub(r"[^a-z0-9\s]", "", text)

    # 4. quitar espacios duplicados
    text = re.sub(r"\s+", " ", text).strip()

    return text