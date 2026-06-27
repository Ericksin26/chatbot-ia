from openai import OpenAI
from functions import (
    validate_input, clean_text, format_response,
    is_exit_command, is_help_command, is_stats_command, is_clear_command,
    is_greeting, is_farewell, contains_question, detect_topic,
    is_weather_query, is_time_query, is_date_query,
    is_joke_query, is_calculator_query, is_riddle_query,
    contains_number, detect_city,
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
    return f"En este momento son las {now.hour}:{now.minute:02d}."


def get_current_date():
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    now = datetime.now()
    return f"Hoy estamos a {dias[now.weekday()]}, {now.day} de {meses[now.month - 1]} de {now.year}."


def get_weather(city: str = None):
    now = datetime.now()
    random.seed(now.day + now.month + now.year)

    climas = {
        "panama": {
            "nombre": "Panama",
            "temp_min": 24, "temp_max": 32,
            "hum_min": 75, "hum_max": 95,
            "desc": [
                "calor humedo con sol y nubes",
                "dia tipico panameno, caluroso y humedo",
                "sol intenso con brisa del Pacifico",
                "calor tropical, nubes pasajeras",
                "cielo nublado con bochorno",
                "lluvia ligera y calor tipico",
                "soleado con alta sensacion termica",
                "nubes y claros, temperatura alta",
            ],
            "extra": "Clima tropical, tipico de Panama. Siempre es buena idea llevar agua."
        },
        "bogota": {"nombre": "Bogota", "temp_min": 7, "temp_max": 18, "hum_min": 60, "hum_max": 85, "desc": ["frio bogotano con neblina", "dia nublado tipico", "llovizna y ambiente frio", "niebla matutina y tarde fria"], "extra": "Clima frio de altura, lleva chaqueta."},
        "medellin": {"nombre": "Medellin", "temp_min": 16, "temp_max": 26, "hum_min": 55, "hum_max": 80, "desc": ["primavera todo el ano", "dia templado y agradable", "soleado con brisa fresca"], "extra": "Ciudad de la eterna primavera."},
        "caracas": {"nombre": "Caracas", "temp_min": 18, "temp_max": 28, "hum_min": 60, "hum_max": 85, "desc": ["calor de valle con nubes", "dia caluroso tipico caraqueno", "sol y nubes alternados"], "extra": "Clima primaveral de montana cerca del mar."},
        "lima": {"nombre": "Lima", "temp_min": 14, "temp_max": 24, "hum_min": 75, "hum_max": 95, "desc": ["garua limena y cielo gris", "nublado con alta humedad", "cielo cubierto tipico de Lima"], "extra": "Lima y su cielo nublado la mayor parte del ano."},
        "buenos aires": {"nombre": "Buenos Aires", "temp_min": 10, "temp_max": 28, "hum_min": 55, "hum_max": 85, "desc": ["dia templado en Buenos Aires", "soleado con brisa del rio", "nubes variables tipicas"], "extra": "Clima templado, tipico del Rio de la Plata."},
        "mexico": {"nombre": "Ciudad de Mexico", "temp_min": 10, "temp_max": 24, "hum_min": 40, "hum_max": 70, "desc": ["dia fresco en el valle", "soleado con aire limpio", "nubes y sol tipico del altiplano"], "extra": "Clima de alta montana, fresco la mayor parte del ano."},
        "madrid": {"nombre": "Madrid", "temp_min": 4, "temp_max": 30, "hum_min": 30, "hum_max": 65, "desc": ["dia soleado en Madrid", "cielo despejado", "frio por la manana, calor al mediodia"], "extra": "Continental mediterraneo, inviernos frios y veranos calurosos."},
        "santiago": {"nombre": "Santiago", "temp_min": 6, "temp_max": 28, "hum_min": 30, "hum_max": 65, "desc": ["dia despejado en Santiago", "cielo azul tipico", "nubes altas durante la tarde"], "extra": "Clima mediterraneo con estaciones marcadas."},
    }

    if city and city in climas:
        c = climas[city]
        temp = random.randint(c["temp_min"], c["temp_max"])
        hum = random.randint(c["hum_min"], c["hum_max"])
        wind = random.randint(5, 20)
        desc = random.choice(c["desc"])
        extra = c["extra"]
        return (
            f"Clima en {c['nombre']}: {desc}. "
            f"Temperatura alrededor de {temp}°C, {hum}% de humedad, viento de {wind} km/h. "
            f"{extra}"
        )

    pair = random.randint(0, 9)
    desc = [
        "dia soleado con algunas nubes",
        "jornada parcialmente nublada",
        "mayormente soleado",
        "nublado, pero sin lluvia por ahora",
        "dia fresco y despejado",
        "lluvia ligera de vez en cuando",
        "posibles tormentas electricas",
        "dia ventoso y nublado",
        "niebla en la manana, luego mejora",
        "cielo completamente despejado",
    ][pair]
    temp = random.randint(18, 32)
    hum = random.randint(45, 90)
    wind = random.randint(5, 25)

    extra = ""
    if "lluv" in desc or "torment" in desc:
        extra = "Mejor llevar paraguas por si acaso."
    elif temp > 28:
        extra = "Va a hacer calor, viste fresco."
    elif temp < 22:
        extra = "Temperatura agradable, buen dia para salir."

    return (
        f"Hoy tenemos un {desc}. "
        f"Temperatura de {temp}°C, {hum}% de humedad, viento de {wind} km/h. "
        f"{extra}"
    )


def get_joke():
    chistes = [
        "¿Que le dice un pez a otro pez? Nada.",
        "¿Como se despiden los quimicos? Acidamente.",
        "¿Que hace una abeja en el gimnasio? Zumba.",
        "Habia una vez un pastor con 30 ovejas. Se cayo una y quedaron 29. ¿Como se llamaba el pastor? Pasto... no, se llamaba Pastor.",
        "¿Que le dice un semaforo a otro? No me mires, me estoy cambiando.",
        "Un hombre pide una pizza y el mesero pregunta si la quiere entera o en partes. El hombre dice: entera, no soy partidario.",
        "¿Cual es el animal mas antiguo? La cebra, porque esta en blanco y negro.",
        "¿Que le dice un 0 a un 8? Bonito cinturon.",
        "Si tienes 10 manzanas en una mano y 15 en la otra, ¿que tienes? Manos grandes.",
        "¿Que hace una computadora en el campo? Byte.",
        "¿Cual es el colmo de un programador? Tener un hijo y llamarle Cursor.",
        "Llega una mama y le dice a su hijo: hijo, hoy te portaste mal en la escuela. El hijo responde: mama, hoy no fui a la escuela. La mama dice: no importa, igual te portaste mal.",
    ]
    return random.choice(chistes)


def calculate(expr: str):
    expr = expr.lower()
    expr = expr.replace("por", "*").replace("x", "*")
    expr = expr.replace("mas", "+").replace("más", "+")
    expr = expr.replace("menos", "-").replace("resta", "-")
    expr = expr.replace("dividido", "/").replace("entre", "/")
    expr = re.sub(r'[^0-9+\-*/().% ]', '', expr).strip()

    if not expr:
        return None

    try:
        result = eval(expr, {"__builtins__": {}}, {})
        if isinstance(result, float):
            if result == int(result):
                result = int(result)
        return f"El resultado es {result}."
    except:
        return None


def get_riddle():
    items = [
        ("Blanco por dentro, verde por fuera. Si quieres que te lo diga, espera. ¿Que soy?", "La pera", "pera"),
        ("Tengo agujas pero no se coser, tengo numeros pero no se leer. ¿Que soy?", "El reloj", "reloj"),
        ("Mientras mas lavo, mas sucia me vuelvo. ¿Que soy?", "El agua", "agua"),
        ("Todos me llevan, todos me tienen, pocos me nombran. ¿Que soy?", "El nombre", "nombre"),
        ("Si me das de comer vivo, si me das de beber muero. ¿Que soy?", "El fuego", "fuego"),
        ("Cuanto mas quitas, mas grande se vuelve. ¿Que soy?", "El hoyo", "hoyo"),
        ("Vuelo sin alas, lloro sin ojos. ¿Que soy?", "La nube", "nube"),
        ("Tengo llaves pero no abro puertas. ¿Que soy?", "El piano", "piano"),
        ("Puedo llenar una habitacion sin ocupar espacio. ¿Que soy?", "La luz", "luz"),
        ("Corro sin pies, y si me detienes muero. ¿Que soy?", "El rio", "rio"),
        ("Cuando me nombras desaparezco. ¿Que soy?", "El silencio", "silencio"),
        ("Tiene cabeza y cola pero no tiene cuerpo. ¿Que es?", "La moneda", "moneda"),
    ]
    pregunta, respuesta, pista = random.choice(items)
    return {"pregunta": pregunta, "respuesta": respuesta, "pista": pista}


def handle_riddle(user_input, state):
    user_input = user_input.lower().strip()

    if state.get("activa") and state.get("esperando"):
        correcta = state["respuesta"].lower()
        if user_input == correcta or user_input in correcta or correcta in user_input:
            state["activa"] = False
            state["esperando"] = False
            return f"¡Correcto! Era {state['respuesta']}. ¿Quieres otra?"
        elif any(w in user_input for w in ["no se", "no sé", "rindo", "rinde", "otra"]):
            state["activa"] = False
            state["esperando"] = False
            return f"Era {state['respuesta']}. ¿Intentamos con otra?"
        else:
            return f"No, no es esa. Una pista: empieza con '{state['pista'][0]}'. ¿O te rindes?"

    if is_riddle_query(user_input):
        r = get_riddle()
        state["activa"] = True
        state["esperando"] = True
        state["respuesta"] = r["respuesta"]
        state["pista"] = r["pista"]
        return f"A ver si adivinas: {r['pregunta']}"

    return None


def get_local_response(user_input: str, riddle_state: dict = None):
    user_input = user_input.lower()
    topic = detect_topic(user_input)

    if riddle_state and riddle_state.get("activa") and riddle_state.get("esperando"):
        result = handle_riddle(user_input, riddle_state)
        if result:
            return result

    if is_time_query(user_input):
        return get_current_time()

    if is_date_query(user_input):
        return get_current_date()

    if is_weather_query(user_input):
        city = detect_city(user_input)
        return get_weather(city)

    if is_joke_query(user_input):
        return get_joke()

    if is_calculator_query(user_input) or contains_number(user_input):
        r = calculate(user_input)
        if r:
            return r

    if is_greeting(user_input):
        if "buenos dias" in user_input or "buen dia" in user_input:
            return "¡Buenos dias! ¿En que puedo ayudarte hoy?"
        if "buenas tardes" in user_input:
            return "¡Buenas tardes! ¿Como va todo?"
        if "buenas noches" in user_input:
            return "¡Buenas noches! ¿Necesitas algo antes de dormir?"
        return "¡Hola! ¿Que necesitas? Puedo ayudarte con programacion, darte la hora, el clima, contarte un chiste o lo que sea."

    if is_farewell(user_input):
        return "¡Hasta luego! Cuando quieras vuelve a escribir."

    if "gracias" in user_input:
        return "De nada, para eso estoy."

    if "como funciona" in user_input:
        return "En terminos simples: si tienes configurada una API key de OpenAI, hablo con GPT. Si no, uso una base de respuestas que tengo guardada sobre programacion, IA, matematicas, clima y otras cosas."

    if "quien te creo" in user_input or "quien te hizo" in user_input:
        return "Me hicieron como proyecto universitario (Parcial 3) para practicar Python, funciones y conceptos de IA. El codigo esta en github.com/Ericksin26/chatbot-ia"

    if "que puedes hacer" in user_input:
        return "Preguntame la hora, la fecha, el clima, un chiste, una adivinanza, o dime una operacion como 'cuanto es 15 * 3'. Tambien se de Python, IA, datos y matematicas."

    if topic == "python":
        temas = [
            "Python lo creo Guido van Rossum en 1991. Es un lenguaje interpretado y multiplataforma que se usa mucho en IA, ciencia de datos y web.",
            "Una de las ventajas de Python es que su sintaxis es muy limpia y facil de leer. Por eso es tan popular entre principiantes y profesionales.",
            "Python tiene librerias para todo: NumPy y Pandas para datos, Django y Flask para web, TensorFlow y PyTorch para machine learning.",
            "A diferencia de otros lenguajes, Python usa indentacion en vez de llaves para definir bloques de codigo. Al principio puede sonar raro, pero ayuda a escribir codigo ordenado.",
        ]
        return temas[len(user_input) % len(temas)]

    if topic == "ia":
        temas = [
            "La inteligencia artificial basicamente busca que las maquinas hagan cosas que normalmente requieren inteligencia humana, como reconocer voz, tomar decisiones o traducir idiomas.",
            "Hay dos tipos de IA: la debil, que hace tareas especificas (como Siri o los chatbots), y la fuerte, que seria una maquina con razonamiento general (todavia no existe).",
            "El machine learning es una rama de la IA donde la maquina aprende de datos en vez de ser programada paso a paso. Hay aprendizaje supervisado, no supervisado y por refuerzo.",
            "El deep learning usa redes neuronales con muchas capas. Es lo que hay detras de los autos autonomos, el reconocimiento facial y ChatGPT.",
        ]
        return temas[len(user_input) % len(temas)]

    if topic == "datos":
        temas = [
            "La ciencia de datos mezcla estadistica, programacion y conocimiento del negocio para sacar informacion util de los datos.",
            "Las librerias mas usadas en Python para datos son NumPy (numeros), Pandas (tablas), Matplotlib (graficas) y Scikit-learn (machine learning).",
            "El analisis de datos suele seguir estos pasos: recoleccion, limpieza, exploracion, modelado e interpretacion.",
        ]
        return temas[len(user_input) % len(temas)]

    if topic == "web":
        temas = [
            "En desarrollo web hay dos partes: frontend (lo que ves) y backend (la logica detras). Python se usa mucho en backend con Django o Flask.",
            "Django es un framework completo que ya trae ORM, autenticacion y panel de administracion. Flask es mas minimalista y flexible.",
        ]
        return temas[len(user_input) % len(temas)]

    if topic == "matematicas":
        temas = [
            "Las matematicas son la base de la programacion y la IA. Sobre todo el algebra lineal, el calculo, la probabilidad y la estadistica.",
            "El algebra lineal es clave para entender redes neuronales. Los datos se representan como vectores y matrices, y las operaciones entre ellos son el corazon del deep learning.",
        ]
        return temas[len(user_input) % len(temas)]

    if contains_question(user_input):
        return "No estoy seguro de entender tu pregunta. Puedo ayudarte con programacion, IA, clima, hora, chistes o calculos. Intenta ser mas especifico."

    return random.choice([
        "No entendi muy bien, pero puedes pedirme la hora, el clima, un chiste, una adivinanza o preguntarme sobre programacion.",
        "Si no sabes que preguntar, escribe 'ayuda' para ver todo lo que puedo hacer.",
        "No estoy seguro de que decir. Prueba con 'clima', 'hora', 'chiste' o preguntame sobre Python o IA.",
    ])


def show_help():
    print()
    print("-" * 50)
    print("  COSAS QUE PUEDES PREGUNTAR")
    print("-" * 50)
    print("  ayuda            - Ver esto")
    print("  salir            - Terminar")
    print("  stats            - Ver estadisticas")
    print("  clear            - Limpiar historial")
    print()
    print("  hora             - Que hora es")
    print("  fecha            - Que dia es hoy")
    print("  clima            - Clima de tu ciudad")
    print("  clima Panama     - Clima de una ciudad")
    print("  chiste           - Escuchar un chiste")
    print("  adivinanza       - Jugar a adivinar")
    print("  calculadora      - Ej: 'cuanto es 25 * 4'")
    print()
    print("  TEMAS:")
    print("  Python, IA, Datos, Web, Matematicas")
    print("-" * 50)
    print()


def show_stats(history: list):
    if not history:
        print("\n  No hay mensajes guardados.\n")
        return

    total = len(history)
    words_user = sum(count_words(h["user"]) for h in history)
    words_bot = sum(count_words(h["assistant"]) for h in history)
    topics = [detect_topic(h["user"]) for h in history]
    top_topic = max(set(topics), key=topics.count) if topics else "N/A"

    print()
    print("-" * 50)
    print("  ESTADISTICAS")
    print("-" * 50)
    print(f"  Mensajes:        {total}")
    print(f"  Tus palabras:    {words_user}")
    print(f"  Mis palabras:    {words_bot}")
    print(f"  Tema frecuente:  {top_topic}")
    print("-" * 50)
    print()


def chat():
    print()
    print("=" * 50)
    print(f"  {APP_NAME} v{VERSION}")
    print("=" * 50)
    print("  Escribe 'ayuda' para empezar")
    print("  Escribe 'salir' para terminar")
    print("-" * 50)

    client = create_client()
    if client:
        print("  Con OpenAI conectado")
    else:
        print("  Modo local (sin API key)")
    print("-" * 50)

    history = load_history() if SAVE_HISTORY else []
    use_api = client is not None
    riddle_state = {"activa": False, "esperando": False, "respuesta": "", "pista": ""}

    while True:
        try:
            user_input = input("\nTu: ")
            if not validate_input(user_input):
                print("Chatbot: Escribe algo, estoy aqui.")
                continue

            user_input = clean_text(user_input)

            if is_exit_command(user_input):
                if SAVE_HISTORY:
                    save_history(history)
                print("\nChatbot: Hasta luego!\n")
                break

            if is_help_command(user_input):
                show_help()
                continue

            if is_stats_command(user_input):
                show_stats(history)
                continue

            if is_clear_command(user_input):
                history.clear()
                riddle_state = {"activa": False, "esperando": False, "respuesta": "", "pista": ""}
                print("Historial borrado.")
                continue

            if use_api:
                try:
                    messages = build_messages(user_input, history)
                    response = ask_openai(client, messages)
                except Exception as e:
                    print(f"Error con OpenAI: {e}. Cambio a modo local.")
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
            print("\n\nHasta luego!\n")
            break
        except EOFError:
            print()
            break
        except Exception as e:
            print(f"Error: {e}. Continuo en modo local.")
            use_api = False
            client = None


if __name__ == "__main__":
    chat()
