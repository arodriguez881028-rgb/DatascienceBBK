# Guía de estudio y exposición: Hundir la Flota

Esta carpeta contiene una copia completa del código del proyecto en `codigo/`. Los módulos Python se pueden ejecutar desde esa carpeta con `python3 main.py`. No hace falta instalar paquetes externos para el juego de consola.

## 1. Qué hace el proyecto

Es un juego de Hundir la Flota para una persona contra la máquina. Cada participante tiene una flota de 10 barcos que ocupa 20 casillas. Los barcos se colocan en horizontal o vertical, sin solaparse. En su turno, cada jugador dispara a una coordenada. Un impacto resta una vida y da otro disparo; un fallo cede el turno. Gana quien deje al contrario con cero vidas.

El programa está separado por responsabilidades:

| Archivo | Responsabilidad |
|---|---|
| `variables.py` | Reglas fijas: tamaño, flota y símbolos. |
| `clases.py` | Estado de cada tablero, colocación y resolución de impactos. |
| `funciones.py` | Entrada del usuario, validación, radar y presentación en consola. |
| `main.py` | Une las piezas y controla el ciclo de turnos y el final. |
| `lanzar_presentacion.py` | Levanta un servidor local y abre la web de presentación. |
| `presentacion.html` | Simulador web independiente implementado con HTML, CSS y JavaScript. |

## 2. Conceptos que conviene entender antes

- **Constante:** valor compartido que representa una regla del juego, como `DIMENSIONES`.
- **Clase y objeto:** `Tablero` es el molde; `tablero_jugador` y `tablero_maquina` son dos objetos con estados separados.
- **Matriz:** lista de listas. Para consultar la fila `f` y columna `c` se usa `matriz[f][c]`.
- **Método:** función que pertenece a un objeto y puede leer o cambiar su estado, por ejemplo `recibir_disparo`.
- **Búsqueda con retroceso (backtracking):** intenta una posición; si más adelante no cabe el resto de la flota, deshace la última elección y prueba otra.
- **Bucle de juego:** repite turnos mientras ambos jugadores tengan vidas.
- **Validación:** comprueba que la entrada tenga dos enteros válidos, dentro del tablero, y que no repita disparo.

## 3. Lectura del código Python, línea por línea

Los números de línea de esta guía corresponden a los archivos de `codigo/`. Las líneas en blanco solo separan secciones. Para la exposición, abre cada archivo en VS Code y sigue estos tramos.

### `variables.py` (17 líneas)

- **Línea 1:** comentario que identifica el propósito del módulo.
- **Líneas 3–4:** fija un tablero cuadrado de diez filas y diez columnas.
- **Líneas 6–8:** declara la flota por eslora. La lista contiene diez barcos y sus longitudes suman veinte casillas.
- **Líneas 10–11:** calcula las vidas iniciales sumando las esloras; así, si cambia la flota, el total se actualiza solo.
- **Líneas 13–17:** asigna símbolos legibles para agua no explorada, barco intacto, impacto y disparo fallido.

**Cómo contarlo:** “Centralizo las reglas en un único archivo para que los demás módulos usen los mismos valores y no repitan números o símbolos.”

### `clases.py` (101 líneas)

**Importaciones — líneas 1–10**

- **Línea 1:** importa `random` para mezclar posiciones posibles.
- **Líneas 2–10:** trae las constantes del módulo de reglas; el formato entre paréntesis permite ordenarlas en varias líneas.

**Clase y creación del tablero — líneas 13–22**

- **Línea 13:** define el molde `Tablero`.
- **Línea 14:** constructor ejecutado cada vez que se crea un tablero; recibe el identificador del jugador.
- **Línea 15:** guarda el nombre en el objeto.
- **Línea 16:** guarda las dimensiones configuradas.
- **Líneas 17–18:** construye una matriz defensiva 10×10, inicialmente llena de agua. El `for _` repite la creación de cada celda; el `for` exterior crea cada fila.
- **Líneas 19–20:** crea otra matriz 10×10 independiente para registrar los disparos que ese jugador ha realizado.
- **Líneas 21–22:** inicia el contador de casillas de barco restantes.

**Colocación de barcos — líneas 24–71**

- **Líneas 24–31:** define el método y documenta que coloca la flota con búsqueda y retroceso, probando un conjunto finito de posiciones.
- **Líneas 32–34:** reinicia la matriz defensiva antes de desplegar barcos.
- **Línea 36:** ordena las longitudes de mayor a menor. Colocar primero los barcos largos reduce callejones sin salida.
- **Línea 37:** crea un diccionario para guardar las posiciones candidatas agrupadas por longitud.
- **Línea 39:** recorre las longitudes distintas; `set` evita volver a generar las mismas posiciones para barcos de idéntica eslora.
- **Línea 40:** crea un conjunto para no duplicar una posición candidata.
- **Líneas 41–43:** generan todas las ubicaciones horizontales que caben: se recorre cada fila y solo columnas donde el barco no se sale del borde.
- **Líneas 44–46:** generan todas las ubicaciones verticales válidas: se recorre cada columna y solo filas donde cabe la longitud.
- **Línea 47:** convierte las candidatas en lista y las guarda según la eslora.
- **Línea 49:** declara una función interna recursiva; `indice` indica qué barco de la lista ordenada se intenta colocar.
- **Líneas 50–51:** caso base: si ya se colocaron todos los barcos, devuelve éxito (`True`).
- **Línea 53:** copia la lista de posiciones candidatas para el tamaño del barco actual.
- **Línea 54:** mezcla el orden para que cada partida tenga una disposición distinta.
- **Línea 56:** prueba una por una las posiciones candidatas.
- **Línea 57:** `all(...)` comprueba que todas las casillas de esa posición estén libres.
- **Líneas 58–59:** si cabe el barco, marca cada una de sus coordenadas como barco.
- **Líneas 61–62:** llama recursivamente para colocar el siguiente barco; si las llamadas posteriores tienen éxito, conserva la posición y devuelve `True`.
- **Línea 64:** comentario que explica la operación inversa cuando la opción bloquea la colocación futura.
- **Líneas 65–66:** deshace la colocación fallida, dejando libres esas casillas para intentar otra alternativa.
- **Línea 68:** devuelve `False` cuando ya se agotaron las posiciones de ese nivel.
- **Líneas 70–71:** inicia la recursión con el primer barco; si no hay solución, lanza un error explícito.

**Disparos y estado — líneas 73–101**

- **Líneas 73–79:** define y documenta la operación que procesa un disparo recibido.
- **Línea 80:** consulta el contenido de la coordenada defensiva.
- **Líneas 81–83:** si había barco, lo marca tocado, resta una vida y devuelve el símbolo de impacto.
- **Líneas 84–86:** si había agua, marca el fallo y devuelve ese resultado. No cambia las vidas.
- **Líneas 87–89:** si la casilla ya tenía otro símbolo, devuelve lo que hay; la validación normal evita llegar aquí con repetición.
- **Líneas 91–95:** método para guardar en el radar propio el resultado obtenido contra el rival.
- **Líneas 97–101:** método de consulta booleana; devuelve `True` mientras queden vidas.

**Cómo contar el backtracking:** “La función coloca un barco, se llama a sí misma para colocar el siguiente y, si descubre que esa elección impide completar la flota, borra ese barco y prueba otra posición. Es como resolver un laberinto: avanzo, y si llego a un callejón sin salida, vuelvo al último cruce.”

### `funciones.py` (91 líneas)

**Importaciones — líneas 1–2**

- **Línea 1:** importa la selección aleatoria que utiliza la máquina.
- **Línea 2:** importa dimensiones y símbolos compartidos.

**Mostrar tableros — líneas 5–22**

- **Líneas 5–9:** define y documenta la función que imprime la defensa y el radar del usuario.
- **Líneas 10–12:** imprime separadores y títulos para organizar la salida.
- **Línea 14:** genera la cabecera numérica de columnas del 0 al 9.
- **Línea 15:** muestra esa cabecera encima de ambas matrices.
- **Línea 17:** recorre las diez filas.
- **Líneas 18–19:** convierte cada fila de matrices en texto separado por espacios.
- **Línea 20:** imprime número de fila y contenido de ambas matrices en paralelo.
- **Líneas 21–22:** imprime cierre y leyenda de símbolos.

**Modo demostración — líneas 25–36**

- **Líneas 25–29:** define la función de demostración; es una ayuda visual y no altera el estado del juego.
- **Líneas 30–32:** imprime título y encabezado de columnas.
- **Líneas 33–35:** recorre e imprime cada fila de la flota de la máquina.
- **Línea 36:** cierra la salida visual.

**Pedir y validar coordenadas — líneas 39–77**

- **Líneas 39–44:** define la entrada del jugador y explica qué valida.
- **Línea 45:** bucle que vuelve a preguntar hasta recibir una entrada válida o un comando.
- **Línea 46:** lee texto; `strip()` quita espacios al principio/final y `lower()` normaliza mayúsculas.
- **Líneas 48–49:** si se pide salir, devuelve dos valores `None` como señal especial al programa principal.
- **Líneas 51–53:** si se pide demo, muestra el tablero enemigo y vuelve a pedir coordenadas sin gastar turno.
- **Líneas 55–56:** permite coma o espacios como separador y divide la entrada en partes.
- **Líneas 58–60:** exige exactamente dos valores; si no, informa del error y repite.
- **Líneas 62–64:** comprueba que ambos textos sean enteros no negativos usando `isdigit()`.
- **Línea 66:** convierte las dos partes de texto a números enteros.
- **Líneas 68–70:** comprueba que fila y columna estén entre 0 y 9; en caso contrario, repite.
- **Líneas 72–75:** consulta el radar propio para impedir disparos repetidos.
- **Línea 77:** devuelve fila y columna cuando pasan todas las validaciones.

**Disparo aleatorio de la máquina — líneas 80–91**

- **Líneas 80–84:** define y documenta la selección del siguiente disparo de la máquina.
- **Líneas 85–90:** comprensión de lista que recoge coordenadas cuyo radar sigue marcado como agua sin explorar.
- **Línea 91:** escoge al azar una coordenada disponible. Como usa el radar, no repite disparos.

**Cómo contarlo:** “Aíslo la interacción con consola y validaciones en funciones separadas. Así `main.py` se concentra en las reglas de turnos y no en leer texto o dibujar matrices.”

### `main.py` (90 líneas)

**Importaciones y bienvenida — líneas 1–17**

- **Líneas 1–3:** importa la clase, funciones auxiliares y constantes que necesita la partida.
- **Línea 6:** define la función de bienvenida.
- **Líneas 7–17:** imprimen título, reglas y comandos disponibles. Son salida informativa y no cambian el estado.

**Preparar la partida — líneas 20–32**

- **Línea 20:** define `jugar`, el punto que organiza una partida completa.
- **Línea 21:** presenta las reglas antes de comenzar.
- **Líneas 23–24:** anuncia que se inicializan las flotas.
- **Líneas 25–26:** crea un objeto `Tablero` por jugador; cada uno tendrá sus propias matrices y vidas.
- **Líneas 28–29:** coloca la flota de manera independiente en cada tablero.
- **Línea 30:** comunica que ya se puede jugar.
- **Línea 32:** inicializa el estado del turno con el jugador humano.

**Bucle y turno humano — líneas 34–59**

- **Línea 35:** repite el juego mientras ambos tableros indiquen que quedan vidas.
- **Línea 36:** selecciona el bloque de turno humano.
- **Línea 37:** muestra las dos matrices propias.
- **Línea 38:** muestra el marcador de vidas.
- **Línea 40:** solicita coordenadas validadas.
- **Líneas 42–45:** detecta la señal `(None, None)` de salir, muestra mensaje y termina `jugar` con `return`.
- **Línea 48:** aplica el disparo del jugador sobre la defensa de la máquina.
- **Línea 49:** guarda el resultado en el radar del jugador.
- **Líneas 51–56:** ante un impacto, lo anuncia; si era la última vida rival, rompe el bucle; en otro caso mantiene el turno humano.
- **Líneas 57–59:** ante un fallo, lo anuncia y cambia el turno a la máquina.

**Turno de la máquina — líneas 61–78**

- **Línea 61:** rama alternativa del turno automático.
- **Líneas 62–63:** anuncia el turno.
- **Línea 64:** obtiene una coordenada aleatoria todavía no usada.
- **Línea 66:** aplica el disparo a la defensa del jugador.
- **Línea 67:** registra el resultado en el radar de la máquina.
- **Líneas 69–74:** si acierta, lo anuncia; si era el último barco, termina el bucle; si no, conserva su turno para volver a disparar.
- **Líneas 75–78:** si falla, lo anuncia y devuelve el turno al usuario; imprime un separador al cerrar la jugada.

**Final y punto de entrada — líneas 80–90**

- **Líneas 80–81:** abre la sección de resultado final.
- **Líneas 82–83:** si la máquina se quedó sin vidas, declara ganador al usuario.
- **Líneas 84–85:** si el tablero humano se quedó sin vidas, declara ganador a la máquina.
- **Línea 86:** cierra el mensaje.
- **Línea 89:** comprueba que el archivo se está ejecutando directamente y no importando como módulo.
- **Línea 90:** inicia el juego solo en ejecución directa.

**Cómo contarlo:** “`main.py` coordina objetos y funciones. El bucle depende de las vidas. Cada turno cambia solo cuando hay un fallo; un acierto conserva el turno. Al acabar, las vidas determinan al ganador.”

### `lanzar_presentacion.py` (32 líneas)

- **Líneas 1–4:** comentario de documentación del lanzador.
- **Líneas 5–10:** importa el servidor HTTP, herramientas de red local, navegador, hilo, temporizador y utilidades de rutas.
- **Línea 12:** fija el puerto local 8000.
- **Línea 13:** sitúa el servidor en la carpeta del propio script para encontrar `presentacion.html`.
- **Línea 15:** define la acción de abrir navegador.
- **Línea 16:** espera un segundo para dar tiempo al servidor a arrancar.
- **Línea 17:** abre la URL local de la presentación.
- **Línea 19:** bloque de ejecución directa.
- **Líneas 20–24:** muestran instrucciones al usuario.
- **Línea 26:** inicia en segundo plano el navegador; `daemon=True` permite que el hilo auxiliar cierre con el proceso.
- **Línea 28:** crea un servidor TCP en el puerto indicado que sirve archivos de la carpeta actual.
- **Líneas 29–30:** atiende solicitudes continuamente.
- **Líneas 31–32:** captura Ctrl+C y muestra un cierre limpio.

### `presentacion.html` (697 líneas)

Este archivo implementa una demostración web paralela al juego de consola; no importa ni ejecuta los módulos Python. Se puede exponer en cinco bloques:

1. **Líneas 1–24:** estructura inicial del documento, idioma español, metadatos, título, estilos CSS y animaciones.
2. **Líneas 25–371:** HTML de la interfaz: encabezado, reloj de diez minutos, pestañas, dos tableros, botones de reinicio/demo y guion de presentación.
3. **Línea 373 en adelante:** comienza JavaScript, donde se administra el estado del simulador web.
4. **Líneas 374–389:** dimensiones, flota y variables del tablero/temporizador.
5. **Líneas 390–430:** iniciar, pausar, reiniciar y dibujar el reloj.
6. **Líneas 431–483:** `generarTableroConBacktracking` y sus funciones internas para barajar y colocar la flota.
7. **Líneas 484–517:** iniciar una partida y activar/desactivar la revelación de barcos.
8. **Líneas 518–598:** `renderizarTableros` actualiza la cuadrícula web y representa los estados con colores/símbolos.
9. **Líneas 599–633:** `dispararJugador` procesa el clic del usuario, muestra impacto/fallo y evalúa victoria.
10. **Líneas 634–675:** `dispararMaquina` elige una casilla disponible y actualiza el turno.
11. **Líneas 676–681:** actualiza la etiqueta visual del turno.
12. **Líneas 682–694:** cambia entre pestañas de simulador, guion y arquitectura.
13. **Línea 695:** cierra la sección de JavaScript.

**Cómo contarlo con honestidad:** “La página web es una demo con su propia lógica en JavaScript. El juego de consola es el proyecto Python descrito en los módulos anteriores. El lanzador solo sirve la página localmente; no conecta ambos motores.”

## 4. Guion sugerido para una exposición de 10 minutos

### 0:00–1:00 — Problema y objetivo

“Mi proyecto es una versión de Hundir la Flota para una persona contra la máquina. El objetivo es modelar un juego por turnos, validar entradas y mantener el estado de las dos flotas.”

Enseña el árbol de archivos y señala que cada archivo Python tiene una responsabilidad concreta.

### 1:00–2:00 — Reglas y datos

Abre `variables.py`. Explica tablero 10×10, flota y total de veinte vidas. Cuenta por qué los símbolos son constantes: centralizan las reglas y facilitan cambiar su representación.

### 2:00–4:30 — Modelo y colocación

Abre `clases.py`. Explica que cada objeto `Tablero` guarda defensa, radar y vidas. Dibuja en una hoja la recursión: colocar barco → colocar siguiente → si falla, deshacer → probar otra posición. Aclara que el método solo exige que los barcos no se solapen; no comprueba separación entre barcos.

### 4:30–5:45 — Interacción y validación

Abre `funciones.py`. Sigue una entrada de ejemplo: `3, 4` se normaliza a `3 4`, se separa, comprueba dos valores, comprueba que sean enteros, revisa límites y evita repetir una coordenada. Menciona `demo` y `salir`.

### 5:45–8:00 — Flujo principal

Abre `main.py`. Explica creación de los dos tableros, bucle mientras haya vidas, disparo del jugador, disparo aleatorio de la máquina, turno extra al acertar y cambio de turno al fallar. Termina con condición de victoria y el bloque `if __name__ == "__main__"`.

### 8:00–9:00 — Presentación web

Muestra brevemente `presentacion.html` y `lanzar_presentacion.py`. Indica que el navegador muestra otro simulador (HTML/CSS/JavaScript) para la exposición; el lanzador lo sirve en localhost y no ejecuta el motor Python.

### 9:00–10:00 — Decisiones y cierre

“Separé configuración, estado, funciones auxiliares y coordinación para que el código se pueda leer y modificar por partes. La máquina elige al azar entre coordenadas disponibles y la colocación aleatoria usa backtracking. Como mejoras, añadiría pruebas automáticas, dificultad para la IA, y validaría también que los barcos no puedan tocarse si esa variante de reglas lo exige.”

## 5. Demostración en vivo recomendada

1. Desde la carpeta `codigo`, ejecuta `python3 main.py`.
2. Enseña el radar y la flota propia antes de disparar.
3. Introduce una coordenada, por ejemplo `3 4`; prueba también una inválida para mostrar la validación.
4. Escribe `demo` para enseñar el tablero de la máquina sin gastar turno.
5. Explica que el acierto da otro intento y el agua cede el turno.
6. Escribe `salir` para cerrar la demostración sin tener que terminar toda la partida.
7. Para enseñar la web, en otra terminal ejecuta `python3 lanzar_presentacion.py`; detén el servidor con Ctrl+C.

## 6. Preguntas que te pueden hacer

**¿Por qué hay dos matrices por jugador?** Una representa ataques recibidos en mi flota y otra representa los ataques que yo he hecho al rival. Mantenerlas separadas evita mezclar información de ataque y defensa.

**¿Cómo evita la máquina repetir coordenadas?** Busca en su radar las celdas que siguen en `AGUA` y elige al azar solo entre esas.

**¿Qué es el caso base de la recursión?** En `colocar_siguiente`, cuando el índice alcanza la cantidad de barcos, se devuelve `True`: la flota está completa.

**¿Qué significa retroceder?** Deshacer una colocación que no permite terminar la flota y probar otra alternativa.

**¿Qué limita el juego?** La IA dispara aleatoriamente y no tiene estrategia. El algoritmo coloca barcos sin solapamiento, pero permite que barcos distintos estén pegados. La web es una implementación aparte en JavaScript.

**¿Por qué dividir en archivos?** Reduce el acoplamiento: las reglas, el estado, la interacción y el flujo principal se pueden entender y mantener por separado.


## 7. Código fuente completo con comentarios de estudio

A continuación está el código real, copiado de los archivos de esta carpeta. Las secciones anteriores explican cada tramo de Python; aquí puedes leer el código completo sin cambiar de archivo. En el HTML, la explicación por bloques identifica qué hace cada parte de la interfaz y del simulador JavaScript.

### Código real: `variables.py`

Este archivo define los valores centrales de las reglas: el tamaño, la flota, las vidas y los símbolos que comparten los demás módulos.

```python
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
```

### Código real: `clases.py`

Aquí está la clase `Tablero`: conserva el estado de cada jugador, coloca barcos con backtracking, procesa impactos y permite consultar si quedan barcos.

```python
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
```

### Código real: `funciones.py`

Estas funciones se encargan de mostrar las matrices, leer y validar las coordenadas y seleccionar el disparo de la máquina.

```python
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
```

### Código real: `main.py`

Este módulo coordina la partida completa: inicializa tableros, alterna turnos, aplica las reglas de impacto y decide el resultado.

```python
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
```

### Código real: `lanzar_presentacion.py`

Este lanzador inicia un servidor HTTP local y abre la presentación en el navegador. No ejecuta el juego Python.

```python
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
```

### Código real: `presentacion.html`

Este es el archivo completo de la demo web. Contiene la estructura HTML, los estilos CSS y la lógica JavaScript del simulador, que funciona de forma separada al juego de consola.

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Batalla de Barcos - Data Science Bootcamp BBK</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    @keyframes pulse-subtle {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.85; transform: scale(1.03); }
    }
    .water-cell {
      background: radial-gradient(circle, #1e3a8a 10%, #0f172a 90%);
      transition: all 0.2s ease;
    }
    .water-cell:hover {
      filter: brightness(1.3);
      cursor: crosshair;
    }
    .radar-sweep {
      background: linear-gradient(135deg, rgba(6, 182, 212, 0.15), transparent);
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans min-h-screen p-4 md:p-8 antialiased selection:bg-cyan-500 selection:text-white">

  <!-- ENCABEZADO BBK BOOTCAMP -->
  <header class="max-w-6xl mx-auto mb-8 border-b border-cyan-800/40 pb-6 flex flex-col md:flex-row justify-between items-center gap-4">
    <div class="flex items-center gap-4">
      <div class="w-14 h-14 rounded-2xl bg-gradient-to-tr from-cyan-600 to-blue-700 flex items-center justify-center shadow-lg shadow-cyan-500/20 text-3xl font-black">
        ⛵
      </div>
      <div>
        <div class="flex items-center gap-2">
          <span class="px-2.5 py-0.5 text-xs font-bold uppercase tracking-wider rounded-full bg-cyan-950 text-cyan-400 border border-cyan-700/50">
            BBK Kuna · Data Science Edition
          </span>
          <span class="text-xs text-slate-400">Entrega Oficial Python</span>
        </div>
        <h1 class="text-2xl md:text-3xl font-black tracking-tight bg-gradient-to-r from-cyan-400 via-sky-300 to-blue-400 bg-clip-text text-transparent">
          Batalla de Barcos del Bootcamp BBK
        </h1>
        <p class="text-sm text-slate-400">
          Desplegado en la Ría de Bilbao · Arquitectura Modular con Backtracking
        </p>
      </div>
    </div>

    <!-- TEMPORIZADOR DE LA PRESENTACIÓN DE 10 MINUTOS -->
    <div class="flex items-center gap-4 bg-slate-900/90 border border-slate-800 rounded-2xl px-5 py-3 shadow-xl">
      <div class="text-right">
        <div class="text-xs uppercase tracking-wider text-slate-400 font-semibold">Tiempo Presentación</div>
        <div id="timer-display" class="text-2xl font-mono font-bold text-cyan-400">10:00</div>
      </div>
      <div class="flex flex-col gap-1">
        <button id="timer-btn" onclick="toggleTimer()" class="px-3 py-1 bg-cyan-600 hover:bg-cyan-500 text-xs font-bold rounded-lg transition">
          Iniciar
        </button>
        <button onclick="resetTimer()" class="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 rounded-lg transition">
          Reset
        </button>
      </div>
    </div>
  </header>

  <!-- PESTAÑAS PRINCIPALES: JUEGO / GUIÓN DE PRESENTACIÓN / CÓDIGO -->
  <main class="max-w-6xl mx-auto space-y-8">
    <div class="flex border-b border-slate-800 gap-2">
      <button onclick="showTab('juego')" id="tab-btn-juego" class="px-5 py-2.5 font-bold text-sm border-b-2 border-cyan-400 text-cyan-400 transition flex items-center gap-2">
        <span>🎮</span> Simulador Interactivo
      </button>
      <button onclick="showTab('guion')" id="tab-btn-guion" class="px-5 py-2.5 font-bold text-sm border-b-2 border-transparent text-slate-400 hover:text-slate-200 transition flex items-center gap-2">
        <span>⏱️</span> Guión de los 10 Minutos
      </button>
      <button onclick="showTab('arquitectura')" id="tab-btn-arquitectura" class="px-5 py-2.5 font-bold text-sm border-b-2 border-transparent text-slate-400 hover:text-slate-200 transition flex items-center gap-2">
        <span>💻</span> Estructura y Backtracking
      </button>
    </div>

    <!-- ========================================== -->
    <!-- TAB 1: SIMULADOR INTERACTIVO DEL JUEGO      -->
    <!-- ========================================== -->
    <div id="tab-juego" class="space-y-6">
      
      <!-- CONTROLES Y MARCADOR -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <!-- Vidas Jugador -->
        <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 flex items-center justify-between shadow-lg">
          <div>
            <div class="text-xs uppercase text-slate-400 font-medium">Flota BBK (Tú)</div>
            <div id="vidas-jugador" class="text-2xl font-black text-cyan-400">20 / 20</div>
            <div class="text-[11px] text-slate-500">Vidas restantes</div>
          </div>
          <div class="text-3xl">🛡️</div>
        </div>

        <!-- Vidas Máquina -->
        <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 flex items-center justify-between shadow-lg">
          <div>
            <div class="text-xs uppercase text-slate-400 font-medium">Flota Rival (Máquina)</div>
            <div id="vidas-maquina" class="text-2xl font-black text-rose-400">20 / 20</div>
            <div class="text-[11px] text-slate-500">Vidas restantes</div>
          </div>
          <div class="text-3xl">🤖</div>
        </div>

        <!-- Turno actual y Mensaje -->
        <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 md:col-span-2 flex flex-col justify-between shadow-lg">
          <div class="flex items-center justify-between">
            <span class="text-xs uppercase tracking-wider text-slate-400 font-semibold">Estado del Combate</span>
            <span id="turno-badge" class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-cyan-900/80 text-cyan-300 border border-cyan-600/40">
              Turno: Alumno BBK
            </span>
          </div>
          <div id="mensaje-estado" class="text-sm font-medium text-slate-200 mt-1">
            Haz clic en una casilla del <strong class="text-rose-400">Radar Rival</strong> para disparar un misil.
          </div>
        </div>
      </div>

      <!-- BOTONES DE ACCIÓN (DEMO, REINICIAR) -->
      <div class="flex flex-wrap items-center justify-between gap-3 bg-slate-900/40 p-3 rounded-xl border border-slate-800/80">
        <div class="flex items-center gap-2 text-xs text-slate-400">
          <span class="inline-block w-3 h-3 rounded-sm bg-blue-600"></span> Barco BBK
          <span class="inline-block w-3 h-3 rounded-sm bg-rose-600 ml-2"></span> Tocado (X)
          <span class="inline-block w-3 h-3 rounded-sm bg-slate-700 ml-2"></span> Agua (O)
        </div>
        <div class="flex items-center gap-3">
          <button onclick="toggleDemoMode()" id="btn-demo" class="px-4 py-2 rounded-xl text-xs font-bold border border-amber-500/50 text-amber-400 bg-amber-950/40 hover:bg-amber-900/50 transition flex items-center gap-1.5 shadow-sm">
            <span>👁️</span> Modo Demo / Tribunal (Revelar Rival)
          </button>
          <button onclick="iniciarNuevaPartida()" class="px-4 py-2 rounded-xl text-xs font-bold bg-cyan-600 hover:bg-cyan-500 text-slate-950 transition flex items-center gap-1.5 shadow-md shadow-cyan-600/20">
            <span>🔄</span> Reposicionar Flotas (Backtracking)
          </button>
        </div>
      </div>

      <!-- LOS DOS TABLEROS LADO A LADO -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
        
        <!-- TABLERO JUGADOR (DEFENSA) -->
        <div class="bg-slate-900/90 border border-slate-800 rounded-3xl p-6 shadow-2xl relative overflow-hidden">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h2 class="text-base font-bold text-cyan-400 flex items-center gap-2">
                <span>⚓</span> Flota de Bilbao (Tu Defensa)
              </h2>
              <p class="text-xs text-slate-400">Tus barcos: Pandas, NumPy, Scikit y Python</p>
            </div>
            <span class="text-xs bg-slate-800 px-2.5 py-1 rounded-lg text-slate-300 font-mono">tablero_barcos</span>
          </div>

          <!-- Cabecera columnas 0..9 -->
          <div class="grid grid-cols-11 gap-1 text-center font-mono text-xs text-slate-500 mb-1">
            <div></div>
            <div>0</div><div>1</div><div>2</div><div>3</div><div>4</div><div>5</div><div>6</div><div>7</div><div>8</div><div>9</div>
          </div>

          <!-- Matriz del Jugador -->
          <div id="grid-jugador" class="space-y-1 font-mono text-xs select-none">
            <!-- Inyectado por JS -->
          </div>
        </div>

        <!-- TABLERO RADAR / MÁQUINA (ATAQUE) -->
        <div class="bg-slate-900/90 border border-rose-950/40 rounded-3xl p-6 shadow-2xl relative overflow-hidden">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h2 class="text-base font-bold text-rose-400 flex items-center gap-2">
                <span>🎯</span> Radar Ofensivo (Ataque a la Máquina)
              </h2>
              <p class="text-xs text-slate-400">Haz clic en una casilla para atacar (0 a 9)</p>
            </div>
            <span class="text-xs bg-slate-800 px-2.5 py-1 rounded-lg text-slate-300 font-mono">tablero_disparos</span>
          </div>

          <!-- Cabecera columnas 0..9 -->
          <div class="grid grid-cols-11 gap-1 text-center font-mono text-xs text-slate-500 mb-1">
            <div></div>
            <div>0</div><div>1</div><div>2</div><div>3</div><div>4</div><div>5</div><div>6</div><div>7</div><div>8</div><div>9</div>
          </div>

          <!-- Matriz del Radar Rival -->
          <div id="grid-maquina" class="space-y-1 font-mono text-xs select-none">
            <!-- Inyectado por JS -->
          </div>
        </div>
      </div>

      <!-- INVENTARIO DE BARCOS CON GUIÑOS AL BOOTCAMP -->
      <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-5">
        <h3 class="text-xs uppercase font-bold tracking-wider text-slate-400 mb-3">
          Inventario de Barcos del Bootcamp BBK (10 barcos · 20 casillas)
        </h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
          <div class="bg-slate-800/60 p-3 rounded-xl border border-slate-700/50">
            <div class="font-bold text-cyan-300">1x Acorazado BBK (4)</div>
            <div class="text-[11px] text-slate-400">"El Coloso de la Ría"</div>
            <div class="flex gap-1 mt-2">
              <span class="w-4 h-4 rounded bg-cyan-600 inline-block"></span>
              <span class="w-4 h-4 rounded bg-cyan-600 inline-block"></span>
              <span class="w-4 h-4 rounded bg-cyan-600 inline-block"></span>
              <span class="w-4 h-4 rounded bg-cyan-600 inline-block"></span>
            </div>
          </div>
          <div class="bg-slate-800/60 p-3 rounded-xl border border-slate-700/50">
            <div class="font-bold text-sky-300">2x Fragatas Pandas (3)</div>
            <div class="text-[11px] text-slate-400">DataFrame I y DataFrame II</div>
            <div class="flex gap-1 mt-2">
              <span class="w-4 h-4 rounded bg-sky-600 inline-block"></span>
              <span class="w-4 h-4 rounded bg-sky-600 inline-block"></span>
              <span class="w-4 h-4 rounded bg-sky-600 inline-block"></span>
            </div>
          </div>
          <div class="bg-slate-800/60 p-3 rounded-xl border border-slate-700/50">
            <div class="font-bold text-blue-300">3x Destructores NumPy (2)</div>
            <div class="text-[11px] text-slate-400">Matrices N-Dimensionales</div>
            <div class="flex gap-1 mt-2">
              <span class="w-4 h-4 rounded bg-blue-600 inline-block"></span>
              <span class="w-4 h-4 rounded bg-blue-600 inline-block"></span>
            </div>
          </div>
          <div class="bg-slate-800/60 p-3 rounded-xl border border-slate-700/50">
            <div class="font-bold text-indigo-300">4x Lanchas Python (1)</div>
            <div class="text-[11px] text-slate-400">Scripts rápidos e iteradores</div>
            <div class="flex gap-1 mt-2">
              <span class="w-4 h-4 rounded bg-indigo-600 inline-block"></span>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- ========================================== -->
    <!-- TAB 2: GUIÓN DE PRESENTACIÓN (10 MINUTOS)  -->
    <!-- ========================================== -->
    <div id="tab-guion" class="hidden space-y-6">
      <div class="bg-slate-900 border border-slate-800 rounded-3xl p-8 space-y-6">
        <div>
          <span class="px-3 py-1 bg-cyan-950 text-cyan-400 border border-cyan-800 rounded-full text-xs font-bold uppercase">
            Estructura Recomendada · 10 Minutos Máximo
          </span>
          <h2 class="text-2xl font-black mt-2 text-white">Guión para Clavar la Presentación</h2>
          <p class="text-slate-400 text-sm">
            Diseñado para que hables con total seguridad y dejes 2 minutos para las preguntas del tribunal.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          <!-- Minuto 0 a 2 -->
          <div class="border border-slate-800 bg-slate-950/60 p-5 rounded-2xl relative">
            <span class="absolute top-4 right-4 text-xs font-bold font-mono text-cyan-400 bg-cyan-950/60 px-2.5 py-1 rounded-lg">
              00:00 - 02:00
            </span>
            <h3 class="font-bold text-cyan-300 text-base mb-2">1. Introducción y Arquitectura</h3>
            <ul class="text-xs text-slate-300 space-y-2">
              <li>• Saludo y mención al <strong>Bootcamp Data Science BBK</strong>.</li>
              <li>• Explicación de la arquitectura modular: <strong>4 scripts .py</strong> (`variables.py`, `clases.py`, `funciones.py`, `main.py`).</li>
              <li>• Por qué no se usó notebook: modularidad profesional y separación de responsabilidades.</li>
            </ul>
          </div>

          <!-- Minuto 2 a 4 -->
          <div class="border border-slate-800 bg-slate-950/60 p-5 rounded-2xl relative">
            <span class="absolute top-4 right-4 text-xs font-bold font-mono text-sky-400 bg-sky-950/60 px-2.5 py-1 rounded-lg">
              02:00 - 04:30
            </span>
            <h3 class="font-bold text-sky-300 text-base mb-2">2. El Desafío: Algoritmo de Backtracking</h3>
            <ul class="text-xs text-slate-300 space-y-2">
              <li>• Explicar por qué un `while` infinito con reintentos aleatorios podía quedarse atascado.</li>
              <li>• La solución elegante: <strong>Búsqueda con Retroceso (Backtracking recursivo)</strong>.</li>
              <li>• Ordenar de mayor a menor eslora y deshacer la posición si bloquea al resto de la flota.</li>
              <li>• Probado en 1.000 tableros: media de 0.5 ms sin un solo error.</li>
            </ul>
          </div>

          <!-- Minuto 4 a 7 -->
          <div class="border border-slate-800 bg-slate-950/60 p-5 rounded-2xl relative">
            <span class="absolute top-4 right-4 text-xs font-bold font-mono text-blue-400 bg-blue-950/60 px-2.5 py-1 rounded-lg">
              04:30 - 07:30
            </span>
            <h3 class="font-bold text-blue-300 text-base mb-2">3. Demo en Terminal (`python3 main.py`)</h3>
            <ul class="text-xs text-slate-300 space-y-2">
              <li>• Abrir la terminal y ejecutar `python3 main.py`.</li>
              <li>• Mostrar la colocación limpia y los dos tableros paralelos con índices 0 a 9.</li>
              <li>• Disparar a una coordenada válida, fallar (agua) y ver cómo la máquina responde sin repetir casillas.</li>
              <li>• Escribir el comando especial <strong>`demo`</strong> para mostrar al tribunal los barcos de la máquina sin perder el turno.</li>
            </ul>
          </div>

          <!-- Minuto 7 a 10 -->
          <div class="border border-slate-800 bg-slate-950/60 p-5 rounded-2xl relative">
            <span class="absolute top-4 right-4 text-xs font-bold font-mono text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded-lg">
              07:30 - 10:00
            </span>
            <h3 class="font-bold text-emerald-300 text-base mb-2">4. Git, Buenas Prácticas y Conclusión</h3>
            <ul class="text-xs text-slate-300 space-y-2">
              <li>• Mostrar el repositorio Git (`git log`) con commits semánticos y `.gitignore`.</li>
              <li>• Cero dependencias externas (`pip`), uso exclusivo de la librería estándar `random`.</li>
              <li>• Agradecimientos al equipo de profesores de BBK y paso a la ronda de preguntas.</li>
            </ul>
          </div>

        </div>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 3: ARQUITECTURA DE CÓDIGO              -->
    <!-- ========================================== -->
    <div id="tab-arquitectura" class="hidden space-y-6">
      <div class="bg-slate-900 border border-slate-800 rounded-3xl p-8 space-y-6">
        <div>
          <span class="px-3 py-1 bg-blue-950 text-blue-400 border border-blue-800 rounded-full text-xs font-bold uppercase">
            Diseño Modular Orientado a Objetos
          </span>
          <h2 class="text-2xl font-black mt-2 text-white">Estructura del Proyecto en 4 Archivos</h2>
        </div>

        <div class="space-y-4 font-mono text-xs">
          <!-- variables.py -->
          <div class="bg-slate-950 p-4 rounded-2xl border border-slate-800">
            <div class="text-cyan-400 font-bold mb-1">📄 variables.py</div>
            <p class="text-slate-400 font-sans text-xs mb-2">Constantes fijas del juego.</p>
            <pre class="text-slate-300 overflow-x-auto">DIMENSIONES = 10
BARCOS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
TOTAL_VIDAS = sum(BARCOS)  # 20
AGUA = "~" ; BARCO = "B" ; TOCADO = "X" ; FALLO = "O"</pre>
          </div>

          <!-- clases.py -->
          <div class="bg-slate-950 p-4 rounded-2xl border border-slate-800">
            <div class="text-sky-400 font-bold mb-1">📄 clases.py (Clase Tablero)</div>
            <p class="text-slate-400 font-sans text-xs mb-2">
              Contiene dos matrices: <code>tablero_barcos</code> (defensa) y <code>tablero_disparos</code> (ofensiva/radar).
              Implementa colocación determinista con <strong>Backtracking</strong>:
            </p>
            <pre class="text-slate-300 overflow-x-auto">def colocar_siguiente(indice):
    if indice == len(barcos): return True
    for casillas in posiciones_barajadas:
        if all(tablero[f][c] == AGUA for f, c in casillas):
            marcar_barco(casillas)
            if colocar_siguiente(indice + 1): return True
            deshacer_barco(casillas) # BACKTRACKING
    return False</pre>
          </div>

          <!-- funciones.py -->
          <div class="bg-slate-950 p-4 rounded-2xl border border-slate-800">
            <div class="text-blue-400 font-bold mb-1">📄 funciones.py</div>
            <p class="text-slate-400 font-sans text-xs mb-2">Entrada validada 0-9, visualización dual, selección aleatoria sin repetición de la máquina.</p>
          </div>

          <!-- main.py -->
          <div class="bg-slate-950 p-4 rounded-2xl border border-slate-800">
            <div class="text-indigo-400 font-bold mb-1">📄 main.py</div>
            <p class="text-slate-400 font-sans text-xs mb-2">Bucle principal: gestiona turnos (quien acierta repite; quien falla cede turno) y condición de victoria.</p>
          </div>
        </div>
      </div>
    </div>

  </main>

  <footer class="max-w-6xl mx-auto mt-12 pt-6 border-t border-slate-900 text-center text-xs text-slate-500">
    Desarrollado para el Bootcamp de Data Science BBK · Bilbao, 2026. Proyecto "Hundir la Flota".
  </footer>

  <!-- LÓGICA DE JUEGO Y PRESENTACIÓN INTERACTIVA EN JAVASCRIPT -->
  <script>
    const DIM = 10;
    const FLEET_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1];
    
    let jugadorBoard = [];
    let maquinaBoard = [];
    let radarJugador = [];
    let vidasJugador = 20;
    let vidasMaquina = 20;
    let turno = 'jugador';
    let demoActive = false;
    let gameOver = false;

    // --- TEMPORIZADOR 10 MINUTOS ---
    let timerSeconds = 600;
    let timerInterval = null;

    function toggleTimer() {
      const btn = document.getElementById('timer-btn');
      if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
        btn.textContent = 'Reanudar';
        btn.classList.replace('bg-amber-600', 'bg-cyan-600');
      } else {
        timerInterval = setInterval(() => {
          if (timerSeconds > 0) {
            timerSeconds--;
            updateTimerDisplay();
          } else {
            clearInterval(timerInterval);
            timerInterval = null;
            alert("⏰ ¡Tiempo de presentación completado (10 minutos)!");
          }
        }, 1000);
        btn.textContent = 'Pausar';
        btn.classList.replace('bg-cyan-600', 'bg-amber-600');
      }
    }

    function resetTimer() {
      clearInterval(timerInterval);
      timerInterval = null;
      timerSeconds = 600;
      updateTimerDisplay();
      const btn = document.getElementById('timer-btn');
      btn.textContent = 'Iniciar';
      btn.classList.replace('bg-amber-600', 'bg-cyan-600');
    }

    function updateTimerDisplay() {
      const min = Math.floor(timerSeconds / 60);
      const sec = timerSeconds % 60;
      document.getElementById('timer-display').textContent = 
        `${String(min).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
    }

    // --- GENERACIÓN DE TABLERO CON BACKTRACKING EN JS (IDÉNTICO A PYTHON) ---
    function generarTableroConBacktracking() {
      let grid = Array(DIM).fill(null).map(() => Array(DIM).fill('~'));
      
      // Precalcular posiciones por eslora
      let posPorEslora = {};
      [4, 3, 2, 1].forEach(eslora => {
        let setPos = [];
        for (let r = 0; r < DIM; r++) {
          for (let c = 0; c <= DIM - eslora; c++) {
            let cells = [];
            for (let i = 0; i < eslora; i++) cells.push([r, c + i]);
            setPos.push(cells);
          }
        }
        for (let r = 0; r <= DIM - eslora; r++) {
          for (let c = 0; c < DIM; c++) {
            let cells = [];
            for (let i = 0; i < eslora; i++) cells.push([r + i, c]);
            setPos.push(cells);
          }
        }
        posPorEslora[eslora] = setPos;
      });

      function shuffle(arr) {
        let a = [...arr];
        for (let i = a.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [a[i], a[j]] = [a[j], a[i]];
        }
        return a;
      }

      function colocarSiguiente(idx) {
        if (idx === FLEET_SIZES.length) return true;
        let eslora = FLEET_SIZES[idx];
        let posiciones = shuffle(posPorEslora[eslora]);

        for (let cells of posiciones) {
          if (cells.every(([r, c]) => grid[r][c] === '~')) {
            cells.forEach(([r, c]) => grid[r][c] = 'B');
            if (colocarSiguiente(idx + 1)) return true;
            cells.forEach(([r, c]) => grid[r][c] = '~'); // Backtrack
          }
        }
        return false;
      }

      colocarSiguiente(0);
      return grid;
    }

    // --- INICIALIZACIÓN ---
    function iniciarNuevaPartida() {
      jugadorBoard = generarTableroConBacktracking();
      maquinaBoard = generarTableroConBacktracking();
      radarJugador = Array(DIM).fill(null).map(() => Array(DIM).fill('~'));
      vidasJugador = 20;
      vidasMaquina = 20;
      turno = 'jugador';
      gameOver = false;
      demoActive = false;

      document.getElementById('vidas-jugador').textContent = '20 / 20';
      document.getElementById('vidas-maquina').textContent = '20 / 20';
      actualizarTurnoBadge('Turno: Alumno BBK', 'bg-cyan-900/80', 'text-cyan-300');
      document.getElementById('mensaje-estado').innerHTML = 
        'Tableros inicializados con Backtracking. Haz clic en el <strong class="text-rose-400">Radar Ofensivo</strong> para disparar.';
      
      renderizarTableros();
    }

    function toggleDemoMode() {
      demoActive = !demoActive;
      const btn = document.getElementById('btn-demo');
      if (demoActive) {
        btn.classList.replace('text-amber-400', 'text-emerald-300');
        btn.classList.replace('bg-amber-950/40', 'bg-emerald-950/60');
        btn.innerHTML = '<span>👁️</span> Modo Demo Activo (Barcos Visibles)';
      } else {
        btn.classList.replace('text-emerald-300', 'text-amber-400');
        btn.classList.replace('bg-emerald-950/60', 'bg-amber-950/40');
        btn.innerHTML = '<span>👁️</span> Modo Demo / Tribunal (Revelar Rival)';
      }
      renderizarTableros();
    }

    function renderizarTableros() {
      // 1. Grid Jugador
      const gridJ = document.getElementById('grid-jugador');
      gridJ.innerHTML = '';
      for (let r = 0; r < DIM; r++) {
        let rowDiv = document.createElement('div');
        rowDiv.className = 'grid grid-cols-11 gap-1 items-center';
        
        let label = document.createElement('div');
        label.className = 'text-center text-slate-500 font-mono text-xs';
        label.textContent = r;
        rowDiv.appendChild(label);

        for (let c = 0; c < DIM; c++) {
          let cell = document.createElement('div');
          cell.className = 'h-7 md:h-8 rounded flex items-center justify-center font-bold text-xs transition border border-slate-800/80';
          const val = jugadorBoard[r][c];

          if (val === 'B') {
            cell.className += ' bg-cyan-700/80 text-cyan-200 border-cyan-500/60 shadow-sm';
            cell.textContent = '⛵';
          } else if (val === 'X') {
            cell.className += ' bg-rose-600 text-white font-black animate-pulse';
            cell.textContent = 'X';
          } else if (val === 'O') {
            cell.className += ' bg-slate-800 text-slate-400';
            cell.textContent = '·';
          } else {
            cell.className += ' bg-slate-950/80 text-slate-700 hover:bg-slate-900';
            cell.textContent = '~';
          }
          rowDiv.appendChild(cell);
        }
        gridJ.appendChild(rowDiv);
      }

      // 2. Grid Máquina (Radar)
      const gridM = document.getElementById('grid-maquina');
      gridM.innerHTML = '';
      for (let r = 0; r < DIM; r++) {
        let rowDiv = document.createElement('div');
        rowDiv.className = 'grid grid-cols-11 gap-1 items-center';
        
        let label = document.createElement('div');
        label.className = 'text-center text-slate-500 font-mono text-xs';
        label.textContent = r;
        rowDiv.appendChild(label);

        for (let c = 0; c < DIM; c++) {
          let cell = document.createElement('button');
          cell.className = 'h-7 md:h-8 rounded flex items-center justify-center font-bold text-xs transition border border-slate-800/80';
          const shot = radarJugador[r][c];
          const real = maquinaBoard[r][c];

          if (shot === 'X') {
            cell.className += ' bg-rose-600 text-white font-black cursor-not-allowed';
            cell.textContent = 'X';
          } else if (shot === 'O') {
            cell.className += ' bg-slate-800 text-slate-400 cursor-not-allowed';
            cell.textContent = '·';
          } else {
            // No disparado
            if (demoActive && real === 'B') {
              cell.className += ' bg-amber-900/60 border-amber-600/70 text-amber-300 hover:bg-amber-800';
              cell.textContent = '⛵';
            } else {
              cell.className += ' water-cell text-slate-600 hover:border-cyan-400';
              cell.textContent = '~';
            }
            if (!gameOver && turno === 'jugador') {
              cell.onclick = () => dispararJugador(r, c);
            } else {
              cell.className += ' cursor-not-allowed';
            }
          }
          rowDiv.appendChild(cell);
        }
        gridM.appendChild(rowDiv);
      }
    }

    function dispararJugador(r, c) {
      if (gameOver || turno !== 'jugador') return;
      if (radarJugador[r][c] !== '~') return;

      if (maquinaBoard[r][c] === 'B') {
        maquinaBoard[r][c] = 'X';
        radarJugador[r][c] = 'X';
        vidasMaquina--;
        document.getElementById('vidas-maquina').textContent = `${vidasMaquina} / 20`;

        if (vidasMaquina === 0) {
          gameOver = true;
          document.getElementById('mensaje-estado').innerHTML = 
            '🏆 <strong class="text-cyan-300">¡VICTORIA BBK!</strong> Has hundido toda la flota enemiga. ¡Excelente!';
          renderizarTableros();
          return;
        }

        document.getElementById('mensaje-estado').innerHTML = 
          `🎯 <strong class="text-cyan-400">¡IMPACTO en (${r}, ${c})!</strong> Barco rival tocado. <strong>¡Vuelves a disparar!</strong>`;
        renderizarTableros();
      } else {
        maquinaBoard[r][c] = 'O';
        radarJugador[r][c] = 'O';
        document.getElementById('mensaje-estado').innerHTML = 
          `🌊 <strong class="text-blue-400">¡AGUA en (${r}, ${c})!</strong> Cedes el turno a la máquina...`;
        turno = 'maquina';
        actualizarTurnoBadge('Turno: Máquina Pensando...', 'bg-rose-950/80', 'text-rose-300');
        renderizarTableros();
        
        // Disparo de la máquina tras pausa realista
        setTimeout(dispararMaquina, 900);
      }
    }

    function dispararMaquina() {
      if (gameOver || turno !== 'maquina') return;

      let disponibles = [];
      for (let r = 0; r < DIM; r++) {
        for (let c = 0; c < DIM; c++) {
          if (jugadorBoard[r][c] !== 'X' && jugadorBoard[r][c] !== 'O') {
            disponibles.push([r, c]);
          }
        }
      }

      if (disponibles.length === 0) return;
      let [r, c] = disponibles[Math.floor(Math.random() * disponibles.length)];

      if (jugadorBoard[r][c] === 'B') {
        jugadorBoard[r][c] = 'X';
        vidasJugador--;
        document.getElementById('vidas-jugador').textContent = `${vidasJugador} / 20`;

        if (vidasJugador === 0) {
          gameOver = true;
          document.getElementById('mensaje-estado').innerHTML = 
            '💀 <strong class="text-rose-400">¡DERROTA!</strong> La máquina ha destruido todos tus barcos.';
          renderizarTableros();
          return;
        }

        document.getElementById('mensaje-estado').innerHTML = 
          `💥 <strong class="text-rose-400">¡La máquina impactó en (${r}, ${c})!</strong> Acierta y vuelve a tirar...`;
        renderizarTableros();
        setTimeout(dispararMaquina, 1000);
      } else {
        jugadorBoard[r][c] = 'O';
        document.getElementById('mensaje-estado').innerHTML = 
          `🛡️ La máquina disparó a <strong>(${r}, ${c})</strong> y dio en AGUA. ¡Te toca!`;
        turno = 'jugador';
        actualizarTurnoBadge('Turno: Alumno BBK', 'bg-cyan-900/80', 'text-cyan-300');
        renderizarTableros();
      }
    }

    function actualizarTurnoBadge(texto, bg, color) {
      const b = document.getElementById('turno-badge');
      b.textContent = texto;
      b.className = `px-2.5 py-0.5 rounded-full text-xs font-bold border border-current ${bg} ${color}`;
    }

    function showTab(tab) {
      ['juego', 'guion', 'arquitectura'].forEach(t => {
        document.getElementById(`tab-${t}`).classList.add('hidden');
        document.getElementById(`tab-btn-${t}`).classList.remove('border-cyan-400', 'text-cyan-400');
        document.getElementById(`tab-btn-${t}`).classList.add('border-transparent', 'text-slate-400');
      });
      document.getElementById(`tab-${tab}`).classList.remove('hidden');
      document.getElementById(`tab-btn-${tab}`).classList.add('border-cyan-400', 'text-cyan-400');
      document.getElementById(`tab-btn-${tab}`).classList.remove('border-transparent', 'text-slate-400');
    }

    // Arrancar la primera partida al cargar
    iniciarNuevaPartida();
  </script>
</body>
</html>
```
