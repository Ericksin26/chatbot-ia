import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "150"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "Eres un asistente amigable y servicial.")
