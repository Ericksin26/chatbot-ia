import re


def validate_input(text: str) -> bool:
    if not text or not text.strip():
        return False
    return True


def clean_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text


def format_response(text: str, max_length: int = 500) -> str:
    if len(text) > max_length:
        text = text[:max_length] + "..."
    return text


def is_exit_command(text: str) -> bool:
    text = text.lower().strip()
    return text in ("salir", "exit", "quit", "chao", "adiós", "adios", "bye")


def is_help_command(text: str) -> bool:
    text = text.lower().strip()
    return text in ("help", "ayuda", "comandos", "commands")


def split_conversation(history: list, max_pairs: int = 5) -> list:
    return history[-max_pairs:]


def count_words(text: str) -> int:
    return len(text.split())


def count_tokens(text: str) -> int:
    return len(text.split()) + text.count(".") + text.count(",")
