
![The Bridge](./0-Recursos/img/TheBridge_logo.png)

# Bootcamp - Data Science

Para clonar este repositorio por https:

```
git clone https://github.com/TheBridge-BBK-Bootcamps/2026-02-BILBAO-FT-Data-Science.git
```

Información y glosario:

- https://developers.google.com/machine-learning/glossary

### Autores

**Lead Instructor**: *David Pernas*

- david.pernas@thebridgeschool.es

**Teacher Assistant**: *Itsazain M. Bilbao*

- jon.itsazain@thebridgeschool.es

---

# Notas del proyecto personal

# 🚢 Batalla de Barcos - Bootcamp Data Science BBK

> Proyecto de entrega individual para el Bootcamp de Data Science BBK (Bilbao, 2026).
> Implementación completa del juego clásico **Hundir la Flota** en Python, con arquitectura modular y algoritmo de backtracking para la colocación de barcos.

---

## 📋 Descripción del Proyecto

Juego de **Hundir la Flota** por consola en Python puro (sin librerías externas). Dos jugadores: la maquina y yo. El objetivo es hundir los 10 barcos del adversario antes de que hunda los tuyos.

- Tablero de **10 × 10** casillas (fila y columna de 0 a 9).
- La máquina nunca repite disparos y no necesita estructuras adicionales: consulta directamente su radar (`tablero_disparos`).
- Si aciertas, **vuelves a disparar**. Si fallas, cedes el turno.
- Gana el primero en hundir las **20 casillas de barco** del rival.

---

## 🏗️ Estructura del Proyecto

```
DatascienceBBK/
│
├── variables.py           # Constantes del juego
├── clases.py              # Clase Tablero + algoritmo de backtracking
├── funciones.py           # Entrada/salida, validación y visualización
├── main.py                # Bucle principal del juego
│
├── presentacion.html      # Web interactiva para la presentación en clase
├── lanzar_presentacion.py # Abre la presentación en tu navegador
│
└── README.md              
```

---

## 🚀 Cómo Ejecutar el Juego

Asegúrate de tener **Python 3.7 o superior**. No se necesita instalar ninguna dependencia externa.

```bash
# 1. Clona o descarga el repositorio
git clone https://github.com/arodrigue/DatascienceBBK.git
cd DatascienceBBK

# 2. Lanza el juego
python3 main.py
```

### Comandos Disponibles Durante la Partida

| Comando | Acción |
|:-------:|:-------|
| `3 5`   | Disparar a la fila 3, columna 5 (separado por espacio o coma) |
| `demo`  | Muestra los barcos de la máquina (modo truco/presentación) sin consumir turno |
| `salir` | Abandona la partida limpiamente |

---

## 🗂️ Descripción de los Archivos

### `variables.py`
Contiene todas las **constantes** del juego que no varían:

```python
DIMENSIONES = 10
BARCOS      = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # 10 barcos, 20 casillas
TOTAL_VIDAS = 20
AGUA        = "~"   # Casilla sin disparar
BARCO       = "B"   # Barco sin tocar
TOCADO      = "X"   # Impacto en barco
FALLO       = "O"   # Disparo al agua
```

---

### `clases.py` — Clase `Tablero`

Cada jugador tiene un objeto `Tablero` con **dos matrices de 10 × 10**:

| Matriz | Nombre | Descripción |
|:------:|:------:|:-----------|
| Defensiva | `tablero_barcos` | Tus barcos (`B`) y los impactos recibidos (`X`, `O`). Es lo que ves en "Tu Flota". |
| Ofensiva  | `tablero_disparos` | Radar de disparos realizados al rival. Empieza todo en `~`. Es tu "niebla de guerra". |

**Mecánica de un disparo** (ejemplo: Jugador dispara a Máquina en `(f, c)`):
1. Se verifica que `jugador.tablero_disparos[f][c] == "~"` (no repetido).
2. Si hay barco (`"B"`) en `maquina.tablero_barcos[f][c]` → se marca `"X"`, se descuenta 1 vida.
3. Si hay agua → se marca `"O"`.
4. El atacante registra el resultado en su propio radar: `jugador.tablero_disparos[f][c] = resultado`.

#### Algoritmo de Colocación: Backtracking

Para garantizar que los barcos siempre se coloquen sin solapamientos ni salirse del tablero y **sin riesgo de bucle infinito**:

```
1. Ordenar barcos de mayor a menor eslora: [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
2. Para cada barco:
   a. Barajar aleatoriamente todas sus posiciones válidas.
   b. Probar cada posición en el tablero.
   c. Si la posición está libre: colocar el barco y pasar al siguiente.
   d. Si no quedan posiciones válidas para los barcos siguientes:
      → RETROCEDER (backtrack): deshacer la colocación y probar la siguiente posición.
3. Si se colocan los 10 barcos: ¡éxito!
```

Resultado: **< 1 ms por tablero** en el 100% de los casos (testado en 1.000 ejecuciones consecutivas).

---

### `funciones.py`

Funciones auxiliares desacopladas de la lógica principal:

- `imprimir_tableros(tablero_jugador)`: Muestra en paralelo la flota defensiva y el radar ofensivo con cabeceras `0..9`.
- `mostrar_demo_maquina(tablero_maquina)`: Revela los barcos de la máquina para la presentación (sin consumir turno).
- `pedir_coordenadas(tablero_jugador, tablero_maquina)`: Valida enteros 0-9, detecta disparos repetidos, y gestiona `demo` y `salir`.
- `disparo_maquina(tablero_maquina)`: Selecciona con `random.choice` una casilla libre del `tablero_disparos` de la máquina.

---

### `main.py`

Flujo principal del juego:

```
mostrar_bienvenida()
inicializar tablero_jugador y tablero_maquina (Backtracking)

while jugador.quedan_barcos() and maquina.quedan_barcos():
    [TURNO JUGADOR]
      imprimir tableros
      pedir coordenadas válidas
      ejecutar disparo sobre maquina
      ¿impacto?
        Sí → vuelve a tirar (continue)
        No → cede turno a la máquina

    [TURNO MÁQUINA]
      elegir coordenada aleatoria no repetida
      ejecutar disparo sobre jugador
      ¿impacto?
        Sí → vuelve a tirar
        No → cede turno al jugador

anunciar ganador
```

---

## 🎯 Inventario de Barcos (Flota BBK)

| Cantidad | Eslora | Casillas |
|:--------:|:------:|:--------:|
| 1x | 4 | 4 |
| 2x | 3 | 6 |
| 3x | 2 | 6 |
| 4x | 1 | 4 |
| **Total** | | **20** |

---

## 🖥️ Presentación Web Interactiva

Para la exposición del **jueves 12 de marzo**, se ha desarrollado una **página web interactiva** con tablero jugable en el navegador, cronómetro de 10 minutos, modo demo para el tribunal y guión de presentación.

```bash
# Lanzar la presentación web (abre el navegador automáticamente)
python3 lanzar_presentacion.py
# → http://localhost:8000/presentacion.html
```

O simplemente abre `presentacion.html` directamente en tu navegador.

---

## 🛠️ Tecnologías

- **Python 3.7+** — Lenguaje principal
- **`random`** — Único módulo externo utilizado (incluido en la librería estándar)
- **Git** — Control de versiones
- Sin dependencias `pip`. No requiere instalación adicional.

---

## 👨‍💻 Autor

**Alejandro Rodríguez Peña**  
Alumno del Bootcamp de Data Science BBK · Bilbao, 2026  
📧 arodrigue881028@gmail.com
