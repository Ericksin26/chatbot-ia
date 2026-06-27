import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "200"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "Eres un asistente amigable, servicial y con conocimientos en programacion, inteligencia artificial, matematicas y tecnologia. Responde en español de forma clara y concisa.")

SAVE_HISTORY = os.getenv("SAVE_HISTORY", "true").lower() == "true"
MAX_HISTORY = int(os.getenv("MAX_HISTORY", "50"))
APP_NAME = "Chatbot IA - Asistente Virtual"
VERSION = "2.0.0"
