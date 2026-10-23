"""
Lanzador de "Presentación 2 definitiva" - Hundir la Flota (Bootcamp BBK).
Intenta usar el puerto 8000; si está ocupado (p. ej. por el juego u otro
servidor), el sistema asigna automáticamente un puerto libre.
"""
import http.server
import socketserver
import threading
import webbrowser
import os

PUERTO_PREFERIDO = 8000
ARCHIVO = "presentacion_2_definitiva.html"
os.chdir(os.path.dirname(os.path.abspath(__file__)))

socketserver.TCPServer.allow_reuse_address = True


def crear_servidor():
    try:
        return socketserver.TCPServer(("", PUERTO_PREFERIDO), http.server.SimpleHTTPRequestHandler)
    except OSError:
        # Puerto ocupado: puerto 0 = el sistema asigna uno libre
        return socketserver.TCPServer(("", 0), http.server.SimpleHTTPRequestHandler)


if __name__ == "__main__":
    with crear_servidor() as httpd:
        puerto = httpd.server_address[1]
        url = f"http://localhost:{puerto}/{ARCHIVO}"
        print("=" * 65)
        print("  🚀 PRESENTACIÓN 2 DEFINITIVA · HUNDIR LA FLOTA · BBK")
        if puerto != PUERTO_PREFERIDO:
            print(f"  ⚠️  El puerto {PUERTO_PREFERIDO} estaba ocupado; se usa el {puerto}")
        print(f"  🌐 URL: {url}")
        print("  Presiona Ctrl+C para detener el servidor")
        print("=" * 65)
        threading.Timer(1, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido. ¡Buena suerte en la presentación!")
