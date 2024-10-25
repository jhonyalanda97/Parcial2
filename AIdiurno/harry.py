from logic import *

rain = False         # True si llueve, False si no
bbc = False          # True si los estudiantes visitaron BBC
unimayor = True      # True si los estudiantes visitaron Unimayor

# Conocimiento:
# Si no llueve, los estudiantes visitan BBC
if not rain:
    bbc = True

# Los estudiantes visitaron BBC o Unimayor pero no ambos (XOR)
bbc_unimayor = (bbc or unimayor) and not (bbc and unimayor)

# Los estudiantes visitaron Unimayor
unimayor = True  # Afirmación directa

# Inferencia sobre BBC y el clima
print("¿Los estudiantes visitaron BBC?", bbc)
print("¿Llovió?", rain)