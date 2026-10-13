import random
from variables import DIMENSIONES, AGUA, BARCO, TOCADO, FALLO


def imprimir_tableros(tablero_jugador):
    """
    Imprime en pantalla el tablero defensivo del jugador (su flota)
    y su radar ofensivo (disparos realizados a la máquina) en paralelo.
    """
    print("\n" + "=" * 65)
    print("        TU FLOTA (DEFENSA)                 TU RADAR (ATAQUE)")
    print("=" * 65)

    cabecera = "   " + " ".join(str(i) for i in range(DIMENSIONES))
    print(f"{cabecera}         {cabecera}")

    for f in range(DIMENSIONES):
        fila_defensa = " ".join(tablero_jugador.tablero_barcos[f])
        fila_ataque = " ".join(tablero_jugador.tablero_disparos[f])
        print(f" {f} {fila_defensa}        {f} {fila_ataque}")
    print("=" * 65)
    print(f"Leyenda: Agua={AGUA} | Barco={BARCO} | Tocado={TOCADO} | Agua disparada={FALLO}\n")


def mostrar_demo_maquina(tablero_maquina):
    """
    Muestra el tablero con los barcos de la máquina (Modo Demo para la presentación).
    No consume turno del jugador.
    """
    print("\n--- [MODO DEMO]: TABLERO DE LA MÁQUINA ---")
    cabecera = "   " + " ".join(str(i) for i in range(DIMENSIONES))
    print(cabecera)
    for f in range(DIMENSIONES):
        fila_barcos = " ".join(tablero_maquina.tablero_barcos[f])
        print(f" {f} {fila_barcos}")
    print("-------------------------------------------\n")


def pedir_coordenadas(tablero_jugador, tablero_maquina):
    """
    Solicita coordenadas (0-9) al usuario. Valida el formato, el rango y
    que la casilla no haya sido disparada previamente.
    Gestiona los comandos 'demo' y 'salir'.
    """
    while True:
        entrada = input("Tu turno -> Introduce fila y columna (ej: '3 4'), o 'demo'/'salir': ").strip().lower()

        if entrada == "salir":
            return None, None

        if entrada == "demo":
            mostrar_demo_maquina(tablero_maquina)
            continue  # Vuelve a pedir coordenadas sin consumir el turno

        # Aceptar separación por espacio o por coma
        partes = entrada.replace(",", " ").split()

        if len(partes) != 2:
            print("❌ Entrada inválida. Debes introducir dos números entre 0 y 9 separados por espacio (ej: '2 5').")
            continue

        if not (partes[0].isdigit() and partes[1].isdigit()):
            print("❌ Ambas coordenadas deben ser números enteros entre 0 y 9.")
            continue

        fila, col = int(partes[0]), int(partes[1])

        if not (0 <= fila < DIMENSIONES and 0 <= col < DIMENSIONES):
            print(f"❌ Coordenadas fuera de rango. Deben estar entre 0 y {DIMENSIONES - 1}.")
            continue

        # Comprobar si ya se ha disparado en esa casilla (fuente única: tablero_disparos)
        if tablero_jugador.tablero_disparos[fila][col] != AGUA:
            print("⚠️ Ya has disparado en esa casilla. Elige otra coordenada.")
            continue

        return fila, col


def disparo_maquina(tablero_maquina):
    """
    Selecciona de forma aleatoria una coordenada no disparada previamente
    a partir de su propio radar ofensivo.
    """
    disponibles = [
        (f, c)
        for f in range(DIMENSIONES)
        for c in range(DIMENSIONES)
        if tablero_maquina.tablero_disparos[f][c] == AGUA
    ]
    return random.choice(disponibles)
