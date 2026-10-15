import random
from variables import (
    DIMENSIONES,
    BARCOS,
    TOTAL_VIDAS,
    AGUA,
    BARCO,
    TOCADO,
    FALLO,
)


class Tablero:
    def __init__(self, id_jugador):
        self.id_jugador = id_jugador
        self.dimensiones = DIMENSIONES
        # Matriz defensiva: barcos propios y ataques recibidos
        self.tablero_barcos = [[AGUA for _ in range(DIMENSIONES)] for _ in range(DIMENSIONES)]
        # Matriz ofensiva: radar con disparos realizados sobre el rival
        self.tablero_disparos = [[AGUA for _ in range(DIMENSIONES)] for _ in range(DIMENSIONES)]
        # Contador de casillas de barco restantes
        self.vidas = TOTAL_VIDAS

    def colocar_barcos_aleatoriamente(self):
        """
        Coloca toda la flota aleatoriamente mediante búsqueda con retroceso.
        Cada posición posible se prueba como máximo una vez por nivel de la
        búsqueda: si bloquea el resto de la flota, se deshace y se prueba otra.
        Al ser un conjunto finito de posiciones, el método no puede quedarse
        reiniciando indefinidamente.
        """
        self.tablero_barcos = [
            [AGUA for _ in range(DIMENSIONES)] for _ in range(DIMENSIONES)
        ]

        barcos = sorted(BARCOS, reverse=True)
        posiciones_por_eslora = {}

        for eslora in set(barcos):
            posiciones = set()
            for fila in range(DIMENSIONES):
                for col in range(DIMENSIONES - eslora + 1):
                    posiciones.add(tuple((fila, col + i) for i in range(eslora)))
            for fila in range(DIMENSIONES - eslora + 1):
                for col in range(DIMENSIONES):
                    posiciones.add(tuple((fila + i, col) for i in range(eslora)))
            posiciones_por_eslora[eslora] = list(posiciones)

        def colocar_siguiente(indice):
            if indice == len(barcos):
                return True

            posiciones = posiciones_por_eslora[barcos[indice]].copy()
            random.shuffle(posiciones)

            for casillas in posiciones:
                if all(self.tablero_barcos[f][c] == AGUA for f, c in casillas):
                    for f, c in casillas:
                        self.tablero_barcos[f][c] = BARCO

                    if colocar_siguiente(indice + 1):
                        return True

                    # Esta opción impidió completar la flota: deshacerla.
                    for f, c in casillas:
                        self.tablero_barcos[f][c] = AGUA

            return False

        if not colocar_siguiente(0):
            raise RuntimeError("No se ha encontrado una colocación válida para la flota.")

    def recibir_disparo(self, fila, col):
        """
        Aplica un impacto sobre el tablero defensivo.
        Si hay un barco, se actualiza a TOCADO y se descuenta una vida.
        Si hay agua, se actualiza a FALLO.
        Devuelve el resultado del disparo (TOCADO o FALLO).
        """
        if self.tablero_barcos[fila][col] == BARCO:
            self.tablero_barcos[fila][col] = TOCADO
            self.vidas -= 1
            return TOCADO
        elif self.tablero_barcos[fila][col] == AGUA:
            self.tablero_barcos[fila][col] = FALLO
            return FALLO
        else:
            # Casilla ya impactada previamente
            return self.tablero_barcos[fila][col]

    def registrar_disparo(self, fila, col, resultado):
        """
        Registra en el radar ofensivo el resultado del disparo efectuado.
        """
        self.tablero_disparos[fila][col] = resultado

    def quedan_barcos(self):
        """
        Comprueba si el jugador aún tiene barcos a flote.
        """
        return self.vidas > 0
