from openai import OpenAI
from functions import (
    validate_input, clean_text, format_response,
    is_exit_command, is_help_command, is_stats_command, is_clear_command,
    is_greeting, is_farewell, contains_question, detect_topic,
    split_conversation, count_words, count_tokens,
    save_history, load_history
)
from config import (
    OPENAI_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE, SYSTEM_PROMPT,
    SAVE_HISTORY, MAX_HISTORY, APP_NAME, VERSION
)


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
    topic = detect_topic(user_input)
    word_count = count_words(user_input)

    saludos = {
        "hola": "¡Hola! ¿En qué puedo ayudarte hoy? Puedes preguntarme sobre Python, IA, programación, matemáticas o tecnología.",
        "buenos dias": "¡Buenos días! Espero que tengas un excelente día. ¿En qué puedo ayudarte?",
        "buenas tardes": "¡Buenas tardes! ¿Cómo va tu día? Estoy aquí para lo que necesites.",
        "buenas noches": "¡Buenas noches! Si necesitas ayuda con algo, aquí estoy.",
        "que tal": "¡Todo bien! ¿Y tú? Cuéntame en qué puedo ayudarte.",
        "como estas": "¡Muy bien, gracias! Estoy listo para ayudarte con lo que necesites.",
    }

    despedidas = {
        "chao": "¡Chao! Que tengas un excelente día. ¡Vuelve cuando quieras!",
        "nos vemos": "¡Nos vemos! Fue un gusto conversar contigo.",
        "hasta luego": "¡Hasta luego! Si necesitas algo más, aquí estaré.",
        "cuidate": "Gracias, tú también cuídate mucho. ¡Hasta pronto!",
    }

    python_responses = [
        "Python es un lenguaje de programación interpretado, de alto nivel y multiplataforma. Fue creado por Guido van Rossum y lanzado en 1991. Es muy usado en inteligencia artificial, ciencia de datos, desarrollo web y automatización.",
        "Python se destaca por su sintaxis clara y legible, lo que lo hace ideal para principiantes. Tiene una gran comunidad y miles de librerías disponibles como NumPy, Pandas, TensorFlow y Django.",
        "En Python puedes hacer desde scripts simples hasta aplicaciones complejas. Es el lenguaje más popular para IA y machine learning gracias a librerías como scikit-learn, PyTorch y Keras.",
        "Python usa indentación para definir bloques de código, a diferencia de otros lenguajes que usan llaves. Esto obliga a escribir código limpio y bien estructurado.",
    ]

    ia_responses = [
        "La Inteligencia Artificial es una rama de la informática que busca crear sistemas capaces de realizar tareas que normalmente requieren inteligencia humana, como el reconocimiento de voz, la toma de decisiones y la traducción de idiomas.",
        "Existen dos tipos principales de IA: la IA Débil (diseñada para tareas específicas) y la IA Fuerte (con capacidad de razonamiento general). Hoy en día usamos principalmente IA Débil en aplicaciones como Siri, Alexa y los chatbots.",
        "El Machine Learning es una subrama de la IA donde las máquinas aprenden de datos sin ser programadas explícitamente. Se divide en: aprendizaje supervisado, no supervisado y por refuerzo.",
        "El Deep Learning usa redes neuronales artificiales con muchas capas para procesar información. Es la tecnología detrás de los autos autónomos, el reconocimiento facial y ChatGPT.",
    ]

    datos_responses = [
        "La ciencia de datos combina estadística, programación y conocimiento del dominio para extraer información valiosa de los datos. Python es el lenguaje más usado en este campo.",
        "Las librerías principales para datos en Python son: NumPy (cálculos numéricos), Pandas (manipulación de datos), Matplotlib (visualización) y Scikit-learn (machine learning).",
        "El análisis de datos sigue estos pasos: 1) Recolección de datos, 2) Limpieza y preparación, 3) Exploración y visualización, 4) Modelado y 5) Interpretación de resultados.",
    ]

    web_responses = [
        "El desarrollo web se divide en frontend (lo que ve el usuario) y backend (la lógica del servidor). Python es muy popular para backend usando frameworks como Django y Flask.",
        "Django es un framework web de alto nivel para Python que sigue el patrón MTV (Model-Template-View). Incluye ORM, autenticación, panel de administración y más.",
        "Flask es un micro-framework para Python, más ligero y flexible que Django. Ideal para APIs REST y aplicaciones pequeñas o medianas.",
    ]

    mates_responses = [
        "Las matemáticas son fundamentales en programación e IA. Conceptos como álgebra lineal, cálculo, probabilidad y estadística son la base de los algoritmos de machine learning.",
        "El álgebra lineal es esencial para entender las redes neuronales. Los datos se representan como vectores y matrices, y las operaciones entre ellos son la base del deep learning.",
    ]

    general_responses = [
        "Interesante pregunta. ¿Podrías darme más detalles para ayudarte mejor?",
        "Entiendo. Dime más sobre eso para poder darte una respuesta más precisa.",
        "Buena pregunta! Puedo ayudarte con temas de programación, IA, matemáticas, tecnología y ciencia de datos.",
        "Estoy aquí para ayudarte. Pregúntame sobre Python, inteligencia artificial, desarrollo web o lo que necesites.",
    ]

    if topic == "saludo" or is_greeting(user_input):
        for key in saludos:
            if key in user_input:
                return saludos[key]
        return saludos["hola"]

    if is_farewell(user_input):
        for key in despedidas:
            if key in user_input:
                return despedidas[key]
        return despedidas["chao"]

    if "gracias" in user_input or "muchas gracias" in user_input or "te agradezco" in user_input:
        return "¡De nada! Me alegra poder ayudarte. Si tienes más preguntas, aquí estoy."

    if "como funciona" in user_input or "cómo funciona" in user_input:
        return "Funciono usando inteligencia artificial. Puedo responder preguntas usando una API de OpenAI (si está configurada) o con respuestas predefinidas en modo local. Mi base de conocimiento incluye programación, IA, matemáticas y tecnología."

    if "quien te creo" in user_input or "quién te creó" in user_input or "quien te hizo" in user_input:
        return "Fui creado como parte de un proyecto académico (Parcial 3) para aprender sobre Python, funciones e inteligencia artificial. Mi código está en GitHub."

    if "que puedes hacer" in user_input or "qué puedes hacer" in user_input:
        return "Puedo conversar contigo, responder preguntas sobre programación Python, inteligencia artificial, ciencia de datos, desarrollo web y matemáticas. También puedo darte ayuda, estadísticas de la conversación y guardar nuestro historial."

    if topic == "python":
        import random
        return python_responses[len(user_input) % len(python_responses)]

    if topic == "ia":
        import random
        return ia_responses[len(user_input) % len(ia_responses)]

    if topic == "datos":
        import random
        return datos_responses[len(user_input) % len(datos_responses)]

    if topic == "web":
        import random
        return web_responses[len(user_input) % len(web_responses)]

    if topic == "matematicas":
        import random
        return mates_responses[len(user_input) % len(mates_responses)]

    if contains_question(user_input):
        import random
        return general_responses[len(user_input) % len(general_responses)]

    import random
    return random.choice(general_responses)


def show_help():
    print("\n" + "-" * 50)
    print("  COMANDOS DISPONIBLES")
    print("-" * 50)
    print("  ayuda / help    - Muestra esta ayuda")
    print("  salir / exit    - Termina la conversacion")
    print("  stats           - Ver estadisticas de la conversacion")
    print("  clear           - Limpiar el historial")
    print("-" * 50)
    print("  TEMAS QUE PUEDES PREGUNTAR:")
    print("  - Python (programacion, codigo)")
    print("  - Inteligencia Artificial (IA, machine learning)")
    print("  - Ciencia de datos (analisis, data science)")
    print("  - Desarrollo web (Django, Flask, HTML, CSS)")
    print("  - Matematicas (calculo, algebra, numeros)")
    print("  - O simplemente conversar!")
    print("-" * 50 + "\n")


def show_stats(history: list):
    if not history:
        print("\n  Aun no hay mensajes en esta sesion.")
        return

    total_mensajes = len(history)
    user_mensajes = sum(1 for h in history if h.get("role") == "user")
    bot_mensajes = total_mensajes - user_mensajes
    total_words_user = sum(count_words(h["user"]) for h in history)
    total_words_bot = sum(count_words(h["assistant"]) for h in history)
    topics = [detect_topic(h["user"]) for h in history]
    top_topic = max(set(topics), key=topics.count) if topics else "N/A"

    print("\n" + "-" * 50)
    print("  ESTADISTICAS DE LA CONVERSACION")
    print("-" * 50)
    print(f"  Total de mensajes:     {total_mensajes}")
    print(f"  Mensajes tuyos:        {user_mensajes}")
    print(f"  Respuestas del bot:    {bot_mensajes}")
    print(f"  Tus palabras totales:  {total_words_user}")
    print(f"  Palabras del bot:      {total_words_bot}")
    print(f"  Tema mas frecuente:    {top_topic}")
    print(f"  Tokens aproximados:    {count_tokens(str(history))}")
    print("-" * 50 + "\n")


def chat():
    print("\n" + "=" * 50)
    print(f"  {APP_NAME}")
    print(f"  Version {VERSION}")
    print("=" * 50)
    print("  Escribe 'ayuda' para ver comandos")
    print("  Escribe 'salir' para terminar")
    print("-" * 50)

    client = create_client()
    if client:
        print("  [OK] Modo: OpenAI API")
        print(f"  Modelo: {MODEL_NAME}")
    else:
        print("  [!] Modo: Local (sin API key)")
        print("  Las respuestas usan base de conocimiento local")
    print("-" * 50)

    history = load_history() if SAVE_HISTORY else []
    use_api = client is not None

    while True:
        try:
            user_input = input("\nTu: ")
            if not validate_input(user_input):
                print("Chatbot: Por favor escribe algo.")
                continue

            user_input = clean_text(user_input)

            if is_exit_command(user_input):
                if SAVE_HISTORY:
                    save_history(history)
                print("\nChatbot: Gracias por conversar! Hasta luego.\n")
                break

            if is_help_command(user_input):
                show_help()
                continue

            if is_stats_command(user_input):
                show_stats(history)
                continue

            if is_clear_command(user_input):
                history.clear()
                print("\nHistorial limpiado.\n")
                continue

            if use_api:
                try:
                    messages = build_messages(user_input, history)
                    response = ask_openai(client, messages)
                except Exception as e:
                    print(f"\n[!] Error con OpenAI: {e}")
                    print("[!] Cambiando a modo local...\n")
                    use_api = False
                    response = get_local_response(user_input)
            else:
                response = get_local_response(user_input)

            response = format_response(response)
            print(f"Chatbot: {response}")

            history.append({"role": "user", "user": user_input, "assistant": response})
            if len(history) > MAX_HISTORY:
                history.pop(0)

        except KeyboardInterrupt:
            if SAVE_HISTORY:
                save_history(history)
            print("\n\nChatbot: Conversacion terminada. Hasta luego!\n")
            break
        except EOFError:
            print("\n")
            break
        except Exception as e:
            print(f"\n[!] Error inesperado: {e}")
            print("[!] Continuando en modo local...\n")
            use_api = False
            client = None


if __name__ == "__main__":
    chat()
