# Importar fracciones para manejar números racionales
from fractions import Fraction


######################################################
##################### Utilidades #####################
######################################################

def nueva_matriz(filas, columnas, datos):
    return {
        'filas': filas,
        'columnas': columnas,
        'datos': [[Fraction(x) for x in fila] for fila in datos]
    }


def duplicar_matriz(matriz):
    return nueva_matriz(matriz['filas'], matriz['columnas'],
                         [fila[:] for fila in matriz['datos']])


def matriz_string(matriz):
    return '\n'.join([' '.join(map(str, fila)) for fila in matriz['datos']])


def input_matriz(contador = 0):
    while True:
        try:
            filas = int(input(f"Ingrese la cantidad de filas de la matriz{f' {contador}' if contador > 0 else ''}: "))
            columnas = int(input(f"Ingrese la cantidad de columnas de la matriz{f' {contador}' if contador > 0 else ''}: "))
            if filas <= 0 or columnas <= 0:
                print("Las dimensiones deben ser un número positivo y entero")
                continue

            matriz = []
            for i in range(filas):
                while True:
                    fila = input(f"Ingrese los números de la fila {i + 1} separados por un espacio (ejemplo: {' '.join(['#'] * columnas)}) si desea dejar espacios vacios escriba 0: ").split()
                    if len(fila) != columnas:
                        print(f"Debes ingresar exactamente {columnas} números")
                        continue
                    try:
                        matriz.append([float(x) for x in fila])
                        break
                    except ValueError:
                        print("Formato no válido")
            return nueva_matriz(filas, columnas, matriz)
        except ValueError:
            print("Las dimensiones deben ser un número positivo y entero")


def input_escalar():
    while True:
        try:
            return float(input("Ingrese el valor del escalar: "))
        except ValueError:
            print("Valor no válido")


######################################################
################ Funciones Algebraicas ###############
######################################################

def sumar_matrices(matriz1, matriz2):
    if matriz1['filas'] != matriz2['filas'] or matriz1['columnas'] != matriz2['columnas']:
        raise ValueError("Matrices deben tener las mismas dimensiones")

    resultado = [
        [matriz1['datos'][i][j] + matriz2['datos'][i][j] for j in range(matriz1['columnas'])]
        for i in range(matriz1['filas'])
    ]
    return nueva_matriz(matriz1['filas'], matriz1['columnas'], resultado)


def restar_matrices(matriz1, matriz2):
    if matriz1['filas'] != matriz2['filas'] or matriz1['columnas'] != matriz2['columnas']:
        raise ValueError("Matrices deben tener las mismas dimensiones")

    resultado = [
        [matriz1['datos'][i][j] - matriz2['datos'][i][j] for j in range(matriz1['columnas'])]
        for i in range(matriz1['filas'])
    ]
    return nueva_matriz(matriz1['filas'], matriz1['columnas'], resultado)


def multiplicar_matrices(matriz1, matriz2):
    if matriz1['columnas'] != matriz2['filas']:
        raise ValueError("El número de columnas de la primera matriz deben == al numero de filas de la segunda matriz")

    resultado = []
    explicacion = []

    for i in range(matriz1['filas']):
        fila = []
        for j in range(matriz2['columnas']):
            total = 0
            pasos = []
            for k in range(matriz1['columnas']):
                producto = matriz1['datos'][i][k] * matriz2['datos'][k][j]
                total += producto
                pasos.append(f"({matriz1['datos'][i][k]}×{matriz2['datos'][k][j]})")
            fila.append(total)
            explicacion.append(f"Elemento [{i + 1},{j + 1}]: {' + '.join(pasos)} = {total}")
        resultado.append(fila)

    return nueva_matriz(matriz1['filas'], matriz2['columnas'], resultado), explicacion


def multiplicar_matrices_escalar(matriz, escalar):
    resultado = [
        [element * escalar for element in fila]
        for fila in matriz['datos']
    ]
    return nueva_matriz(matriz['filas'], matriz['columnas'], resultado)


def calcular_determinante(matriz):
    if matriz['filas'] != matriz['columnas']:
        raise ValueError("El determinante solo se puede calcular para matrices cuadradas")

    datos = matriz['datos']
    if matriz['filas'] == 1:
        return datos[0][0]

    try:
        def submatriz(datos_matriz, fila, columna):
            return [[datos_matriz[i][j] for j in range(len(datos_matriz)) if j != columna]
                    for i in range(len(datos_matriz)) if i != fila]

        return sum((-1) ** c * datos[0][c] * calcular_determinante(
            nueva_matriz(matriz['filas'] - 1, matriz['columnas'] - 1, submatriz(datos, 0, c))
        ) for c in range(matriz['columnas']))
    except Exception as e:
        raise ValueError(f"Error al calcular el determinante: {e}")


def calcular_inversa(matriz, metodo="adjuncion"):
    if matriz['filas'] != matriz['columnas']:
        raise ValueError("La inversa solo se puede calcular para matrices cuadradas")

    determinante = calcular_determinante(matriz)
    if determinante == 0:
        raise ValueError("La matriz no tiene inversa porque su determinante es 0")

    pasos = []
    datos = matriz['datos']
    n = matriz['filas']

    if metodo == "a":
        try:
            adjunta = [[(-1) ** (i + j) * calcular_determinante(
                nueva_matriz(n - 1, n - 1, [fila[:j] + fila[j + 1:] for fila in (datos[:i] + datos[i + 1:])])
            ) for j in range(n)] for i in range(n)]

            print("Paso 1: Calcular la matriz adjunta.")
            print('\n'.join([' '.join(map(str, fila)) for fila in adjunta]))
            print("Paso 2: Dividir cada elemento de la adjunta por el determinante.")
            inversa = [[Fraction(adjunta[j][i], determinante) for j in range(n)] for i in range(n)]
            return nueva_matriz(n, n, inversa)
        except Exception as e:
            raise ValueError(f"Error al calcular la inversa por adjunción: {e}")

    elif metodo == "g":
        try:
            matriz_extendida = [fila + [Fraction(1) if i == j else Fraction(0) for j in range(n)]
                                for i, fila in enumerate(datos)]

            pasos.append("Paso 1: Formar la matriz aumentada con la matriz identidad.")
            pasos.append('\n'.join([' '.join(map(str, fila[:n])) + " | " + ' '.join(map(str, fila[n:]))
                                    for fila in matriz_extendida]))

            for i in range(n):
                if matriz_extendida[i][i] == 0:
                    raise ValueError(
                        "No se puede calcular la inversa con el método de Gauss-Jordan debido a un pivote cero")

                pivote = matriz_extendida[i][i]
                matriz_extendida[i] = [round(x / pivote, 3) for x in matriz_extendida[i]]
                pasos.append(f"Paso {i + 2}: Hacer el pivote {pivote} igual a 1 dividiendo la fila {i + 1}.")
                pasos.append('\n'.join([' '.join(map(str, fila[:n])) + " | " + ' '.join(map(str, fila[n:]))
                                        for fila in matriz_extendida]))

                for j in range(n):
                    if i != j:
                        factor = matriz_extendida[j][i]
                        matriz_extendida[j] = [round(matriz_extendida[j][k] - factor * matriz_extendida[i][k], 3)
                                               for k in range(2 * n)]
                        pasos.append(f"Reducir la fila {j + 1} usando la fila {i + 1}.")
                        pasos.append('\n'.join([' '.join(map(str, fila[:n])) + " | " + ' '.join(map(str, fila[n:]))
                                                for fila in matriz_extendida]))

            inversa = [fila[n:] for fila in matriz_extendida]
            pasos.append("Resultado final:")
            pasos.append('\n'.join([' '.join(map(str, fila)) for fila in inversa]))
            print("\n".join(pasos))
            return nueva_matriz(n, n, inversa)
        except Exception as e:
            raise ValueError(f"Error al calcular la inversa por Gauss-Jordan: {e}")

    else:
        raise ValueError("Método no reconocido. Use 'adjuncion' o 'gauss-jordan'")


def eliminar_gauss_jordan(matriz):
    n = matriz['filas']
    m = matriz['columnas']
    datos = [fila[:] for fila in matriz['datos']]
    pasos = []

    for i in range(n):
        if datos[i][i] == 0:
            for j in range(i + 1, n):
                if datos[j][i] != 0:
                    datos[i], datos[j] = datos[j], datos[i]
                    pasos.append(f"Intercambiar fila {i + 1} con fila {j + 1}")
                    break
            else:
                raise ValueError("No se puede aplicar Gauss-Jordan, pivote cero sin intercambios posibles.")

        pivote = datos[i][i]
        datos[i] = [x / pivote for x in datos[i]]
        pasos.append(f"Dividir fila {i + 1} por {pivote}")

        for j in range(n):
            if i != j:
                factor = datos[j][i]
                datos[j] = [datos[j][k] - factor * datos[i][k] for k in range(m)]
                pasos.append(f"Restar {factor} veces la fila {i + 1} de la fila {j + 1}")

    pasos.append("Resultado final:")
    pasos.append('\n'.join([' '.join(map(str, fila)) for fila in datos]))
    print("\n".join(pasos))
    return nueva_matriz(n, m, datos)


def resolver_cramer(matriz_aumentada):
    if matriz_aumentada['filas'] != matriz_aumentada['columnas'] - 1:
        raise ValueError("La matriz aumentada debe tener una columna más que filas")

    n = matriz_aumentada['filas']
    datos = matriz_aumentada['datos']

    A_datos = [fila[:-1] for fila in datos]
    b_datos = [[fila[-1]] for fila in datos]

    A = nueva_matriz(n, n, A_datos)
    b = nueva_matriz(n, 1, b_datos)

    det_A = calcular_determinante(A)
    if det_A == 0:
        raise ValueError("El determinante de A es 0, el sistema no tiene solución única")

    soluciones = []
    explicacion = []

    for i in range(n):
        A_i = duplicar_matriz(A)

        for j in range(n):
            A_i['datos'][j][i] = b['datos'][j][0]

        det_A_i = calcular_determinante(A_i)

        x_i = Fraction(det_A_i, det_A)
        soluciones.append(x_i)

        explicacion.append(f"x_{i + 1} = det(A_{i + 1}) / det(A) = {det_A_i} / {det_A} = {x_i}")

    return soluciones, explicacion


######################################################
################## Función Princiapl #################
######################################################

def main():
    while True:
        print("\nCalculadora de Álgebra Lineal")
        print("Seleccione una operación:")
        print("1. Sumar matrices")
        print("2. Restar matrices")
        print("3. Multiplicar matrices/escalares")
        print("4. Obtener determinante")
        print("5. Inversa de matriz (Adjunción o Gauss-Jordan)")
        print("6. Eliminación de Gauss-Jordan")
        print("7. Regla de Cramer")
        print("8. Salir")

        opcion = input("Seleccione una opción (1-8): ")

        match opcion:
            case '1':  # Suma de matrices
                try:
                    contador = int(input("Ingrese la cantidad de matrices a sumar: "))
                    if contador < 2:
                        print("Se requieren al menos 2 matrices para sumar")
                        continue
                except ValueError:
                    print("Número invalido")
                    continue

                operandos = []
                for i in range(contador):
                    operandos.append(input_matriz((i + 1)))

                resultado = operandos[0]
                pasos = []

                # Realizar las sumas secuencialmente
                for i in range(1, len(operandos)):
                    try:
                        nuevo_resultado = sumar_matrices(resultado, operandos[i])
                        resultado_str = matriz_string(resultado)
                        operando_str = matriz_string(operandos[i])
                        nuevo_resultado_str = matriz_string(nuevo_resultado)

                        pasos.append(f"{resultado_str}\n+\n{operando_str}\n=\n{nuevo_resultado_str}\n")
                        resultado = nuevo_resultado
                    except ValueError as e:
                        print(f"Error: {e}")
                        break

                # Mostrar los pasos y el resultado
                if pasos:
                    print("\nSOLUCIÓN PASO A PASO:")
                    for paso in pasos:
                        print(paso)
                    print("\nRESULTADO:")
                    print(matriz_string(resultado))

            case '2':  # Resta de matrices
                try:
                    contador = int(input("Ingrese la cantidad de matrices a restar: "))
                    if contador < 2:
                        print("Se requieren al menos 2 matrices para restar")
                        continue
                except ValueError:
                    print("Número invalido")
                    continue

                operandos = []
                for i in range(contador):
                    operandos.append(input_matriz((i + 1)))

                # Inicializar los pasos y el resultado
                resultado = operandos[0]
                pasos = []

                # Realizar las restas secuencialmente
                for i in range(1, len(operandos)):
                    try:
                        nuevo_resultado = restar_matrices(resultado, operandos[i])
                        resultado_str = matriz_string(resultado)
                        operando_str = matriz_string(operandos[i])
                        nuevo_resultado_str = matriz_string(nuevo_resultado)

                        pasos.append(f"{resultado_str}\n-\n{operando_str}\n=\n{nuevo_resultado_str}\n")
                        resultado = nuevo_resultado
                    except ValueError as e:
                        print(f"Error: {e}")
                        break

                # Mostrar los pasos y el resultado
                if pasos:
                    print("\nSOLUCIÓN PASO A PASO:")
                    for paso in pasos:
                        print(paso)
                    print("\nRESULTADO:")
                    print(matriz_string(resultado))

            case '3':  # Multiplicación
                try:
                    contador = int(input("Ingrese cuantas matrices o escalares desea multiplicar: "))
                    if contador < 2:
                        print("Se requieren al menos 2 operandos para multiplicar")
                        continue
                except ValueError:
                    print("Número invalido")
                    continue

                operandos = []
                for i in range(contador):
                    opcion_multi = input(f"El operando {i + 1} es escalar (e) o matriz (m)? ").lower()
                    if  opcion_multi == 'e':
                        operandos.append(input_escalar())
                    elif opcion_multi == 'm':
                        operandos.append(input_matriz((i + 1)))
                    else:
                        print("Opción invalida")
                        break

                # Inicializar los pasos y el resultado
                resultado = operandos[0]
                pasos = []

                # Realizar las multiplicaciones secuencialmente
                for i in range(1, len(operandos)):
                    try:
                        # Comprobar si la operación es escalar
                        actual_es_escalar = isinstance(resultado, (int, float))
                        prox_es_escalar = isinstance(operandos[i], (int, float))

                        if actual_es_escalar or prox_es_escalar:
                            # Manejar multiplicación escalar
                            if actual_es_escalar and prox_es_escalar:
                                # Ambos son escalares
                                nuevo_resultado = resultado * operandos[i]
                                explicacion = []
                                simbolo_op = '×'
                            elif actual_es_escalar:
                                # Escalar * Matriz
                                escalar = resultado
                                matriz = operandos[i]
                                nuevo_resultado = multiplicar_matrices_escalar(matriz, escalar)
                                explicacion = []
                                simbolo_op = '× scalar'
                            else:
                                # Matriz * Escalar
                                escalar = operandos[i]
                                nuevo_resultado = multiplicar_matrices_escalar(resultado, escalar)
                                explicacion = []
                                simbolo_op = '× scalar'
                        else:
                            # Multiplicación de matrices
                            nuevo_resultado, explicacion = multiplicar_matrices(resultado, operandos[i])
                            simbolo_op = '×'

                        # Agregar explicación si existe
                        if explicacion:
                            pasos.extend(explicacion)

                        # Formato de cadenas para mostrar
                        resultado_str = resultado if isinstance(resultado, (int, float)) else matriz_string(resultado)
                        operando_str = operandos[i] if isinstance(operandos[i], (int, float)) else matriz_string(
                            operandos[i])
                        nuevo_resultado_str = nuevo_resultado if isinstance(nuevo_resultado,
                                                                            (int, float)) else matriz_string(
                            nuevo_resultado)

                        pasos.append(f"{resultado_str}\n{simbolo_op}\n{operando_str}\n=\n{nuevo_resultado_str}\n")
                        resultado = nuevo_resultado
                    except ValueError as e:
                        print(f"Error: {e}")
                        break

                # Mostrar los pasos y el resultado
                if pasos:
                    print("\nSOLUCIÓN PASO A PASO:")
                    for paso in pasos:
                        print(paso)
                    print("\nRESULTADO:")
                    if isinstance(resultado, (int, float)):
                        print(resultado)
                    else:
                        print(matriz_string(resultado))

            case '4':
                matriz = input_matriz()
                try:
                    determinante = calcular_determinante(matriz)
                    print(f"El determinante de la matriz es: {determinante}")
                except ValueError as e:
                    print(f"Error: {e}")

            case '5':
                matriz = input_matriz()
                metodo = input("Desea usar adjuncion o gauss-jordan (responda con a o g respectivamente): ").lower()
                try:
                    inversa = calcular_inversa(matriz, metodo)
                    print("La inversa de la matriz es:")
                    print(matriz_string(inversa))
                except ValueError as e:
                    print(f"Error: {e}")

            case '6':
                matriz = input_matriz()
                try:
                    resultado = eliminar_gauss_jordan(matriz)
                    print("\nSolución del sistema:")
                    # Mostrar x_n resultantes
                    for i in range(resultado['filas']):
                        print(f"x_{i + 1} = {resultado['datos'][i][-1]}")

                except ValueError as e:
                    print(f"Error: {e}")

            case '7':  # Regla de Cramer
                print("\nResolver sistema de ecuaciones con regla de Cramer")
                print(
                    "Ingrese la matriz aumentada [A | b] donde A es la matriz de coeficientes y b es el vector de términos independientes")
                print("Ejemplo para un sistema 2x2: ax + by = c, dx + ey = f")
                print("La matriz aumentada sería:")
                print("a b | c")
                print("d e | f\n")

                matriz_aumentada = input_matriz()

                try:
                    soluciones, explicacion = resolver_cramer(matriz_aumentada)

                    print("\nSOLUCIÓN PASO A PASO:")
                    # Mostrar la matriz original
                    print("Matriz aumentada [A | b]:")
                    print(matriz_string(matriz_aumentada))

                    # Extraer matriz A para calcular su determinante
                    n = matriz_aumentada['filas']
                    A_datos = [fila[:-1] for fila in matriz_aumentada['datos']]
                    A = nueva_matriz(n, n, A_datos)

                    det_A = calcular_determinante(A)
                    print(f"\nDeterminante de la matriz de coeficientes A: {det_A}")

                    if det_A == 0:
                        print("El sistema no tiene solución única porque el determinante de A es 0")
                    else:
                        print("\nCalculando cada incógnita:")
                        for i in range(len(explicacion)):
                            print(explicacion[i])

                        print("\nSolución del sistema:")
                        for i, sol in enumerate(soluciones):
                            print(f"x_{i + 1} = {sol}")

                except ValueError as e:
                    print(f"Error: {e}")

            case '8':
                break

            case _:
                print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()