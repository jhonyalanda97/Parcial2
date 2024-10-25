from itertools import product

# Función para verificar una proposición lógica en un modelo
def evaluar_proposicion(proposicion, modelo):
    """
    Evalúa una proposición con base en un modelo de verdad.
    El modelo es un diccionario que asigna True/False a proposiciones básicas.
    """
    # Reemplazamos las proposiciones en el modelo por sus valores de verdad
    for var, valor in modelo.items():
        proposicion = proposicion.replace(var, str(valor))
    
    # Evaluamos la expresión lógica
    return eval(proposicion)

# Función de chequeo de modelo
def chequeo_de_modelo(kb, proposicion, variables):
    """
    Verifica si una proposición es verdadera en todos los modelos que satisfacen la base de conocimiento (KB).
    
    kb: Lista de proposiciones en la base de conocimiento.
    proposicion: La proposición a verificar.
    variables: Las proposiciones básicas usadas en la KB y proposición.
    """
    # Generamos todas las combinaciones posibles de verdad para las variables
    modelos = list(product([True, False], repeat=len(variables)))
    
    # Recorremos cada posible modelo de verdad
    for modelo_valores in modelos:
        modelo = dict(zip(variables, modelo_valores))  # Creamos el modelo como diccionario
        
        # Verificamos si el modelo satisface todas las proposiciones de la base de conocimiento
        kb_satisfecha = all(evaluar_proposicion(kb_proposicion, modelo) for kb_proposicion in kb)
        
        if kb_satisfecha:
            # Si la KB es verdadera bajo este modelo, verificamos la proposición
            proposicion_valida = evaluar_proposicion(proposicion, modelo)
            
            if not proposicion_valida:
                # Si la proposición es falsa en un modelo que satisface la KB, no es válida
                return False
    
    # Si la proposición es verdadera en todos los modelos que satisfacen la KB, es válida
    return True

# Ejemplo de uso

# Base de conocimiento (KB)
kb = [
    "(P or Q)",  # P o Q
    "not Q or R" # Si no Q, entonces R
]

# Proposición a verificar
proposicion = "P -> R"  # Si P entonces R

# Variables presentes en la KB y la proposición
variables = ["P", "Q", "R"]

# Verificamos si la proposición es válida en la base de conocimiento
resultado = chequeo_de_modelo(kb, proposicion, variables)

if resultado:
    print("La proposición es verdadera en el modelo que satisface la base de conocimiento.")
else:
    print("La proposición es falsa en al menos un modelo que satisface la base de conocimiento.")