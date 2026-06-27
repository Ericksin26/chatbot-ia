# 🤖 Chatbot de IA - Parcial 3

Chatbot conversacional desarrollado en Python que funciona con OpenAI API o en modo local sin conexión.

## Estructura del proyecto

```
chatbot-ia/
├── main.py          # Punto de entrada
├── chatbot.py       # Lógica del chatbot
├── functions.py     # Funciones auxiliares
├── config.py        # Configuración (variables de entorno)
├── .env.example     # Ejemplo de configuración
├── requirements.txt # Dependencias
└── README.md        # Documentación
```

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd chatbot-ia

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key (opcional, para modo OpenAI)
cp .env.example .env
# Editar .env y agregar tu OPENAI_API_KEY
```

## Uso

```bash
python main.py
```

### Comandos durante la conversación
- `ayuda` / `help` - Muestra los comandos disponibles
- `salir` / `exit` - Termina la conversación

## Características

- **Modo OpenAI**: Respuestas inteligentes usando GPT
- **Modo Local**: Funciona sin conexión con respuestas predefinidas
- Historial de conversación
- Manejo de errores
- Funciones organizadas y reutilizables
