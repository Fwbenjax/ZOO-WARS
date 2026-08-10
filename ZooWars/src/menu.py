import pygame
import os

class MenuPrincipal:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.niveles = self.obtener_niveles()
        self.indice_seleccionado = 0
        
        self.fuente_titulo = pygame.font.SysFont("Arial", 64, bold=True)
        self.fuente_menu = pygame.font.SysFont("Arial", 32)
        self.fuente_pequena = pygame.font.SysFont("Arial", 16)
        
        self.nivel_seleccionado_ruta = None

        ruta_musica = os.path.join("assets", "audio", "menu.wav")
        if os.path.exists(ruta_musica):
            pygame.mixer.music.load(ruta_musica)
            pygame.mixer.music.play(-1) 
            pygame.mixer.music.set_volume(0.5)

    def obtener_niveles(self):
        if not os.path.exists("levels"):
            os.makedirs("levels")
        archivos = [f for f in os.listdir("levels") if f.endswith('.txt')]
        return sorted(archivos)

    def manejar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_DOWN:
                self.indice_seleccionado = (self.indice_seleccionado + 1) % len(self.niveles) if self.niveles else 0
            elif evento.key == pygame.K_UP:
                self.indice_seleccionado = (self.indice_seleccionado - 1) % len(self.niveles) if self.niveles else 0
            elif evento.key == pygame.K_RETURN:
                if self.niveles:
                    self.nivel_seleccionado_ruta = os.path.join("levels", self.niveles[self.indice_seleccionado])

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill((30, 30, 50))
        
        texto_titulo = self.fuente_titulo.render("ZOO WARS", True, (255, 215, 0))
        pantalla.blit(texto_titulo, (self.ancho // 2 - texto_titulo.get_width() // 2, 80))

        if not self.niveles:
            texto_error = self.fuente_menu.render("No hay niveles en la carpeta 'levels/'", True, (255, 50, 50))
            pantalla.blit(texto_error, (self.ancho // 2 - texto_error.get_width() // 2, 250))
        else:
            for i, nombre_archivo in enumerate(self.niveles):
                nombre_limpio = os.path.splitext(nombre_archivo)[0] 
                nombre_limpio = nombre_limpio.replace("_", " ").title() 

                color = (0, 255, 0) if i == self.indice_seleccionado else (200, 200, 200)
                prefijo = ">  " if i == self.indice_seleccionado else "   "
                
                texto_nivel = self.fuente_menu.render(f"{prefijo}{nombre_limpio}", True, color)
                pantalla.blit(texto_nivel, (self.ancho // 2 - 100, 220 + (i * 45)))
      
        texto_instruccion = self.fuente_pequena.render("Usa las FLECHAS para moverte y ENTER para seleccionar", True, (150, 150, 150))
        pantalla.blit(texto_instruccion, (self.ancho // 2 - texto_instruccion.get_width() // 2, self.alto - 50))