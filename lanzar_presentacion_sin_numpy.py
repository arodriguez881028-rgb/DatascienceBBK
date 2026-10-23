"""
Lanzador de la presentación "Hundir la Flota" (versión sin NumPy).
Usa un puerto libre elegido automáticamente por el sistema, así no choca
con el juego u otros servidores que ya estén corriendo (p. ej. el puerto 8000).
"""
import http.server
import socketserver
import threading
import webbrowser
import os

ARCHIVO = "presentacion_sin_numpy.html"
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Puerto 0 = el sistema operativo asigna un puerto libre
    with socketserver.TCPServer(("", 0), http.server.SimpleHTTPRequestHandler) as httpd:
        puerto = httpd.server_address[1]
        url = f"http://localhost:{puerto}/{ARCHIVO}"
        print("=" * 65)
        print("  🚀 PRESENTACIÓN HUNDIR LA FLOTA · BBK Bootcamp")
        print(f"  🌐 URL: {url}")
        print("  Presiona Ctrl+C para detener el servidor")
        print("=" * 65)
        threading.Timer(1, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")
