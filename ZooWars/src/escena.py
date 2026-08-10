import pygame
import math
import os
from src.entidades import Animal, Proyectil, Explosion

def cargar_nivel(ruta):
    mapa = []
    spawns_1 = []
    spawns_2 = []

    with open(ruta, 'r') as archivo:
        for y, linea in enumerate(archivo):
            fila = []
            x = 0
            for char in linea.strip():
                if char in [',', ' ', '\t']: 
                    continue 
        
                if char == '1':
                    spawns_1.append((x, y)) 
                    fila.append(0) 
                elif char == '2':
                    spawns_2.append((x, y)) 
                    fila.append(0) 
                elif char == '.': 
                    fila.append(0)
                elif char == '#': 
                    fila.append(1)
                x += 1
            
            if fila:
                mapa.append(fila)
    
    return mapa, spawns_1, spawns_2

class EscenaBatalla:
    def __init__(self, columnas, filas, celda, ruta_nivel):
        self.celda = celda

        self.AIRE = 0
        self.TIERRA = 1
        self.mapa, spawns_1, spawns_2 = cargar_nivel(ruta_nivel)
        
        self.filas = len(self.mapa)
        self.columnas = len(self.mapa[0]) if self.filas > 0 else 0
        
        # Bucle para intercalar los animales de ambos equipos
        # Bucle para intercalar los animales de ambos equipos
        self.animales = []
        max_animales = max(len(spawns_1), len(spawns_2))
        
        for i in range(max_animales):
            if i < len(spawns_1):
                # ¡CORREGIDO! Pasamos primero [1] (Fila/Y) y luego [0] (Columna/X)
                self.animales.append(Animal(spawns_1[i][1], spawns_1[i][0], self.celda, equipo=1))
            
            if i < len(spawns_2):
                # ¡CORREGIDO! Pasamos primero [1] (Fila/Y) y luego [0] (Columna/X)
                self.animales.append(Animal(spawns_2[i][1], spawns_2[i][0], self.celda, equipo=2))
        
        self.turno_equipo = 1 
        self.estado_juego = "APUNTANDO" 
        self.ultimo_jugador_equipo = {
            1: self.animales[0] if len(self.animales) > 0 else None,
            2: None
        }
        self.indice_jugador_activo = 0 
        self.proyectiles = []
        self.explosiones = []
        self.tick_gravedad = 0

        self.sonido_disparo = None
        ruta_snd_disparo = os.path.join("assets", "audio", "disparo.ogg")
        if os.path.exists(ruta_snd_disparo):
            self.sonido_disparo = pygame.mixer.Sound(ruta_snd_disparo)

        self.sonido_explosion = None
        ruta_snd_explosion = os.path.join("assets", "audio", "explosion.wav")
        if os.path.exists(ruta_snd_explosion):
            self.sonido_explosion = pygame.mixer.Sound(ruta_snd_explosion)

        self.sonido_victoria = None
        ruta_snd_victoria = os.path.join("assets", "audio", "round_end.wav") 
        if os.path.exists(ruta_snd_victoria):
            self.sonido_victoria = pygame.mixer.Sound(ruta_snd_victoria)

        self.sonido_muerte = None
        ruta_snd_muerte = os.path.join("assets", "audio", "death.wav") 
        if os.path.exists(ruta_snd_muerte):
            self.sonido_muerte = pygame.mixer.Sound(ruta_snd_muerte)

        pygame.mixer.music.stop()
        ruta_musica_juego = os.path.join("assets", "audio", "battle.mp3")
        if os.path.exists(ruta_musica_juego):
            pygame.mixer.music.load(ruta_musica_juego)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.2)
            
        self.victoria_reproducida = False

        self.tiempo_turno_max = 20000  
        self.tiempo_inicio_turno = pygame.time.get_ticks()
        self.tiempo_restante = 20

        self.fondo = None
        ruta_fondo = os.path.join("assets", "images", "cielo.jpg")
        if os.path.exists(ruta_fondo):
            img = pygame.image.load(ruta_fondo).convert()
            self.fondo = pygame.transform.scale(img, (self.columnas * celda, self.filas * celda))

        self.textura_tierra = None
        ruta_tierra = os.path.join("assets", "images", "tierra.png")
        if os.path.exists(ruta_tierra):
            img = pygame.image.load(ruta_tierra).convert()
            self.textura_tierra = pygame.transform.scale(img, (celda, celda))

    def obtener_jugador_activo(self):
        return self.animales[self.indice_jugador_activo] if self.animales else None

    def cambiar_turno(self):
        animales_vivos = [a for a in self.animales if a.vida > 0]
        if not animales_vivos: return

        siguiente_equipo = 2 if self.turno_equipo == 1 else 1
        
        animales_equipo = [a for a in animales_vivos if a.equipo == siguiente_equipo]
        
        if not animales_equipo:
            siguiente_equipo = self.turno_equipo
            animales_equipo = [a for a in animales_vivos if a.equipo == siguiente_equipo]
            if not animales_equipo: return
            
        self.turno_equipo = siguiente_equipo
        
        ultimo = self.ultimo_jugador_equipo.get(siguiente_equipo)
        nuevo_jugador = animales_equipo[0]
        
        if ultimo in animales_equipo:
 
            idx = animales_equipo.index(ultimo)
            nuevo_jugador = animales_equipo[(idx + 1) % len(animales_equipo)]
        
        self.ultimo_jugador_equipo[siguiente_equipo] = nuevo_jugador
        self.indice_jugador_activo = self.animales.index(nuevo_jugador)
        
        self.estado_juego = "APUNTANDO"
        self.tiempo_inicio_turno = pygame.time.get_ticks()
        
        if nuevo_jugador:
            nuevo_jugador.cargando = False
            nuevo_jugador.fuerza_actual = 0

    def disparar_proyectil(self, jugador):
        centro_x = jugador.getX() + self.celda // 2
        centro_y = jugador.getY() + self.celda // 2
        
        radianes = math.radians(jugador.angulo)
        distancia_canon = self.celda * 1.2 
        
        origen_x = centro_x + (math.cos(radianes) * distancia_canon)
        origen_y = centro_y - (math.sin(radianes) * distancia_canon)

        if self.sonido_disparo:
            self.sonido_disparo.play()
        
        fuerza = jugador.obtener_fuerza_disparo()
        self.proyectiles.append(Proyectil(origen_x, origen_y, self.celda, jugador.angulo, fuerza))
        self.estado_juego = "VOLANDO"

    def manejar_eventos(self, evento):
        if self.estado_juego != "APUNTANDO": return
        jugador_activo = self.obtener_jugador_activo()
        if not jugador_activo: return
        
        if jugador_activo.getFila() < self.filas - 1 and self.mapa[jugador_activo.getFila() + 1][jugador_activo.getColumna()] == self.AIRE:
            return

        if evento.type == pygame.KEYDOWN:
            if not jugador_activo.cargando:
                if evento.key == pygame.K_LEFT and jugador_activo.getColumna() > 0:
                    if self.mapa[jugador_activo.getFila()][jugador_activo.getColumna() - 1] == self.AIRE:
                        jugador_activo.moverIzquierda()
                elif evento.key == pygame.K_RIGHT and jugador_activo.getColumna() < self.columnas - 1:
                    if self.mapa[jugador_activo.getFila()][jugador_activo.getColumna() + 1] == self.AIRE:
                        jugador_activo.moverDerecha()
                elif evento.key == pygame.K_UP:
                    jugador_activo.angulo = min(180, jugador_activo.angulo + 5)
                elif evento.key == pygame.K_DOWN:
                    jugador_activo.angulo = max(0, jugador_activo.angulo - 5)
                elif evento.key == pygame.K_SPACE:
                    jugador_activo.iniciar_carga()
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_SPACE and jugador_activo.cargando:
                self.disparar_proyectil(jugador_activo)

    def actualizar(self):
        jugador_activo = self.obtener_jugador_activo()
        
        if self.estado_juego == "APUNTANDO" and jugador_activo:
            # Lógica del reloj 
            tiempo_actual = pygame.time.get_ticks()
            tiempo_pasado = tiempo_actual - self.tiempo_inicio_turno
            self.tiempo_restante = max(0, (self.tiempo_turno_max - tiempo_pasado) // 1000)

            if self.tiempo_restante <= 0:
                self.cambiar_turno()
            elif jugador_activo.cargar_fuerza():
                self.disparar_proyectil(jugador_activo)

      # Lógica de gravedad
        self.tick_gravedad += 1
        if self.tick_gravedad >= 10: 
            self.tick_gravedad = 0
            for animal in self.animales: 
                if animal.vida > 0: # Solo aplicamos gravedad a los vivos
                    if animal.getFila() < self.filas - 1 and self.mapa[animal.getFila() + 1][animal.getColumna()] == self.AIRE:
                        animal.moverAbajo()
                    elif animal.getFila() >= self.filas - 1:
                        animal.vida = 0 # Muere silenciosamente al caer al vacío

        # Actualizar explosiones
        for exp in self.explosiones[:]:
            exp.actualizar()
            if exp.vida <= 0:
                self.explosiones.remove(exp)
                if self.estado_juego == "ESPERANDO_TURNO" and len(self.explosiones) == 0:
                    self.cambiar_turno()

        # Actualizar proyectiles y colisiones
        for p in self.proyectiles[:]:
            p.actualizar()
            px, py = p.getX(), p.getY()
            
            if px < 0 or px > self.columnas * self.celda or py > self.filas * self.celda:
                self.proyectiles.remove(p)
                if len(self.explosiones) == 0:
                    self.cambiar_turno()
                else:
                    self.estado_juego = "ESPERANDO_TURNO"
                continue
            
            col_impacto, fila_impacto = int(px // self.celda), int(py // self.celda)
            hubo_impacto = False

            for animal in self.animales:
                if math.hypot(px - (animal.getX() + self.celda // 2), py - (animal.getY() + self.celda // 2)) < self.celda * 0.4:
                    hubo_impacto = True; break

            if not hubo_impacto and 0 <= fila_impacto < self.filas and 0 <= col_impacto < self.columnas:
                if self.mapa[fila_impacto][col_impacto] == self.TIERRA: hubo_impacto = True

            if hubo_impacto:
                self.explosiones.append(Explosion(px, py, self.celda))
                
                if self.sonido_explosion:
                    self.sonido_explosion.play()

                for df in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if 0 <= fila_impacto + df < self.filas and 0 <= col_impacto + dc < self.columnas:
                            self.mapa[fila_impacto + df][col_impacto + dc] = self.AIRE
                
                for animal in self.animales:
                    if math.hypot(px - (animal.getX() + self.celda // 2), py - (animal.getY() + self.celda // 2)) <= self.celda * 1.8:
                        animal.recibir_dano(35)

                self.proyectiles.remove(p)
                self.estado_juego = "ESPERANDO_TURNO" 

        jugador_activo_antes = self.obtener_jugador_activo()
        animales_vivos = [a for a in self.animales if a.vida > 0]
        
        if len(animales_vivos) != len(self.animales):
            
            if self.sonido_muerte:
                self.sonido_muerte.play()
            
            self.animales = animales_vivos
            
            if jugador_activo_antes in self.animales:
                self.indice_jugador_activo = self.animales.index(jugador_activo_antes)
            else:
                self.indice_jugador_activo = 0
                if self.estado_juego == "APUNTANDO":
                    self.cambiar_turno()

        equipos_vivos = set(a.equipo for a in self.animales)
        
        if len(equipos_vivos) == 1 and len(self.animales) > 0:
            pygame.mixer.music.stop()
            if self.sonido_victoria and not self.victoria_reproducida:
                self.sonido_victoria.play()
                self.victoria_reproducida = True

    def dibujar(self, pantalla):
        if self.fondo:
            pantalla.blit(self.fondo, (0, 0))
        else:
            pantalla.fill((135, 206, 235))

        for f in range(len(self.mapa)):
            for c in range(len(self.mapa[f])):
                if self.mapa[f][c] == self.TIERRA:
                    if self.textura_tierra:
                        pantalla.blit(self.textura_tierra, (c * self.celda, f * self.celda))
                    else:
                        pygame.draw.rect(pantalla, (139, 69, 19), (c * self.celda, f * self.celda, self.celda, self.celda))
                        pygame.draw.rect(pantalla, (34, 139, 34), (c * self.celda, f * self.celda, self.celda, 10))

     
        fuente = pygame.font.SysFont("Arial", 24, bold=True)
        if len(self.animales) == 0:
            pantalla.blit(fuente.render("¡EMPATE! Todos han muerto", True, (255, 0, 0)), (10, 10))
        elif len(set(a.equipo for a in self.animales)) == 1:
            pantalla.blit(fuente.render(f"¡EQUIPO {self.animales[0].equipo} GANA!", True, (0, 255, 0)), (10, 10))
        else:
            pantalla.blit(fuente.render(f"Turno: Equipo {self.turno_equipo}", True, (255, 255, 255)), (10, 10))
            
            # Dibujar el temporizador 
            if self.estado_juego == "APUNTANDO":
                color_tiempo = (255, 255, 255) 
                if self.tiempo_restante <= 5:
                    color_tiempo = (255, 50, 50) 
                
                texto_tiempo = fuente.render(f"Tiempo: {self.tiempo_restante}s", True, color_tiempo)
                x_centro = (self.columnas * self.celda) // 2 - texto_tiempo.get_width() // 2
                pantalla.blit(texto_tiempo, (x_centro, 10))

        jugador_activo = self.obtener_jugador_activo()
        if jugador_activo and jugador_activo.cargando:
            pygame.draw.rect(pantalla, (0, 0, 0), (10, 40, 200, 20), 2)
            pygame.draw.rect(pantalla, (255, 0, 0), (12, 42, int(196 * (jugador_activo.fuerza_actual / jugador_activo.FUERZA_MAXIMA)), 16))

        for i, animal in enumerate(self.animales):
            animal.dibujar(pantalla, (i == self.indice_jugador_activo and self.estado_juego == "APUNTANDO"))
        
        for p in self.proyectiles: p.dibujar(pantalla)
        for exp in self.explosiones: exp.dibujar(pantalla)