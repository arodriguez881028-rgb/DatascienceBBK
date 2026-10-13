#%% ==========================================
# EJERCICIO 1
# ==========================================
# Dada la siguiente lista:
# ejer_1 = [1, 2, 3, 4, 5]
#
# Inviértela para que quede de la siguiente manera:
# ejer_1 = [5, 4, 3, 2, 1]
# (Prueba varias formas: slicing, reverse(), reversed(), etc.)

ejer_1 = [1, 2, 3, 4, 5]
print ("_"*50)
# Forma 1 (Slicing)
inv_1 = ejer_1[::-1]
print (f"Forma slicing ,{inv_1}")
print ("_"*50)
# Forma 2 (Método reverse)
ejer_1.reverse()
inv_2 = ejer_1
print (f"Metodo reverse,{inv_2}")
print ("_"*50)
# Forma 3 (Función reversed)
ejer_1_orig = [1, 2, 3, 4, 5]
inv_3 = list(reversed(ejer_1_orig))
print (f"Función reverse,{inv_2}")
print("Ejercicio 1:", inv_1, inv_2, inv_3)


#%% ==========================================
# EJERCICIO 2
# ==========================================
# Eleva todos los elementos de la lista al cuadrado
# ejer_2 = [1, 2, 3, 4, 5]

ejer_2 = [1, 2, 3, 4, 5]
ejer_2_cuadrados = [x ** 2 for x in ejer_2]

print("Ejercicio 2:", ejer_2_cuadrados)
print ("_"*50)
#%% ==========================================
# EJERCICIO 3
# ==========================================
# Crea una lista nueva con todas las combinaciones de las siguientes dos listas:
# ejer_3_1 = ["Hola", "amigo"]
# ejer_3_2 = ["Que", "tal"]
#
# Obten el siguiente output:
# ['Hola Que', 'Hola tal', 'amigo Que', 'amigo tal']
print ("_"*60)
print ("_"*60)


ejer_3_1 = ["Hola", "amigo"]
ejer_3_2 = ["Que", "tal"]

ejer_3_1 = ["Hola", "amigo"]
ejer_3_2 = ["Que", "tal"]

# Doble bucle en list comprehension
ejer_3_res = [f"{palabra1} {palabra2}" for palabra1 in ejer_3_1 for palabra2 in ejer_3_2]

print("Ejercicio 3:", ejer_3_res)



#%% ==========================================
# EJERCICIO 4
# ==========================================
# Dada la siguiente lista, encuentra por el índice el valor 45 y sustitúyelo por el 0
ejer_4 = [20, 47, 19, 29, 45, 67, 78, 90]

indice_45 = ejer_4.index(45)
ejer_4[indice_45] = 0

print("Ejercicio 4:", ejer_4)
print("_" * 50)


#%% ==========================================
# EJERCICIO 5
# ==========================================
# Dada la siguiente lista, elimina todos los valores iguales a 3
# TIP: No intentes eliminar elementos sobre la lista que estás iterando. Haz una copia con ejer_5.copy()
ejer_5 = [3, 20, 3, 47, 19, 3, 29, 45, 67, 78, 90, 3, 3]

# Usando list comprehension sobre una copia de la lista
ejer_5_res = [x for x in ejer_5.copy() if x != 3]

print("Ejercicio 5:", ejer_5_res)
print("_" * 50)


#%% ==========================================
# EJERCICIO 6
# ==========================================
# 1. Crea una tupla con 3 elementos
tupla_1 = (10, 20, 30)

# 2. Crea otra tupla con un elemento y comprueba su tipo (requiere la coma final)
tupla_un_elemento = (5,)
print("Ejercicio 6.2 - Tipo:", type(tupla_un_elemento))

# 3. Crea una tupla con elementos de diferentes tipos
tupla_variada = ("Python", 3.14, True, 100)

# 4. Imprime primer y último elemento (usando len para el último)
print("Ejercicio 6.4 - Primer elemento:", tupla_variada[0])
print("Ejercicio 6.4 - Último elemento:", tupla_variada[len(tupla_variada) - 1])

# 5. Añade un elemento a la tupla (las tuplas son inmutables, se concatenan)
tupla_ampliada = tupla_variada + ("Nuevo elemento",)
print("Ejercicio 6.5:", tupla_ampliada)

# 6. Eliminar un elemento de la mitad (pasando temporalmente a lista o mediante slicing)
# La tupla ampliada tiene 5 elementos; eliminamos el de la mitad (índice 2)
tupla_sin_mitad = tupla_ampliada[:2] + tupla_ampliada[3:]
print("Ejercicio 6.6:", tupla_sin_mitad)

# 7. Convierte la tupla del apartado 5 en una lista
lista_desde_tupla = list(tupla_ampliada)
print("Ejercicio 6.7:", lista_desde_tupla)
print("_" * 50)


#%% ==========================================
# EJERCICIO 7
# ==========================================
# Concatena todos los elementos de la tupla en un único string usando .join()
ejer_7 = ("cien", "cañones", "por", "banda")

resultado_7 = " ".join(ejer_7)
print("Ejercicio 7:", resultado_7)
print("_" * 50)


#%% ==========================================
# EJERCICIO 8
# ==========================================
# Obtén el tercer elemento y el tercero empezando por la cola
ejer_8 = (3, 20, 3, 47, 19, 3, 29, 45, 67, 78, 90, 3, 3)

tercero = ejer_8[2]
tercero_cola = ejer_8[-3]

print("Ejercicio 8 - Tercer elemento:", tercero)
print("Ejercicio 8 - Tercero por la cola:", tercero_cola)
print("_" * 50)


#%% ==========================================
# EJERCICIO 9
# ==========================================
ejer_9 = (3, 20, 3, 47, 19, 3, 29, 45, 67, 78, 90, 3, 3, 5, 2, 4, 7, 9, 4, 2, 4, 3, 3, 4, 6, 7)

# 1. ¿Cuántas veces se repite el 3?
veces_tres = ejer_9.count(3)
print("Ejercicio 9.1 - Veces que se repite el 3:", veces_tres)

# 2. Tupla nueva con los elementos desde la posición 5 a la 10 (incluyendo el 10)
sub_tupla = ejer_9[5:11]
print("Ejercicio 9.2 - Posición 5 a 10:", sub_tupla)

# 3. ¿Cuántos elementos tiene la tupla?
num_elementos = len(ejer_9)
print("Ejercicio 9.3 - Total elementos:", num_elementos)

# 4. Comprueba si el número 60 está en la tupla
esta_60 = 60 in ejer_9
print("Ejercicio 9.4 - ¿Está el 60?:", esta_60)
print("_" * 50)


#%% ==========================================
# EJERCICIO 10
# ==========================================
# 1. Convierte la tupla del ejercicio 9 en una lista
lista_ejer10 = list(ejer_9)

# 2. Convierte la tupla del ejercicio 9 en un set
set_ejer10 = set(ejer_9)

# 3. Convierte la tupla del ejercicio 9 en un diccionario usando los índices como claves
dict_ejer10 = {i: val for i, val in enumerate(ejer_9)}

print("Ejercicio 10.1 (Lista - primeros 5):", lista_ejer10[:5])
print("Ejercicio 10.2 (Set):", set_ejer10)
print("Ejercicio 10.3 (Diccionario - primeros 5 items):", list(dict_ejer10.items())[:5])
print("_" * 50)


#%% ==========================================
# EJERCICIO 11
# ==========================================
# Convierte la siguiente lista en un diccionario agrupando por clave:
ejer_11 = [("x", 1), ("x", 2), ("x", 3), ("y", 1), ("y", 2), ("z", 1)]

dic_ejer11 = {}
for clave, valor in ejer_11:
    if clave not in dic_ejer11:
        dic_ejer11[clave] = []
    dic_ejer11[clave].append(valor)

print("Ejercicio 11:", dic_ejer11)
print("_" * 50)


#%% ==========================================
# EJERCICIO 12
# ==========================================
ejer_12 = {4: 78, 2: 98, 8: 234, 5: 29}

# 1. Lista ordenada ascendente con las claves
claves_asc = sorted(list(ejer_12.keys()))
print("Ejercicio 12.1 (Claves asc):", claves_asc)

# 2. Lista ordenada descendente con los valores
valores_desc = sorted(list(ejer_12.values()), reverse=True)
print("Ejercicio 12.2 (Valores desc):", valores_desc)

# 3. Añade una nueva clave/valor
ejer_12[10] = 500
print("Ejercicio 12.3 (Diccionario actualizado):", ejer_12)

# 4. Busca la clave igual a 2 dentro del diccionario
existe_2 = 2 in ejer_12
print("Ejercicio 12.4 (¿Existe clave 2?):", existe_2, "Valor:", ejer_12.get(2))

# 5. Itera la clave y el valor del diccionario con un único for
print("Ejercicio 12.5 (Iteración):")
for k, v in ejer_12.items():
    print(f"  Clave: {k} -> Valor: {v}")
print("_" * 50)


#%% ==========================================
# EJERCICIO 13
# ==========================================
# Junta ambos diccionarios usando update
ejer_13_1 = {1: 11, 2: 22}
ejer_13_2 = {3: 33, 4: 44}

ejer_13_1.update(ejer_13_2)
print("Ejercicio 13:", ejer_13_1)
print("_" * 50)


#%% ==========================================
# EJERCICIO 14
# ==========================================
# Suma todos los valores del diccionario
ejer_14 = {1: 11, 2: 22, 3: 33, 4: 44, 5: 55}

suma_valores = sum(ejer_14.values())
print("Ejercicio 14:", suma_valores)
print("_" * 50)


#%% ==========================================
# EJERCICIO 15
# ==========================================
# Multiplica todos los valores del diccionario
ejer_15 = {1: 11, 2: 22, 3: 33, 4: 44, 5: 55}

from math import prod
multiplicacion_valores = prod(ejer_15.values())
print("Ejercicio 15:", multiplicacion_valores)
print("_" * 50)


#%% ==========================================
# EJERCICIO 16
# ==========================================
# 1. Crea un set de tres elementos
mi_set = {10, 20, 30}

# 2. Añade un cuarto
mi_set.add(40)
print("Ejercicio 16.2:", mi_set)

# 3. Elimina el último elemento añadido (o uno específico utilizando discard/remove)
mi_set.discard(40)
print("Ejercicio 16.3:", mi_set)

# 4. Elimina el elemento 10 si está presente usando discard() (evita errores si no existe)
mi_set.discard(10)
print("Ejercicio 16.4 (tras discard de 10):", mi_set)
print("_" * 50)