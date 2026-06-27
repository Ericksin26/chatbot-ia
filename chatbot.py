from openai import OpenAI
from functions import (
    validate_input, clean_text, format_response,
    is_exit_command, is_help_command, is_stats_command, is_clear_command,
    is_greeting, is_farewell, contains_question, detect_topic,
    is_weather_query, is_time_query, is_date_query,
    is_joke_query, is_calculator_query, is_riddle_query,
    contains_number,
    split_conversation, count_words, count_tokens,
    save_history, load_history
)
from config import (
    OPENAI_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE, SYSTEM_PROMPT,
    SAVE_HISTORY, MAX_HISTORY, APP_NAME, VERSION
)
from datetime import datetime
import random
import re


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


def get_current_time():
    now = datetime.now()
    return f"Son las {now.hour}:{now.minute:02d} (hora local)."


def get_current_date():
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    now = datetime.now()
    dia_semana = dias[now.weekday()]
    dia = now.day
    mes = meses[now.month - 1]
    año = now.year
    return f"Hoy es {dia_semana}, {dia} de {mes} de {año}."


def get_weather():
    import random
    now = datetime.now()
    random.seed(now.day + now.month + now.year)

    condiciones = [
        "Soleado con algunas nubes",
        "Parcialmente nublado",
        "Mayormente soleado",
        "Nublado con posibilidad de lluvia",
        "Despejado y fresco",
        "Lluvia ligera",
        "Tormentas electricas dispersas",
        "Ventoso y nublado",
        "Niebla matutina luego sol",
        "Cielo completamente despejado",
    ]
    temp_base = random.randint(18, 32)
    humedad = random.randint(45, 90)
    viento = random.randint(5, 25)
    condicion = random.choice(condiciones)

    return (
        f"Clima de hoy ({now.day}/{now.month}/{now.year}):\n"
        f"  Condicion: {condicion}\n"
        f"  Temperatura: {temp_base}°C\n"
        f"  Humedad: {humedad}%\n"
        f"  Viento: {viento} km/h\n"
        f"  Recomendacion: {'Lleva paraguas' if 'lluvia' in condicion.lower() or 'tormenta' in condicion.lower() else 'Disfruta el dia'}"
    )


def get_joke():
    chistes = [
        "¿Que le dice un pez a otro pez? \n- Nada.",
        "¿Como se despiden los quimicos? \n- Acidamente.",
        "¿Que hace una abeja en el gimnasio? \n- Zumba.",
        "¿Por que los programadores confunden Halloween con Navidad? \n- Porque Oct 31 == Dec 25.",
        "¿Que le dice un jardinero a otro? \n- Disfruta de las plantas.",
        "Habia una vez un pastor que tenia 30 ovejas. Un dia se cayo una y solo le quedaron 29. ¿Como se llamaba el pastor? \n- ¡Pastor!",
        "¿Que le dice un semaforo a otro? \n- No me mires, me estoy cambiando.",
        "Llega un hombre a un restaurante y dice: \n- Quiero una pizza. \nEl mesero dice: \n- ¿Entera o en partes? \nEl hombre responde: \n- Entera, no soy Partidario.",
        "¿Que hace un perro con un taladro? \n- Taladrando.",
        "¿Cual es el animal mas antiguo? \n- La cebra, porque esta en blanco y negro.",
        "¿Que le dice un 0 a un 8? \n- Bonito cinturon.",
        "¿Como se dice 'policia' en chino? \n- Ching-chong-ley.",
        "Si tienes 10 manzanas en una mano y 15 en la otra, ¿que tienes? \n- Manos grandes.",
        "¿Que hace una computadora en el campo? \n- Byte.",
        "¿Cual es el colmo de un programador? \n- Tener un hijo y llamarle 'Cursor'.",
    ]
    return random.choice(chistes)


def calculate(expr: str):
    expr = expr.lower()
    expr = expr.replace("por", "*").replace("x", "*").replace("por", "*")
    expr = expr.replace("mas", "+").replace("más", "+").replace("suma", "+")
    expr = expr.replace("menos", "-").replace("resta", "-")
    expr = expr.replace("dividido", "/").replace("entre", "/").replace("division", "/").replace("división", "/")
    expr = re.sub(r'[^0-9+\-*/().% ]', '', expr)
    expr = expr.strip()

    if not expr:
        return None

    try:
        result = eval(expr, {"__builtins__": {}}, {"abs": abs, "round": round, "float": float, "int": int})
        if isinstance(result, (int, float)):
            if result == int(result):
                result = int(result)
            return f"Resultado: {result}"
    except:
        return None
    return None


def get_riddle():
    adivinanzas = [
        {
            "pregunta": "Blanco por dentro, verde por fuera. Si quieres que te lo diga, espera. ¿Que soy?",
            "respuesta": "La pera"
        },
        {
            "pregunta": "Tengo agujas pero no sé coser, tengo números pero no sé leer. ¿Que soy?",
            "respuesta": "El reloj"
        },
        {
            "pregunta": "Mientras mas lavo, mas sucia me vuelvo. ¿Que soy?",
            "respuesta": "El agua"
        },
        {
            "pregunta": "Todos me llevan, todos me tienen, pocos me nombran. ¿Que soy?",
            "respuesta": "El nombre"
        },
        {
            "pregunta": "Si me das de comer, vivo; si me das de beber, muero. ¿Que soy?",
            "respuesta": "El fuego"
        },
        {
            "pregunta": "Cuanto mas quitas, mas grande se vuelve. ¿Que soy?",
            "respuesta": "El hoyo / El agujero"
        },
        {
            "pregunta": "Vuelo sin alas, lloro sin ojos. ¿Que soy?",
            "respuesta": "La nube"
        },
        {
            "pregunta": "Tengo llaves pero no abro puertas. ¿Que soy?",
            "respuesta": "El piano"
        },
        {
            "pregunta": "Puedo llenar una habitacion sin ocupar espacio. ¿Que soy?",
            "respuesta": "La luz"
        },
        {
            "pregunta": "Corro sin pies, y si me detienes, muero. ¿Que soy?",
            "respuesta": "El tiempo / El rio"
        },
        {
            "pregunta": "Cuando me nombras, desaparezco. ¿Que soy?",
            "respuesta": "El silencio"
        },
        {
            "pregunta": "Tiene cabeza y cola pero no tiene cuerpo. ¿Que es?",
            "respuesta": "La moneda"
        },
    ]
    return random.choice(adivinanzas)


def handle_riddle(user_input, riddle_state):
    user_input = user_input.lower().strip()

    if riddle_state.get("activa") and riddle_state.get("esperando_respuesta"):
        respuesta_correcta = riddle_state["respuesta"].lower()
        if user_input == respuesta_correcta or user_input in respuesta_correcta or respuesta_correcta in user_input:
            riddle_state["activa"] = False
            riddle_state["esperando_respuesta"] = False
            return f"¡Correcto! Muy bien. La respuesta era: {riddle_state['respuesta']}. ¿Quieres otra adivinanza?"
        elif "no se" in user_input or "no sé" in user_input or "rind" in user_input or "otra" in user_input:
            riddle_state["activa"] = False
            riddle_state["esperando_respuesta"] = False
            return f"La respuesta era: {riddle_state['respuesta']}. ¿Quieres intentar con otra?"
        else:
            return f"No es esa. Sigue intentando. Pista: {riddle_state.get('pista', 'usa tu ingenio')}. ¿O te rindes?"

    if is_riddle_query(user_input):
        riddle = get_riddle()
        riddle_state["activa"] = True
        riddle_state["esperando_respuesta"] = True
        riddle_state["respuesta"] = riddle["respuesta"]
        riddle_state["pista"] = riddle["respuesta"][:3] + "..."
        return f"Adivinanza: {riddle['pregunta']}\n¿Cual es tu respuesta?"

    return None


def get_local_response(user_input: str, riddle_state: dict = None):
    user_input = user_input.lower()
    topic = detect_topic(user_input)

    if riddle_state and riddle_state.get("activa") and riddle_state.get("esperando_respuesta"):
        result = handle_riddle(user_input, riddle_state)
        if result:
            return result

    saludos = {
        "hola": "¡Hola! ¿En qué puedo ayudarte hoy? Puedes preguntarme sobre Python, IA, programación, matemáticas, o pedirme la hora, el clima, chistes, adivinanzas y más.",
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

    if is_time_query(user_input):
        return get_current_time()

    if is_date_query(user_input):
        return get_current_date()

    if is_weather_query(user_input):
        return get_weather()

    if is_joke_query(user_input):
        return "Aquí va un chiste:\n" + get_joke()

    if is_calculator_query(user_input) or contains_number(user_input):
        result = calculate(user_input)
        if result:
            return result

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
        return "Funciono usando inteligencia artificial. Puedo responder preguntas usando una API de OpenAI (si está configurada) o con respuestas predefinidas en modo local. Tambien se la hora, fecha, clima, chistes, calculo matematico y adivinanzas."

    if "quien te creo" in user_input or "quién te creó" in user_input or "quien te hizo" in user_input:
        return "Fui creado como parte de un proyecto academico (Parcial 3) para aprender sobre Python, funciones e inteligencia artificial. Mi codigo esta en GitHub: https://github.com/Ericksin26/chatbot-ia"

    if "que puedes hacer" in user_input or "qué puedes hacer" in user_input:
        return "Puedo conversar contigo, responder preguntas sobre Python, IA, datos, web y matematicas. Tambien te digo la hora, la fecha, el clima, te cuento chistes, hago calculos matematicos y te pongo adivinanzas. Pide ayuda para ver todo."

    python_responses = [
        "Python es un lenguaje de programacion interpretado, de alto nivel y multiplataforma. Creado por Guido van Rossum en 1991. Usado en IA, ciencia de datos, desarrollo web y automatizacion.",
        "Python se destaca por su sintaxis clara y legible. Tiene una gran comunidad y librerias como NumPy, Pandas, TensorFlow y Django.",
        "En Python puedes hacer desde scripts simples hasta aplicaciones complejas. Es el lenguaje mas popular para IA y machine learning.",
        "Python usa indentacion para definir bloques de codigo, lo que obliga a escribir codigo limpio y bien estructurado.",
    ]

    ia_responses = [
        "La IA es una rama de la informatica que crea sistemas capaces de realizar tareas que requieren inteligencia humana: reconocimiento de voz, toma de decisiones y traduccion.",
        "Tipos de IA: Debil (tareas especificas) y Fuerte (razonamiento general). Hoy usamos principalmente IA Debil en Siri, Alexa y chatbots.",
        "Machine Learning: subrama donde las maquinas aprenden de datos sin ser programadas explicitamente. Se divide en supervisado, no supervisado y por refuerzo.",
        "Deep Learning: redes neuronales con muchas capas. Tecnologia detras de autos autonomos, reconocimiento facial y ChatGPT.",
    ]

    datos_responses = [
        "Ciencia de datos: combina estadistica, programacion y conocimiento del dominio para extraer informacion valiosa de datos.",
        "Librerias principales: NumPy (numerico), Pandas (manipulacion), Matplotlib (visualizacion) y Scikit-learn (machine learning).",
        "Pasos del analisis de datos: 1) Recoleccion, 2) Limpieza, 3) Exploracion, 4) Modelado, 5) Interpretacion.",
    ]

    web_responses = [
        "Desarrollo web: frontend (lo que ve el usuario) y backend (logica del servidor). Python es popular para backend con Django y Flask.",
        "Django: framework MTV con ORM, autenticacion y panel de administracion incluido.",
        "Flask: micro-framework ligero y flexible para APIs REST y aplicaciones medianas.",
    ]

    mates_responses = [
        "Matematicas fundamentales en programacion e IA: algebra lineal, calculo, probabilidad y estadistica.",
        "Algebra lineal: esencial para redes neuronales. Datos como vectores y matrices.",
    ]

    general_responses = [
        "Interesante pregunta. ¿Podrias darme mas detalles para ayudarte mejor?",
        "Entiendo. Dame mas contexto para darte una respuesta mas precisa.",
        "Puedo ayudarte con programacion, IA, matematicas, tecnologia, clima, hora, chistes y adivinanzas.",
        "Estoy aqui para ayudarte. Preguntame lo que necesites!",
    ]

    if topic == "python":
        return python_responses[len(user_input) % len(python_responses)]

    if topic == "ia":
        return ia_responses[len(user_input) % len(ia_responses)]

    if topic == "datos":
        return datos_responses[len(user_input) % len(datos_responses)]

    if topic == "web":
        return web_responses[len(user_input) % len(web_responses)]

    if topic == "matematicas":
        return mates_responses[len(user_input) % len(mates_responses)]

    if contains_question(user_input):
        return general_responses[len(user_input) % len(general_responses)]

    return random.choice(general_responses)


def show_help():
    print("\n" + "-" * 50)
    print("  COMANDOS DISPONIBLES")
    print("-" * 50)
    print("  ayuda / help      - Muestra esta ayuda")
    print("  salir / exit      - Termina la conversacion")
    print("  stats             - Ver estadisticas")
    print("  clear             - Limpiar historial")
    print("-" * 50)
    print("  FUNCIONES ESPECIALES:")
    print("  clima             - Clima simulado del dia")
    print("  hora              - Hora actual")
    print("  fecha             - Fecha actual")
    print("  chiste            - Un chiste aleatorio")
    print("  calculadora       - Ej: 'cuanto es 25 * 4'")
    print("  adivinanza        - Adivinanza interactiva")
    print("-" * 50)
    print("  TEMAS DE CONOCIMIENTO:")
    print("  Python / IA / Datos / Web / Matematicas")
    print("-" * 50 + "\n")


def show_stats(history: list):
    if not history:
        print("\n  Aun no hay mensajes en esta sesion.")
        return

    total_mensajes = len(history)
    total_words_user = sum(count_words(h["user"]) for h in history)
    total_words_bot = sum(count_words(h["assistant"]) for h in history)
    topics = [detect_topic(h["user"]) for h in history]
    top_topic = max(set(topics), key=topics.count) if topics else "N/A"

    print("\n" + "-" * 50)
    print("  ESTADISTICAS DE LA CONVERSACION")
    print("-" * 50)
    print(f"  Total de mensajes:     {total_mensajes}")
    print(f"  Tus palabras totales:  {total_words_user}")
    print(f"  Palabras del bot:      {total_words_bot}")
    print(f"  Tema mas frecuente:    {top_topic}")
    print(f"  Tokens aproximados:    {count_tokens(str(history))}")
    print("-" * 50 + "\n")


def chat():
    print("\n" + "=" * 50)
    print(f"  {APP_NAME} v{VERSION}")
    print("=" * 50)
    print("  Escribe 'ayuda' para ver comandos")
    print("  Escribe 'salir' para terminar")
    print("-" * 50)

    client = create_client()
    if client:
        print("  [OK] Modo: OpenAI API - " + MODEL_NAME)
    else:
        print("  [!] Modo: Local (sin API key)")
        print("  ️  Clima | Hora | Fecha | Chistes | Calculos | Adivinanzas")
    print("-" * 50)

    history = load_history() if SAVE_HISTORY else []
    use_api = client is not None
    riddle_state = {"activa": False, "esperando_respuesta": False, "respuesta": "", "pista": ""}

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
                riddle_state = {"activa": False, "esperando_respuesta": False, "respuesta": "", "pista": ""}
                print("\n Historial y estado de adivinanza limpiados.\n")
                continue

            if use_api:
                try:
                    messages = build_messages(user_input, history)
                    response = ask_openai(client, messages)
                except Exception as e:
                    print(f"\n[!] Error con OpenAI: {e}")
                    print("[!] Cambiando a modo local...\n")
                    use_api = False
                    response = get_local_response(user_input, riddle_state)
            else:
                response = get_local_response(user_input, riddle_state)

            response = format_response(response)
            print(f"Chatbot: {response}")

            history.append({"user": user_input, "assistant": response})
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
