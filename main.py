import sys
from chatbot import chat
from config import APP_NAME, VERSION


def show_banner():
    print()
    print("=" * 50)
    print(f"  {APP_NAME}")
    print(f"  Version {VERSION}")
    print("=" * 50)
    print("  Una aplicacion educativa para aprender")
    print("  sobre Python, funciones e IA.")
    print("=" * 50)
    print()


def main():
    args = sys.argv[1:]

    if "--version" in args or "-v" in args:
        print(f"{APP_NAME} v{VERSION}")
        return

    if "--help" in args or "-h" in args:
        show_banner()
        print("Uso: python main.py [opciones]")
        print()
        print("Opciones:")
        print("  -h, --help      Muestra esta ayuda")
        print("  -v, --version   Muestra la version")
        print()
        print("Comandos durante la conversacion:")
        print("  ayuda     - Muestra los comandos disponibles")
        print("  stats     - Muestra estadisticas de la sesion")
        print("  clear     - Limpia el historial")
        print("  salir     - Termina la conversacion")
        print()
        return

    chat()


if __name__ == "__main__":
    main()
