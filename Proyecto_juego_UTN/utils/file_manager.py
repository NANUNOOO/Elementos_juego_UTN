import os

def leer_ranking_desde_archivo():
    nombre_archivo_puntajes = "ranking.txt" # Cambiado a ranking.txt
    lista_mejores_puntajes = []
    
    if os.path.exists(nombre_archivo_puntajes):
        with open(nombre_archivo_puntajes, "r") as archivo_lectura:
            for linea_texto in archivo_lectura:
                datos_jugador = linea_texto.strip().split(",")
                if len(datos_jugador) == 2:
                    nombre_jugador = datos_jugador[0]
                    puntaje_jugador = int(datos_jugador[1])
                    lista_mejores_puntajes.append((nombre_jugador, puntaje_jugador))
        
    lista_mejores_puntajes.sort(key=lambda x: x[1], reverse=True)
    return lista_mejores_puntajes[:5]

def guardar_nuevo_puntaje(nombre_jugador, puntaje_obtenido):
    nombre_archivo_puntajes = "ranking.txt" # Cambiado a ranking.txt
    with open(nombre_archivo_puntajes, "a") as archivo_escritura:
        archivo_escritura.write(f"{nombre_jugador},{puntaje_obtenido}\n")