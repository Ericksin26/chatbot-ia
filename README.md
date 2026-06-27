# Chatbot de IA - Parcial 3

Chatbot conversacional desarrollado en Python con modo OpenAI y modo local. Proyecto academico para aprender sobre funciones, APIs e inteligencia artificial.

## Estructura del proyecto

```
chatbot-ia/
├── main.py          # Punto de entrada con argumentos CLI
├── chatbot.py       # Logica del chatbot (OpenAI + modo local)
├── functions.py     # Funciones auxiliares y utilerias
├── config.py        # Configuracion via variables de entorno
├── historial.json   # Historial de conversacion (se genera automaticamente)
├── .env.example     # Template de configuracion
├── requirements.txt # Dependencias
└── README.md        # Documentacion
```

## Instalacion

```bash
git clone https://github.com/Ericksin26/chatbot-ia.git
cd chatbot-ia
pip install -r requirements.txt
```

### Configurar API key (opcional)

```bash
cp .env.example .env
```

Editar `.env` y agregar tu `OPENAI_API_KEY` de OpenAI.

## Uso

```bash
python main.py
```

### Opciones CLI

```bash
python main.py -h      # Ayuda
python main.py -v      # Version
```

### Comandos durante la conversacion

| Comando  | Descripcion |
|----------|------------|
| ayuda    | Muestra los comandos y temas disponibles |
| stats    | Muestra estadisticas de la conversacion |
| clear    | Limpia el historial de la sesion |
| salir    | Termina la conversacion |

### Temas que soporta

- Python (programacion, codigo, librerias)
- Inteligencia Artificial (IA, machine learning, deep learning)
- Ciencia de datos (analisis, NumPy, Pandas)
- Desarrollo web (Django, Flask, HTML)
- Matematicas (calculo, algebra)
- Conversacion general

## Caracteristicas

- **Modo OpenAI**: Respuestas inteligentes usando GPT-3.5/GPT-4
- **Modo Local**: Base de conocimiento local con +30 respuestas categorizadas
- **Deteccion de temas**: Identifica automaticamente el tema de la pregunta
- **Historial persistente**: Guarda la conversacion en `historial.json`
- **Estadisticas**: Cuenta mensajes, palabras, tokens y tema mas frecuente
- **Manejo de errores**: Fallback automatico a modo local si OpenAI falla
- **Funciones organizadas**: Modular, reutilizable y documentada
- **Multiple responses**: Varias respuestas por tema para evitar repeticion

## Creditos

Proyecto academico - Parcial 3: Chatbot de IA
