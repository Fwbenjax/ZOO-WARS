import pygame
import math
import os
from src.base import BaseGrafica, BaseLogica

class Animal(BaseLogica):
    def __init__(self, fila, columna, celda, equipo):
        super().__init__(fila, columna, celda)
        self.equipo = equipo
        self.vida = 100
        self.angulo = 45 if equipo == 1 else 135 
        
        self.fuerza_actual = 0
        self.cargando = False 
        self.FUERZA_MAXIMA = 100

        self.sprite = None
        nombre_archivo = "perro.png" if equipo == 1 else "gato.png"
        ruta_sprite = os.path.join("assets", "images", nombre_archivo)
        
        if os.path.exists(ruta_sprite):
            img = pygame.image.load(ruta_sprite).convert_alpha()
            ancho, alto = img.get_size()
            for x in range(ancho):
                for y in range(alto):
                    color = img.get_at((x, y))
                    if color.r > 240 and color.g > 240 and color.b > 240:
                        img.set_at((x, y), (255, 255, 255, 0)) 

            self.sprite = pygame.transform.scale(img, (self.getEscala(), self.getEscala()))
        else:
            self.setColor((40, 100, 200) if equipo == 1 else (200, 40, 40))

    def recibir_dano(self, cantidad):
        self.vida -= cantidad
        if self.vida < 0: self.vida = 0

    def iniciar_carga(self):
        self.cargando = True
        self.fuerza_actual = 0

    def cargar_fuerza(self):
        if self.cargando:
            self.fuerza_actual += 2
            if self.fuerza_actual >= self.FUERZA_MAXIMA:
                self.fuerza_actual = self.FUERZA_MAXIMA
                return True 
        return False

    def obtener_fuerza_disparo(self):
        self.cargando = False
        fuerza_final = self.fuerza_actual
        self.fuerza_actual = 0
        return max(10, fuerza_final) 

    def dibujar(self, pantalla, es_mi_turno):
        if self.sprite:
            if self.angulo > 90:
                sprite_volteado = pygame.transform.flip(self.sprite, True, False)
                pantalla.blit(sprite_volteado, (self.getX(), self.getY()))
            else:
                pantalla.blit(self.sprite, (self.getX(), self.getY()))
        else:
            centro_x = self.getX() + self.getEscala() // 2
            centro_y = self.getY() + self.getEscala() // 2
            pygame.draw.circle(pantalla, self.getColor(), (centro_x, centro_y), int(self.getEscala() * 0.4))

        centro_x = self.getX() + self.getEscala() // 2
        centro_y = self.getY() + self.getEscala() // 2
        ancho_barra = self.getEscala()
        x_barra = centro_x - ancho_barra // 2
        y_barra = self.getY() - 10
        
        pygame.draw.rect(pantalla, (255, 0, 0), (x_barra, y_barra, ancho_barra, 6))
        pygame.draw.rect(pantalla, (0, 255, 0), (x_barra, y_barra, int(ancho_barra * (self.vida / 100.0)), 6))

        if es_mi_turno:
            radianes = math.radians(self.angulo)
            distancia_reticula = self.getEscala() * 1.2
            reticula_x = centro_x + (math.cos(radianes) * distancia_reticula)
            reticula_y = centro_y - (math.sin(radianes) * distancia_reticula) 
            pygame.draw.line(pantalla, (255, 255, 255), (centro_x, centro_y), (reticula_x, reticula_y), 2)
            pygame.draw.circle(pantalla, (255, 0, 0), (int(reticula_x), int(reticula_y)), 4)
            pygame.draw.polygon(pantalla, (255, 255, 0), [(centro_x, y_barra - 5), (centro_x - 5, y_barra - 15), (centro_x + 5, y_barra - 15)])

class Proyectil(BaseGrafica):
    def __init__(self, x, y, celda, angulo, fuerza):
        super().__init__(x, y, celda)
        radianes = math.radians(angulo)
        self.vel_x = math.cos(radianes) * fuerza * 0.25
        self.vel_y = -math.sin(radianes) * fuerza * 0.25 
        self.gravedad = 0.5 
        
        self.sprite = None
        ruta_proyectil = os.path.join("assets", "images", "proyectil.png")
        if os.path.exists(ruta_proyectil):
            img = pygame.image.load(ruta_proyectil).convert_alpha()
            tamano_proyectil = self.getEscala() // 2
            self.sprite = pygame.transform.scale(img, (tamano_proyectil, tamano_proyectil))

    def actualizar(self):
        self.setX(self.getX() + self.vel_x)
        self.setY(self.getY() + self.vel_y)
        self.vel_y += self.gravedad 

    def dibujar(self, pantalla):
        if self.sprite:
            pantalla.blit(self.sprite, (int(self.getX()), int(self.getY())))
        else:
            pygame.draw.circle(pantalla, (255, 255, 0), (int(self.getX()), int(self.getY())), max(2, self.getEscala() // 8))

class Explosion(BaseGrafica):
    def __init__(self, x, y, celda):
        super().__init__(x, y, celda)
        self.radio = 2
        self.vida = 15 
        
    def actualizar(self):
        self.radio += 3 
        self.vida -= 1
        
    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, (255, 140, 0), (int(self.getX()), int(self.getY())), self.radio)
        pygame.draw.circle(pantalla, (255, 255, 0), (int(self.getX()), int(self.getY())), max(1, self.radio // 2))