from openai import OpenAI
from functions import (
    validate_input, clean_text, format_response,
    is_exit_command, is_help_command, is_stats_command, is_clear_command,
    is_greeting, is_farewell, contains_question, detect_topic,
    is_weather_query, is_time_query, is_date_query,
    is_joke_query, is_calculator_query, is_riddle_query,
    is_curiosity_query, is_advice_query, is_motivation_query,
    is_coin_query, is_dice_query,
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
    return f"Son las {now.hour}:{now.minute:02d}"


def get_current_date():
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    now = datetime.now()
    return f"Hoy es {dias[now.weekday()]} {now.day} de {meses[now.month - 1]} de {now.year}"


def get_weather(city: str = None):
    now = datetime.now()
    random.seed(now.day + now.month + now.year)

    climas = {
        "panama": {
            "nombre": "Panama",
            "temp_min": 24, "temp_max": 32,
            "hum_min": 75, "hum_max": 95,
            "desc": [
                "calor humedo, sol y nubes",
                "caluroso y humedo como siempre",
                "sol intenso con brisa del Pacifico",
                "calor tropical, nubes pasando",
                "nublado con bochorno",
                "llovizna ligera y calor",
                "soleado, sensacion termica alta",
                "nubes y claros, calor tipico",
            ],
            "fin": ["Tipico clima de Panama.", "Panama tropical, ya sabes.", "Calor panameno de siempre."]
        },
        "bogota": {"nombre": "Bogota", "temp_min": 7, "temp_max": 18, "hum_min": 60, "hum_max": 85, "desc": ["frio con neblina", "nublado como siempre", "llovizna y ambiente frio", "niebla en la manana"], "fin": ["Frio bogotano, lleva chaqueta.", "Altura, hace frio."]},
        "medellin": {"nombre": "Medellin", "temp_min": 16, "temp_max": 26, "hum_min": 55, "hum_max": 80, "desc": ["templado y agradable", "soleado con brisa", "clima de eterna primavera"], "fin": ["Medellin siempre agradable.", "La eterna primavera."]},
        "caracas": {"nombre": "Caracas", "temp_min": 18, "temp_max": 28, "hum_min": 60, "hum_max": 85, "desc": ["calor de valle", "caluroso tipico", "sol y nubes"], "fin": ["Clima caraqueno de siempre.", "Calorcito de Caracas."]},
        "lima": {"nombre": "Lima", "temp_min": 14, "temp_max": 24, "hum_min": 75, "hum_max": 95, "desc": ["garua y cielo gris", "nublado con alta humedad", "cielo cubierto tipico"], "fin": ["Lima y su cielo gris.", "Tipico clima limeno."]},
        "buenos aires": {"nombre": "Buenos Aires", "temp_min": 10, "temp_max": 28, "hum_min": 55, "hum_max": 85, "desc": ["templado", "soleado con brisa del rio", "nubes variables"], "fin": ["Clima porteño tipico.", "Buenos Aires y su clima."]},
        "mexico": {"nombre": "Ciudad de Mexico", "temp_min": 10, "temp_max": 24, "hum_min": 40, "hum_max": 70, "desc": ["fresco en el valle", "soleado con aire limpio", "nubes y sol"], "fin": ["Clima de ciudad de Mexico.", "Fresco por la altura."]},
        "madrid": {"nombre": "Madrid", "temp_min": 4, "temp_max": 30, "hum_min": 30, "hum_max": 65, "desc": ["soleado", "cielo despejado", "frio en la manana, calor al mediodia"], "fin": ["Madrid tipico.", "Continental, estaciones marcadas."]},
        "santiago": {"nombre": "Santiago", "temp_min": 6, "temp_max": 28, "hum_min": 30, "hum_max": 65, "desc": ["despejado", "cielo azul", "nubes altas en la tarde"], "fin": ["Santiago y su cielo azul.", "Clima mediterraneo."]},
    }

    if city and city in climas:
        c = climas[city]
        temp = random.randint(c["temp_min"], c["temp_max"])
        hum = random.randint(c["hum_min"], c["hum_max"])
        wind = random.randint(5, 20)
        desc = random.choice(c["desc"])
        fin = random.choice(c["fin"])
        return f"En {c['nombre']} esta {desc}. Como {temp}°C, {hum}% de humedad, viento de {wind} km/h. {fin}"

    pair = random.randint(0, 9)
    desc = [
        "soleado con nubes",
        "parcialmente nublado",
        "mayormente soleado",
        "nublado pero sin lluvia",
        "fresco y despejado",
        "lluvia ligera de vez en cuando",
        "posibles tormentas",
        "ventoso y nublado",
        "niebla en la manana, luego mejora",
        "cielo despejado",
    ][pair]
    temp = random.randint(18, 32)
    hum = random.randint(45, 90)
    wind = random.randint(5, 25)

    extra = ""
    if "lluv" in desc or "torment" in desc:
        extra = "Lleva paraguas por si acaso."
    elif temp > 28:
        extra = "Va a hacer calor, viste fresco."
    elif temp < 22:
        extra = "Temperatura agradable."

    return f"Hoy tenemos {desc}. {temp}°C, {hum}% humedad, viento {wind} km/h. {extra}"


def get_joke():
    chistes = [
        "¿Que le dice un pez a otro pez? Nada.",
        "¿Como se despiden los quimicos? Acidamente.",
        "¿Que hace una abeja en el gimnasio? Zumba.",
        "Un pastor tenia 30 ovejas. Se cayo una y quedaron 29. ¿Como se llamaba el pastor? Se llamaba Pastor.",
        "¿Que le dice un semaforo a otro? No me mires, me estoy cambiando.",
        "Un hombre pide una pizza y le preguntan si la quiere entera o en partes. Dice: entera, no soy partidario.",
        "¿Cual es el animal mas antiguo? La cebra, porque esta en blanco y negro.",
        "¿Que le dice un 0 a un 8? Bonito cinturon.",
        "Si tienes 10 manzanas en una mano y 15 en la otra, ¿que tienes? Manos grandes.",
        "¿Que hace una computadora en el campo? Byte.",
        "El colmo de un programador: tener un hijo y llamarle Cursor.",
        "Llega una mama y le dice al hijo: hoy te portaste mal. El hijo: mama, hoy no fui a la escuela. La mama: no importa, igual te portaste mal.",
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
        return f"Da {result}"
    except:
        return None


def get_curiosity():
    datos = [
        "Los pulpos tienen tres corazones y sangre azul.",
        "Las hormigas nunca duermen. Literalmente.",
        "El ojo humano puede distinguir hasta 10 millones de colores.",
        "Banana no es la unica fruta que tiene pepitas. Todas las frutas las tienen.",
        "El corazón de un camarón esta en la cabeza.",
        "Los arboles se comunican entre si a traves de sus raices usando una red de hongos llamada 'wood wide web'.",
        "El 90% de los datos del mundo se generaron en los ultimos dos años.",
        "Un grupo de flamencos se llama 'flamenco', igual que el ave en singular.",
        "El primer programador de la historia fue una mujer: Ada Lovelace.",
        "El wifi fue inventado por accidente mientras buscaban algo completamente diferente.",
        "Python no se llama por la serpiente, sino por el grupo comico Monty Python.",
        "El aguacate es una fruta, no una verdura.",
        "La miel nunca se echa a perder. Se encontró miel comestible en tumbas egipcias de 3000 años.",
        "Los dinosaurios aun existen: son las aves.",
        "El nombre mas comun en el mundo es Mohammed.",
    ]
    return random.choice(datos)


def get_advice():
    consejos = [
        "Aprende a decir 'no' sin sentirte mal. Tu tiempo vale.",
        "Lee al menos 10 páginas al día. En un año son 10 libros.",
        "Si algo te toma menos de 2 minutos, hazlo ahora.",
        "No compares tu progreso con el de otros. Cada quien va a su ritmo.",
        "Duerme bien. No hay productividad que valga la pena sin descanso.",
        "Guarda plata aunque sea poquito. El habito es lo que importa.",
        "No le temas a equivocarte. Los errores son la forma mas rapida de aprender.",
        "Si no sabes algo, preguntalo. La unica pregunta tonta es la que no se hace.",
        "Aprende a cocinar al menos 3 platos. Te va a salvar la vida.",
        "Camina 15 minutos al dia. Hace mas de lo que crees.",
        "Organiza tu tiempo. La mayoria de la gente pierde 2 horas al dia sin darse cuenta.",
        "No respondas cuando estes enojado. Espera 5 minutos.",
    ]
    return random.choice(consejos)


def get_motivation():
    frases = [
        "No se trata de ser el mejor, sino de ser mejor que ayer.",
        "El exito es la suma de pequeños esfuerzos repetidos dia tras dia.",
        "No esperes a estar listo, empieza y ve aprendiendo en el camino.",
        "Si puedes soñarlo, puedes hacerlo. Pero tienes que empezar.",
        "El unico fracaso real es no intentarlo.",
        "Tu unico limite es tu mente. Todo lo demas es excusa.",
        "La disciplina vence a la motivación. Hazlo aunque no tengas ganas.",
        "Cada día es una nueva oportunidad. No importa lo que paso ayer.",
        "No subestimes el poder de avanzar un poco cada dia.",
        "Las grandes cosas nunca vienen de zonas de confort.",
        "El momento perfecto no existe. El mejor momento es ahora.",
        "Si nada cambia, nada cambia. Tu tienes el poder de empezar.",
    ]
    return random.choice(frases)


def flip_coin():
    return random.choice(["Cara", "Cruz"])


def roll_dice():
    return random.randint(1, 6)


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
            return f"¡Bien ahi! Era {state['respuesta']}. ¿Otra?"
        elif any(w in user_input for w in ["no se", "no sé", "rindo", "rinde", "otra"]):
            state["activa"] = False
            state["esperando"] = False
            return f"Era {state['respuesta']}. ¿Otra?"
        else:
            return f"No. La palabra empieza con '{state['pista'][0]}'. ¿Te rindes?"

    if is_riddle_query(user_input):
        r = get_riddle()
        state["activa"] = True
        state["esperando"] = True
        state["respuesta"] = r["respuesta"]
        state["pista"] = r["pista"]
        return f"Adivina: {r['pregunta']}"

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

    if is_curiosity_query(user_input):
        return f"Sabias que... {get_curiosity()}"

    if is_advice_query(user_input):
        return f"Un consejo: {get_advice()}"

    if is_motivation_query(user_input):
        return get_motivation()

    if is_coin_query(user_input):
        return f"Salio: {flip_coin()}"

    if is_dice_query(user_input):
        return f"El dado cayo en: {roll_dice()}"

    if "numero de la suerte" in user_input or "número de la suerte" in user_input:
        return f"Tu numero de la suerte hoy es: {random.randint(1, 100)}"

    if is_calculator_query(user_input) or contains_number(user_input):
        r = calculate(user_input)
        if r:
            return r

    if is_greeting(user_input):
        if "buenos dias" in user_input or "buen dia" in user_input:
            return "Buenos dias! ¿Que necesitas?"
        if "buenas tardes" in user_input:
            return "Buenas tardes! ¿Como vas?"
        if "buenas noches" in user_input:
            return "Buenas noches! ¿Algo antes de dormir?"
        return "Que tal! Preguntame la hora, el clima, un chiste, una curiosidad, o lo que sea."

    if is_farewell(user_input):
        return "Nos vemos, cuando quieras."

    if "gracias" in user_input:
        return "De nada, para eso estoy."

    if "como funciona" in user_input:
        return "Si tienes API key hablo con GPT, si no uso respuestas que tengo guardadas. Es simple."

    if "quien te creo" in user_input or "quien te hizo" in user_input:
        return "Me creo Baules, Erick. Es muy inteligente, capaz y unico, seguramente lograra muchas cosas."

    if "que puedes hacer" in user_input:
        return "Preguntame la hora, la fecha, el clima, un chiste, una adivinanza, una curiosidad, un consejo, o hazme una cuenta. Tambien puedo lanzar una moneda, tirar un dado o darte tu numero de la suerte."

    if topic == "python":
        temas = [
            "Python lo hizo Guido van Rossum en 1991. Se usa caleta en IA, datos y web.",
            "Lo bueno de Python es que se lee casi como ingles, por eso es tan popular.",
            "Tiene librerias para todo: NumPy, Pandas, Django, Flask, TensorFlow...",
            "Usa indentacion en vez de llaves. Al principio cuesta pero despues te acostumbras.",
        ]
        return temas[len(user_input) % len(temas)]

    if topic == "ia":
        temas = [
            "La IA basicamente es que las maquinas hagan cosas que requieren inteligencia humana: reconocer voz, decisiones, traduccion.",
            "Hay IA debil (Siri, chatbots) e IA fuerte (la de las peliculas, que aun no existe).",
            "Machine learning es cuando la maquina aprende sola de los datos. Hay tres tipos: supervisado, no supervisado y por refuerzo.",
            "Deep learning son redes neuronales con muchas capas. Es lo que usan los autos autonomos y ChatGPT.",
        ]
        return temas[len(user_input) % len(temas)]

    if topic == "datos":
        temas = [
            "Ciencia de datos es mezclar estadistica con programacion para sacar info util de los datos.",
            "Las librerias mas usadas: NumPy (numeros), Pandas (tablas), Matplotlib (graficas), Scikit-learn (machine learning).",
            "El analisis de datos va asi: recoleccion, limpieza, exploracion, modelado, interpretacion.",
        ]
        return temas[len(user_input) % len(temas)]

    if topic == "web":
        temas = [
            "El desarrollo web tiene frontend (lo que ves) y backend (la logica). Python se usa en backend con Django o Flask.",
            "Django ya trae de todo: ORM, autenticacion, panel admin. Flask es mas simple y flexible.",
        ]
        return temas[len(user_input) % len(temas)]

    if topic == "matematicas":
        temas = [
            "Las matematicas son la base de la programacion. Algebra lineal, calculo, probabilidad y estadistica sobre todo.",
            "El algebra lineal es clave para las redes neuronales. Los datos son vectores y matrices.",
        ]
        return temas[len(user_input) % len(temas)]

    if contains_question(user_input):
        return "No entendi bien la pregunta. Prueba con 'hora', 'clima', 'chiste', o preguntame sobre Python o IA."

    return random.choice([
        "No entendi, pero puedes pedirme la hora, el clima, un chiste o preguntar de programacion.",
        "Si no sabes que preguntar, pon 'ayuda' para ver las opciones.",
        "No se que decir. Prueba 'clima', 'hora', 'chiste' o pregunta sobre Python o IA.",
    ])


def show_help():
    print()
    print("-" * 50)
    print("  QUE PUEDES HACER")
    print("-" * 50)
    print("  ayuda            - Ver esto")
    print("  salir            - Terminar")
    print("  stats            - Estadisticas")
    print("  clear            - Borrar historial")
    print()
    print("  hora             - Que hora es")
    print("  fecha            - Que dia es")
    print("  clima            - Clima de tu ciudad")
    print("  clima Panama     - Clima de una ciudad")
    print("  chiste           - Un chiste")
    print("  adivinanza       - Jugar a adivinar")
    print("  calculadora      - Ej: cuanto es 25 * 4")
    print("  curiosidad       - Dato interesante")
    print("  consejo          - Un consejo util")
    print("  motivacion       - Frase motivadora")
    print("  cara o cruz      - Lanza una moneda")
    print("  dado             - Tira un dado")
    print("  numero suerte    - Tu numero de la suerte")
    print()
    print("  TEMAS:")
    print("  Python, IA, Datos, Web, Matematicas")
    print("-" * 50)
    print()


def show_stats(history: list):
    if not history:
        print("\n  No hay mensajes.\n")
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
    print(f"  Mensajes:       {total}")
    print(f"  Tus palabras:   {words_user}")
    print(f"  Mis palabras:   {words_bot}")
    print(f"  Tema comun:     {top_topic}")
    print("-" * 50)
    print()


def chat():
    print()
    print("=" * 50)
    print(f"  {APP_NAME} v{VERSION}")
    print("=" * 50)
    print("  Escribe 'ayuda' para ver opciones")
    print("  Escribe 'salir' para terminar")
    print("-" * 50)

    client = create_client()
    if client:
        print("  Con OpenAI conectado")
    else:
        print("  Modo local")
    print("-" * 50)

    history = load_history() if SAVE_HISTORY else []
    use_api = client is not None
    riddle_state = {"activa": False, "esperando": False, "respuesta": "", "pista": ""}

    while True:
        try:
            user_input = input("\nTu: ")
            if not validate_input(user_input):
                print("Chatbot: Escribe algo")
                continue

            user_input = clean_text(user_input)

            if is_exit_command(user_input):
                if SAVE_HISTORY:
                    save_history(history)
                print("\nChao!\n")
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
                    print(f"Error con OpenAI: {e}. Paso a modo local.")
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
            print("\n\nChao!\n")
            break
        except EOFError:
            print()
            break
        except Exception as e:
            print(f"Error: {e}. Continua modo local.")
            use_api = False
            client = None


if __name__ == "__main__":
    chat()
