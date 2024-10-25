# Función para imprimir la tabla de verdad de la compuerta OR
def tabla_verdad_or():
    print("A\tB\tA OR B")
    print("-------------------")
    for A in [0, 1]:
        for B in [0, 1]:
            resultado = A or B
            print(f"{A}\t{B}\t{resultado}")

# Llamar a la función
tabla_verdad_or()
