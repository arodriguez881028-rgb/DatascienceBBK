"""
Lanzador del Servidor HTTP para la Presentación de Hundir la Flota (Bootcamp BBK)
Abre automáticamente la presentación interactiva en tu navegador web.
"""
import http.server
import socketserver
import webbrowser
import threading
import time
import os

PORT = 8000
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def abrir_navegador():
    time.sleep(1)
    webbrowser.open(f"http://localhost:{PORT}/presentacion.html")

if __name__ == "__main__":
    print("=" * 65)
    print("  🚀 INICIANDO SERVIDOR WEB DE LA PRESENTACIÓN BBK")
    print(f"  🌐 URL: http://localhost:{PORT}/presentacion.html")
    print("  Presiona Ctrl+C en esta terminal para detener el servidor")
    print("=" * 65)

    threading.Thread(target=abrir_navegador, daemon=True).start()

    with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido. ¡Buena suerte en la presentación!")
