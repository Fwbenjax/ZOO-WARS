# 🐾 Zoo Wars: Artillería Animal 🚀

Zoo Wars es un videojuego 2D de estrategia y artillería por turnos, fuertemente inspirado en clásicos como *Worms*. En este juego, dos facciones animales (Perros vs. Gatos) se enfrentan en un campo de batalla dinámico donde el posicionamiento, la puntería y la gestión del tiempo son claves para la victoria.

## ✨ Características Principales

* **Físicas y Gravedad:** Los personajes y el entorno responden a la gravedad. Si el suelo desaparece, ¡caerán al vacío!
* **Terreno Destructible:** Los impactos de los proyectiles destruyen dinámicamente la matriz del mapa, creando cráteres y alterando la estrategia de la partida.
* **Sistema de Turnos y Temporizador:** Gestión automática de turnos alternados entre equipos, con un reloj en tiempo real que fuerza la toma de decisiones rápidas (20 segundos por turno).
* **Mapas Personalizables:** El juego incluye un sistema de lectura de archivos `.txt` que permite a cualquier usuario diseñar y jugar en sus propios niveles usando un sistema visual ASCII.
* **Multimedia:** Banda sonora inmersiva y efectos de sonido independientes para disparos, explosiones, victorias y derrotas.

## 🛠️ Requisitos del Sistema

Para ejecutar este proyecto de forma local, necesitas tener instalado Python y la librería Pygame.

* Python 3.8 o superior.
* Pygame 2.0 o superior.

## 📥 Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/TU_USUARIO/zoo-wars.git](https://github.com/TU_USUARIO/zoo-wars.git)
   cd zoo-wars

   - ##Instalar dependencias:

   pip install pygame

   - ##Ejecutar el juego:

   python main.py

## 🎮 Controles de Juego
Una vez dentro de la partida, los controles para el jugador activo son los siguientes:

 ```bash

  | Tecla | Acción |
| :--- | :--- |
| `FLECHA IZQUIERDA` | Caminar hacia la izquierda. |
| `FLECHA DERECHA` | Caminar hacia la derecha. |
| `FLECHA ARRIBA` | Elevar el ángulo del cañón. |
| `FLECHA ABAJO` | Bajar el ángulo del cañón. |
| `MANTENER ESPACIO` | Cargar la fuerza del disparo (Barra roja). |
| `SOLTAR ESPACIO` | Disparar el proyectil. |
| `ESC` | Abandonar la partida y volver al menú. |
```

## 🗺️ Creación de Niveles (Modding)

Puedes crear tus propios escenarios añadiendo un archivo `.txt` dentro de la carpeta `levels/`. El motor del juego leerá el archivo utilizando la siguiente nomenclatura:

* `.` (Punto): Aire / Espacio vacío.
* `#` (Numeral): Bloque de tierra destructible.
* `1`: Punto de aparición (Spawn) para el Equipo 1.
* `2`: Punto de aparición (Spawn) para el Equipo 2.

**Ejemplo de mapa:**

 ```bash
..............................
..............................
...1......................2...
..####..................####..
..............................
.........2..........1.........
......#######....#######......
..............................
##############################
