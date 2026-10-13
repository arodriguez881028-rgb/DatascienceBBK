from clases import Tablero
from funciones import imprimir_tableros, pedir_coordenadas, disparo_maquina
from variables import TOCADO, FALLO


def mostrar_bienvenida():
    print("=" * 65)
    print("           🚢  BIENVENIDO A HUNDIR LA FLOTA  🚢")
    print("=" * 65)
    print("Reglas del juego:")
    print(" - Tablero de 10x10 casillas (filas 0 a 9, columnas 0 a 9).")
    print(" - Flota: 1 barco de 4, 2 de 3, 3 de 2 y 4 de 1 (20 vidas en total).")
    print(" - Si aciertas en un barco enemigo, ¡vuelves a disparar!")
    print(" - Si disparas al agua, cedes el turno al contrincante.")
    print(" - En cualquier turno puedes escribir 'demo' para ver los barcos rivales.")
    print(" - Escribe 'salir' para abandonar la partida en cualquier momento.")
    print("=" * 65)


def jugar():
    mostrar_bienvenida()

    # Inicialización de tableros y colocación aleatoria de barcos
    print("\nInicializando la flota de ambos jugadores...")
    tablero_jugador = Tablero("Jugador")
    tablero_maquina = Tablero("Máquina")

    tablero_jugador.colocar_barcos_aleatoriamente()
    tablero_maquina.colocar_barcos_aleatoriamente()
    print("¡Flotas desplegadas con éxito! Comienza la partida.\n")

    turno = "jugador"

    # Bucle principal de la partida
    while tablero_jugador.quedan_barcos() and tablero_maquina.quedan_barcos():
        if turno == "jugador":
            imprimir_tableros(tablero_jugador)
            print(f"Marcador -> Tus vidas: {tablero_jugador.vidas} | Vidas rival: {tablero_maquina.vidas}")

            fila, col = pedir_coordenadas(tablero_jugador, tablero_maquina)

            # Salida voluntaria del juego
            if fila is None:
                print("\nHas decidido salir de la partida. ¡Hasta la próxima!")
                return

            # Ejecutar disparo sobre la máquina
            resultado = tablero_maquina.recibir_disparo(fila, col)
            tablero_jugador.registrar_disparo(fila, col, resultado)

            if resultado == TOCADO:
                print(f"\n🎯 ¡IMPACTO en ({fila}, {col})! Has tocado un barco enemigo.")
                if not tablero_maquina.quedan_barcos():
                    break
                print("💥 ¡Has acertado, así que vuelves a disparar!")
                # El turno se mantiene en 'jugador'
            else:
                print(f"\n🌊 ¡AGUA en ({fila}, {col})! Has fallado.")
                turno = "maquina"

        else:  # Turno de la máquina
            print("\n" + "-" * 35)
            print("🤖 Turno de la Máquina...")
            fila, col = disparo_maquina(tablero_maquina)

            resultado = tablero_jugador.recibir_disparo(fila, col)
            tablero_maquina.registrar_disparo(fila, col, resultado)

            if resultado == TOCADO:
                print(f"💥 ¡La máquina ha disparado a ({fila}, {col}) y ha TOCADO uno de tus barcos!")
                if not tablero_jugador.quedan_barcos():
                    break
                print("La máquina ha acertado y vuelve a disparar.")
                # El turno se mantiene en 'maquina'
            else:
                print(f"🌊 La máquina ha disparado a ({fila}, {col}) y ha dado en AGUA.")
                turno = "jugador"
            print("-" * 35)

    # Fin de la partida
    print("\n" + "=" * 65)
    if not tablero_maquina.quedan_barcos():
        print("🏆 ¡ENHORABUENA! ¡Has destruido toda la flota enemiga y ganado el juego!")
    elif not tablero_jugador.quedan_barcos():
        print("💀 ¡DERROTA! La máquina ha hundido todos tus barcos.")
    print("=" * 65)


if __name__ == "__main__":
    jugar()
