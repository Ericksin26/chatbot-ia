import re
import json
import os
import random
import math
from datetime import datetime


HISTORY_FILE = "historial.json"


def validate_input(text: str) -> bool:
    if not text or not text.strip():
        return False
    return True


def clean_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text


def format_response(text: str, max_length: int = 800) -> str:
    if len(text) > max_length:
        text = text[:max_length] + "..."
    return text


def is_exit_command(text: str) -> bool:
    text = text.lower().strip()
    return text in ("salir", "exit", "quit", "chao", "adios", "adiós", "bye", "terminar", "finalizar")


def is_help_command(text: str) -> bool:
    text = text.lower().strip()
    return text in ("help", "ayuda", "comandos", "commands", "que puedo preguntar", "que hago")


def is_stats_command(text: str) -> bool:
    text = text.lower().strip()
    return text in ("stats", "estadisticas", "estadísticas", "historial", "history")


def is_clear_command(text: str) -> bool:
    text = text.lower().strip()
    return text in ("clear", "limpiar", "borrar historial", "reiniciar")


def is_greeting(text: str) -> bool:
    text = text.lower().strip()
    greetings = ("hola", "buenos dias", "buenas tardes", "buenas noches", "hey", "buen dia", "que tal", "como estas", "cómo estás")
    return any(g in text for g in greetings)


def is_farewell(text: str) -> bool:
    text = text.lower().strip()
    farewells = ("chao", "bye", "nos vemos", "hasta luego", "adios", "adiós", "cuidate", "cuídate")
    return any(f in text for f in farewells)


def is_weather_query(text: str) -> bool:
    text = text.lower().strip()
    keywords = ("clima", "temperatura", "lluvia", "soleado", "climático", "climatica", "pronostico", "pronóstico")
    return any(k in text for k in keywords)


def is_time_query(text: str) -> bool:
    text = text.lower().strip()
    keywords = ("hora", "que hora es", "qué hora es", "hora actual", "reloj")
    return any(k in text for k in keywords)


def is_date_query(text: str) -> bool:
    text = text.lower().strip()
    keywords = ("fecha", "que dia es", "qué día es", "dia de hoy", "día de hoy", "que fecha", "qué fecha")
    return any(k in text for k in keywords)


def is_joke_query(text: str) -> bool:
    text = text.lower().strip()
    keywords = ("chiste", "broma", "hazme reir", "hazme reír", "algo gracioso", "cuentame un chiste", "cuéntame un chiste")
    return any(k in text for k in keywords)


def is_calculator_query(text: str) -> bool:
    text = text.lower().strip()
    keywords = ("calcula", "calculadora", "cuanto es", "cuánto es", "resultado", "operacion", "operación")
    return any(k in text for k in keywords)


def is_riddle_query(text: str) -> bool:
    text = text.lower().strip()
    keywords = ("adivinanza", "adivina", "acertijo", "que soy", "qué soy")
    return any(k in text for k in keywords)


def split_conversation(history: list, max_pairs: int = 5) -> list:
    return history[-max_pairs:]


def count_words(text: str) -> int:
    return len(text.split())


def count_tokens(text: str) -> int:
    return len(text.split()) + text.count(".") + text.count(",")


def contains_question(text: str) -> bool:
    return "?" in text or text.lower().startswith(("que", "qué", "como", "cómo", "cuando", "cuándo", "donde", "dónde", "por que", "por qué", "quien", "quién", "cual", "cuál"))


def contains_number(text: str) -> bool:
    return bool(re.search(r'\d+', text))


def detect_topic(text: str) -> str:
    text = text.lower()
    topics = {
        "python": ["python", "programacion", "programación", "codigo", "código", "lenguaje"],
        "ia": ["inteligencia artificial", "ia", "machine learning", "aprendizaje automatico", "deep learning", "red neuronal", "algoritmo"],
        "datos": ["datos", "data", "analisis", "análisis", "estadistica", "estadística", "big data"],
        "web": ["web", "internet", "pagina", "página", "sitio", "html", "css", "javascript", "django", "flask"],
        "matematicas": ["matematica", "matemática", "calculo", "calcular", "algebra", "álgebra", "numero", "número"],
        "clima": ["clima", "temperatura", "lluvia", "soleado", "pronostico", "pronóstico"],
        "tiempo": ["hora", "reloj", "minuto", "segundo"],
        "fecha": ["fecha", "dia", "día", "semana", "mes", "año", "calendario"],
        "chiste": ["chiste", "broma", "gracioso", "reir", "reír", "humor"],
        "calculadora": ["calcula", "calculadora", "suma", "resta", "multiplica", "divide", "operacion", "operación", "mas", "menos", "por"],
        "adivinanza": ["adivinanza", "adivina", "acertijo", "que soy", "qué soy"],
        "saludo": ["hola", "buenos", "buenas", "hey"],
    }
    for topic, keywords in topics.items():
        if any(k in text for k in keywords):
            return topic
    return "general"


def save_history(history: list, filename: str = HISTORY_FILE):
    data = {
        "ultima_sesion": datetime.now().isoformat(),
        "total_mensajes": len(history),
        "conversacion": history
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_history(filename: str = HISTORY_FILE) -> list:
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("conversacion", [])
    return []
