from openai import OpenAI
from functions import (
    validate_input, clean_text, format_response,
    is_exit_command, is_help_command, split_conversation
)
from config import OPENAI_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE, SYSTEM_PROMPT


def create_client(api_key: str = OPENAI_API_KEY):
    if api_key:
        return OpenAI(api_key=api_key)
    return None


def build_messages(user_input: str, history: list, system_prompt: str = SYSTEM_PROMPT):
    messages = [{"role": "system", "content": system_prompt}]
    for h in split_conversation(history):
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": h["assistant"]})
    messages.append({"role": "user", "content": user_input})
    return messages


def ask_openai(client, messages):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    return response.choices[0].message.content


def get_local_response(user_input: str):
    user_input = user_input.lower()

    responses = {
        "hola": "¡Hola! ¿En qué puedo ayudarte hoy?",
        "cómo estás": "¡Estoy muy bien, gracias por preguntar! ¿Y tú?",
        "qué es python": "Python es un lenguaje de programación interpretado, de alto nivel y multiplataforma, muy usado en IA, ciencia de datos y desarrollo web.",
        "qué es ia": "La Inteligencia Artificial es una rama de la informática que crea sistemas capaces de realizar tareas que requieren inteligencia humana.",
        "gracias": "¡De nada! Estoy aquí para ayudarte.",
    }

    for key, value in responses.items():
        if key in user_input:
            return value

    return "Lo siento, no tengo una respuesta para eso. Puedes preguntarme sobre Python, IA o simplemente saludar."


def show_help():
    print("Comandos disponibles:")
    print("  help / ayuda  - Muestra esta ayuda")
    print("  salir / exit  - Termina la conversación")
    print()
    print("Puedes preguntarme sobre:")
    print("  - Python")
    print("  - Inteligencia Artificial")
    print("  - O simplemente conversar")


def chat():
    print("=" * 50)
    print("  🤖 CHATBOT IA - Asistente Virtual")
    print("=" * 50)
    print("  Escribe 'ayuda' para ver comandos")
    print("  Escribe 'salir' para terminar")
    print("-" * 50)

    client = create_client()
    if client:
        print("  ✅ Modo: OpenAI API")
    else:
        print("  ⚠️  Modo: Local (sin API key)")
    print("-" * 50)

    history = []
    use_api = client is not None

    while True:
        try:
            user_input = input("\nTú: ")
            if not validate_input(user_input):
                print("Chatbot: Por favor escribe algo.")
                continue

            user_input = clean_text(user_input)

            if is_exit_command(user_input):
                print("Chatbot: ¡Gracias por conversar! Hasta luego. 👋")
                break

            if is_help_command(user_input):
                show_help()
                continue

            if use_api:
                messages = build_messages(user_input, history)
                response = ask_openai(client, messages)
            else:
                response = get_local_response(user_input)

            response = format_response(response)
            print(f"Chatbot: {response}")

            history.append({"user": user_input, "assistant": response})

        except KeyboardInterrupt:
            print("\n\nChatbot: Conversación terminada. ¡Hasta luego!")
            break
        except Exception as e:
            print(f"Error: {e}. Cambiando a modo local...")
            use_api = False
            client = None


if __name__ == "__main__":
    chat()
