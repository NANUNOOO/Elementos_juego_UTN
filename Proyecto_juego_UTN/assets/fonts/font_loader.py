import pygame

def crear_fuente_titulo():
    return pygame.font.SysFont("Arial", 50, bold=True)

def crear_fuente_botones():
    return pygame.font.SysFont("Arial", 30, bold=True)

def crear_fuente_general():
    return pygame.font.SysFont("Arial", 25)

def crear_fuente_puntuacion():
    return pygame.font.Font(None, 36)