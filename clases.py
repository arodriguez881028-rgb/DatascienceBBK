import random
from variables import (
    DIMENSIONES,
    BARCOS,
    TOTAL_VIDAS,
    AGUA,
    BARCO,
    TOCADO,
    FALLO,
    MAX_INTENTOS_BARCO,
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
        Coloca todos los barcos aleatoriamente en el tablero.
        Si algún barco no cabe tras MAX_INTENTOS_BARCO, vacía el tablero
        y reinicia la colocación de toda la flota para evitar bloqueos.
        """
        while True:
            # Vaciar el tablero antes de cada intento completo
            self.tablero_barcos = [[AGUA for _ in range(DIMENSIONES)] for _ in range(DIMENSIONES)]
            flota_colocada = True

            for eslora in BARCOS:
                colocado = False
                intentos = 0

                while not colocado and intentos < MAX_INTENTOS_BARCO:
                    intentos += 1
                    orientacion = random.choice(["H", "V"])

                    if orientacion == "H":
                        fila = random.randint(0, DIMENSIONES - 1)
                        col = random.randint(0, DIMENSIONES - eslora)
                        casillas = [(fila, col + i) for i in range(eslora)]
                    else:  # Vertical
                        fila = random.randint(0, DIMENSIONES - eslora)
                        col = random.randint(0, DIMENSIONES - 1)
                        casillas = [(fila + i, col) for i in range(eslora)]

                    # Comprobar si todas las casillas están libres
                    if all(self.tablero_barcos[f][c] == AGUA for f, c in casillas):
                        for f, c in casillas:
                            self.tablero_barcos[f][c] = BARCO
                        colocado = True

                # Si no se pudo colocar este barco, reiniciar toda la flota
                if not colocado:
                    flota_colocada = False
                    break

            if flota_colocada:
                break

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
