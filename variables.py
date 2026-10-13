# Constantes del juego Hundir la Flota

# Dimensiones del tablero (10x10)
DIMENSIONES = 10

# Lista de esloras de los barcos a colocar
# 1 barco de 4, 2 barcos de 3, 3 barcos de 2, 4 barcos de 1
BARCOS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

# Total de casillas ocupadas por barcos (vidas)
TOTAL_VIDAS = sum(BARCOS)  # 20

# Símbolos del tablero
AGUA = "~"
BARCO = "B"
TOCADO = "X"
FALLO = "O"

# Límite de intentos para colocar un barco individual antes de reiniciar el tablero completo
MAX_INTENTOS_BARCO = 100
