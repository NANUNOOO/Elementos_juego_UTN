# 1. Librerías estándar de Python
import random
import sys
import pygame

# 2. Nuestras librerías locales
from constantes import *
import funciones 

# --- INICIALIZACIÓN DE PYGAME Y RECURSOS ---
pygame.init()

# Configuración de ventana
ventana_principal = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption(NOMBRE_DEL_JUEGO)
reloj_control = pygame.time.Clock()

# Cargar imágenes y fuentes (desde funciones.py)
funciones.inicializar_recursos()

# --- VARIABLES LOCALES DEL BUCLE PRINCIPAL ---
ESTADO_ACTUAL = "MENU"
se_hizo_clic_previamente = False
juego_corriendo = True

# --- DEFINICIÓN DE BOTONES (Posición y Tamaño) ---
coord_centro_x = ANCHO_VENTANA // 2

rect_jugar = pygame.Rect(0, 0, 250, 50)
rect_jugar.center = (coord_centro_x, 200)

rect_ranking = pygame.Rect(0, 0, 250, 50)
rect_ranking.center = (coord_centro_x, 270)

rect_creditos = pygame.Rect(0, 0, 250, 50)
rect_creditos.center = (coord_centro_x, 340)

rect_salir = pygame.Rect(0, 0, 250, 50)
rect_salir.center = (coord_centro_x, 410)

rect_volver = pygame.Rect(20, ALTO_VENTANA - 70, 150, 50)

# ==========================================
#           BUCLE PRINCIPAL DEL JUEGO
# ==========================================
while juego_corriendo:
    # 1. Control de Tiempo
    tiempo_actual = pygame.time.get_ticks()
    reloj_control.tick(CUADROS_POR_SEGUNDO)
    
    # 2. Control de Inputs (Mouse y Teclado)
    mouse_esta_presionado = pygame.mouse.get_pressed()[0]
    
    # --- PROCESAMIENTO DE EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            juego_corriendo = False
        
        # Teclas específicas del JUEGO
        if ESTADO_ACTUAL == "JUEGO":
            # Iniciar lanzamiento con ESPACIO
            if not funciones.juego_esta_activo and funciones.vidas_jugador > 0:
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    funciones.juego_esta_activo = True
            
            # Detectar si perdió todas las vidas
            if not funciones.juego_esta_activo and funciones.vidas_jugador <= 0:
                 ESTADO_ACTUAL = "GAME_OVER"

        # Teclas específicas de GAME OVER (Escribir nombre)
        elif ESTADO_ACTUAL == "GAME_OVER":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    # Guardar puntaje al presionar ENTER
                    nombre = funciones.nombre_usuario_entrada if funciones.nombre_usuario_entrada else "Anonimo"
                    funciones.guardar_nuevo_puntaje(nombre, funciones.puntuacion_actual)
                    ESTADO_ACTUAL = "RANKING"
                elif evento.key == pygame.K_BACKSPACE:
                    # Borrar letra
                    funciones.nombre_usuario_entrada = funciones.nombre_usuario_entrada[:-1]
                else:
                    # Escribir letra (máximo 10 caracteres)
                    if len(funciones.nombre_usuario_entrada) < 10 and evento.unicode.isalnum():
                        funciones.nombre_usuario_entrada += evento.unicode

    # --- DIBUJO GENERAL ---
    # Dibujar fondo (común a todas las pantallas)
    ventana_principal.blit(funciones.IMAGEN_FONDO, (0, 0))

    # --- MÁQUINA DE ESTADOS ---
    
    # ------------------ ESTADO: MENU ------------------
    if ESTADO_ACTUAL == "MENU":
        funciones.dibujar_texto_centrado(ventana_principal, "ARKANOID PRO", funciones.fuente_titulo_principal, COLOR_BLANCO, 100)
        
        # Botón JUGAR
        if funciones.dibujar_boton_interactivo(ventana_principal, rect_jugar, "JUGAR") and not se_hizo_clic_previamente:
            funciones.iniciar_nueva_partida()
            ESTADO_ACTUAL = "JUEGO"
            
        # Botón RANKING
        if funciones.dibujar_boton_interactivo(ventana_principal, rect_ranking, "RANKING") and not se_hizo_clic_previamente:
            ESTADO_ACTUAL = "RANKING"
            
        # Botón CRÉDITOS
        if funciones.dibujar_boton_interactivo(ventana_principal, rect_creditos, "CREDITOS") and not se_hizo_clic_previamente:
            ESTADO_ACTUAL = "CREDITOS"
            
        # Botón SALIR
        if funciones.dibujar_boton_interactivo(ventana_principal, rect_salir, "SALIR") and not se_hizo_clic_previamente:
            juego_corriendo = False

    # ------------------ ESTADO: RANKING ------------------
    elif ESTADO_ACTUAL == "RANKING":
        funciones.dibujar_texto_centrado(ventana_principal, "MEJORES PUNTAJES", funciones.fuente_titulo_principal, COLOR_BLANCO, 80)
        
        lista_top = funciones.leer_ranking_desde_archivo()
        pos_y = 180
        
        if not lista_top:
            funciones.dibujar_texto_centrado(ventana_principal, "No hay datos disponibles", funciones.fuente_botones, COLOR_BLANCO, pos_y)
        else:
            for i, (nombre, puntos) in enumerate(lista_top):
                texto = f"{i + 1}. {nombre} - {puntos}"
                funciones.dibujar_texto_centrado(ventana_principal, texto, funciones.fuente_botones, COLOR_BLANCO, pos_y)
                pos_y += 60
             
        if funciones.dibujar_boton_interactivo(ventana_principal, rect_volver, "VOLVER") and not se_hizo_clic_previamente:
            ESTADO_ACTUAL = "MENU"

    # ------------------ ESTADO: CREDITOS ------------------
    elif ESTADO_ACTUAL == "CREDITOS":
        funciones.dibujar_texto_centrado(ventana_principal, "ALUMNOS", funciones.fuente_titulo_principal, COLOR_BLANCO, 100)
        
        alumnos = ["Barrera, Valeria", "Macura, Matias", "Ruiz Diaz, Nahuel"]
        pos_y = 200
        for nombre in alumnos:
            funciones.dibujar_texto_centrado(ventana_principal, nombre, funciones.fuente_botones, COLOR_BLANCO, pos_y)
            pos_y += 50
            
        if funciones.dibujar_boton_interactivo(ventana_principal, rect_volver, "VOLVER") and not se_hizo_clic_previamente:
            ESTADO_ACTUAL = "MENU"

    # ------------------ ESTADO: GAME OVER ------------------
    elif ESTADO_ACTUAL == "GAME_OVER":
        funciones.dibujar_texto_centrado(ventana_principal, "GAME OVER", funciones.fuente_titulo_principal, COLOR_BLANCO, 150)
        funciones.dibujar_texto_centrado(ventana_principal, f"Puntuacion Final: {funciones.puntuacion_actual}", funciones.fuente_botones, COLOR_BLANCO, 220)
        
        funciones.dibujar_texto_centrado(ventana_principal, "Ingresa tu nombre:", funciones.fuente_texto_general, COLOR_GRIS_CLARO, 300)
        
        # Caja de texto visual
        pygame.draw.rect(ventana_principal, COLOR_BLANCO, (coord_centro_x - 100, 330, 200, 40), 2)
        funciones.dibujar_texto_centrado(ventana_principal, funciones.nombre_usuario_entrada, funciones.fuente_botones, COLOR_BLANCO, 350)
        
        funciones.dibujar_texto_centrado(ventana_principal, "Presiona ENTER para guardar", funciones.fuente_texto_general, COLOR_GRIS_CLARO, 450)

    # ------------------ ESTADO: JUEGO ------------------
    elif ESTADO_ACTUAL == "JUEGO":
        # 1. Dibujar UI (Vidas y Puntos)
        texto_pts = funciones.fuente_puntuacion.render(f"Puntos: {funciones.puntuacion_actual}", True, COLOR_BLANCO)
        ventana_principal.blit(texto_pts, (ANCHO_VENTANA - 150, ALTO_VENTANA - 40))
        
        for i in range(funciones.vidas_jugador):
            ventana_principal.blit(funciones.imagen_corazon_1, (30 + (i * 45), ALTO_VENTANA - 60))

        # 2. Dibujar Elementos del Juego
        ventana_principal.blit(funciones.imagen_paleta_actual, funciones.rectangulo_paleta)
        
        if funciones.vidas_jugador > 0:
            pygame.draw.circle(ventana_principal, COLOR_BLANCO, (int(funciones.posicion_pelota_x), int(funciones.posicion_pelota_y)), RADIO_PELOTA)
        
        # 3. Mensaje de pausa inicial
        if not funciones.juego_esta_activo and funciones.vidas_jugador > 0:
            mensaje = funciones.fuente_texto_general.render("Presiona ESPACIO para lanzar", True, COLOR_BLANCO)
            rect_msg = mensaje.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
            ventana_principal.blit(mensaje, rect_msg)
            
            # Pegar pelota a la paleta
            funciones.posicion_pelota_x = funciones.rectangulo_paleta.centerx
            funciones.posicion_pelota_y = funciones.rectangulo_paleta.top - RADIO_PELOTA - 2

        # 4. Lógica Activa del Juego (Movimiento y Colisiones)
        if funciones.juego_esta_activo and funciones.vidas_jugador > 0:
            
            # A. Actualizar PowerUps (Tiempo)
            efectos_vencidos = []
            for ef in funciones.lista_efectos_activos:
                if tiempo_actual >= ef["expira_en"]:
                    funciones.desactivar_power_up(ef["tipo"])
                    efectos_vencidos.append(ef)
            for ef in efectos_vencidos: funciones.lista_efectos_activos.remove(ef)
            
            # B. Movimiento Paleta
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and funciones.rectangulo_paleta.left > 0:
                funciones.rectangulo_paleta.x -= VELOCIDAD_PALETA
            if keys[pygame.K_RIGHT] and funciones.rectangulo_paleta.right < ANCHO_VENTANA:
                funciones.rectangulo_paleta.x += VELOCIDAD_PALETA
            
            # C. Movimiento Pelota
            funciones.posicion_pelota_x += funciones.velocidad_pelota_x
            funciones.posicion_pelota_y += funciones.velocidad_pelota_y
            
            # D. Rebotes Paredes
            if funciones.posicion_pelota_x - RADIO_PELOTA <= 0 or funciones.posicion_pelota_x + RADIO_PELOTA >= ANCHO_VENTANA:
                funciones.velocidad_pelota_x *= -1
            if funciones.posicion_pelota_y - RADIO_PELOTA <= 0:
                funciones.velocidad_pelota_y *= -1
            
            # E. Perder Vida (Pelota cae)
            if funciones.posicion_pelota_y + RADIO_PELOTA >= ALTO_VENTANA:
                funciones.vidas_jugador -= 1
                funciones.juego_esta_activo = False
                # Limpiar efectos al perder vida
                for ef in funciones.lista_efectos_activos: funciones.desactivar_power_up(ef["tipo"])
                funciones.lista_efectos_activos.clear()
                funciones.lista_power_ups_cayendo.clear()
            
            # F. Colisión Paleta
            rect_pelota = pygame.Rect(funciones.posicion_pelota_x - RADIO_PELOTA, funciones.posicion_pelota_y - RADIO_PELOTA, RADIO_PELOTA * 2, RADIO_PELOTA * 2)
            if funciones.rectangulo_paleta.colliderect(rect_pelota) and funciones.velocidad_pelota_y > 0:
                funciones.velocidad_pelota_y *= -1
                # Efecto de ángulo según golpe
                diff = (funciones.rectangulo_paleta.centerx - funciones.posicion_pelota_x) / (funciones.rectangulo_paleta.width / 2)
                funciones.velocidad_pelota_x = -diff * 5 + (funciones.velocidad_pelota_x * 0.5)

            # G. Colisión Bloques
            bloques_a_borrar = []
            for bloque in funciones.lista_bloques:
                ventana_principal.blit(bloque["imagen"], bloque["rectangulo"])
                if bloque["rectangulo"].colliderect(rect_pelota):
                    funciones.velocidad_pelota_y *= -1
                    funciones.puntuacion_actual += VALORES_PUNTOS_BLOQUES[bloque["tipo"]]
                    bloques_a_borrar.append(bloque)
                    # Probabilidad PowerUp (30%)
                    if random.random() < 0.3:
                        tipo = random.choice(LISTA_TIPOS_POWER_UP)
                        rect_pu = funciones.diccionario_imagenes_powerups[tipo].get_rect(center=bloque["rectangulo"].center)
                        funciones.lista_power_ups_cayendo.append({"rectangulo": rect_pu, "tipo": tipo, "imagen": funciones.diccionario_imagenes_powerups[tipo]})
            
            for b in bloques_a_borrar: funciones.lista_bloques.remove(b)

            # H. PowerUps Cayendo
            pu_a_borrar = []
            for pu in funciones.lista_power_ups_cayendo:
                pu["rectangulo"].y += VELOCIDAD_CAIDA_POWERUP
                ventana_principal.blit(pu["imagen"], pu["rectangulo"])
                
                # Recoger PowerUp
                if funciones.rectangulo_paleta.colliderect(pu["rectangulo"]):
                    funciones.activar_power_up(pu["tipo"])
                    pu_a_borrar.append(pu)
                # Fuera de pantalla
                elif pu["rectangulo"].top > ALTO_VENTANA:
                    pu_a_borrar.append(pu)
            
            for pu in pu_a_borrar: funciones.lista_power_ups_cayendo.remove(pu)
        
        else:
            # Dibujar bloques estáticos si el juego está pausado
            for bloque in funciones.lista_bloques:
                ventana_principal.blit(bloque["imagen"], bloque["rectangulo"])

    # --- ACTUALIZAR PANTALLA ---
    se_hizo_clic_previamente = mouse_esta_presionado
    pygame.display.flip()

# Salida limpia
pygame.quit()
sys.exit()