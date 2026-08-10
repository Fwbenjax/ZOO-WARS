import pygame
from src.menu import MenuPrincipal
from src.escena import EscenaBatalla

pygame.init()
CELDA = 40
COLUMNAS = 30
FILAS = 20

pantalla = pygame.display.set_mode((COLUMNAS * CELDA, FILAS * CELDA))
pygame.display.set_caption("Zoo Wars")
reloj = pygame.time.Clock()

escena_actual = MenuPrincipal(COLUMNAS * CELDA, FILAS * CELDA)

jugando = True
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        else:
            escena_actual.manejar_eventos(evento)
            
            if isinstance(escena_actual, EscenaBatalla) and evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                escena_actual = MenuPrincipal(COLUMNAS * CELDA, FILAS * CELDA)

    if isinstance(escena_actual, MenuPrincipal) and escena_actual.nivel_seleccionado_ruta:
        ruta = escena_actual.nivel_seleccionado_ruta
        escena_actual = EscenaBatalla(COLUMNAS, FILAS, CELDA, ruta)

    escena_actual.actualizar()

    escena_actual.dibujar(pantalla)

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()