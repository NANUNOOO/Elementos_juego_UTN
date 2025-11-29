#generamos los powerups y sus contras.

import random

tipo_de_efectos = ("Fuego", "Hoja", "Gota", "Viento", "Nada", "Nada", "Nada", "Nada")

decision = random.choice(tipo_de_efectos)

print (decision)


match tipo_de_efectos:
    
    case 