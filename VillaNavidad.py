import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
from OpenGL.GLUT import *
import sys
import math
import random

a = 0.1
b = 0.5
turns = 40
points_per_turn = 1000

snowflakes = []
num_snowflakes = 500

def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)  # Activar prueba de profundidad

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = 800, 600
    gluPerspective(90, width / height, 0.1, 200.0)  # Ampliar el rango máximo
    glMatrixMode(GL_MODELVIEW)

def init_snow():
    """Inicializa las posiciones de los copos de nieve"""
    global snowflakes
    snowflakes = [
        [random.uniform(-50, 50), random.uniform(5, 20), random.uniform(-20, 20)]
        for _ in range(num_snowflakes)
    ]

def update_snow():
    """Actualiza la posición de los copos de nieve"""
    global snowflakes
    for flake in snowflakes:
        flake[1] -= 0.05  # Mueve el copo hacia abajo
        if flake[1] < 0:  # Si el copo llega al suelo, reinícialo en la parte superior
            flake[0] = random.uniform(-20, 20)
            flake[1] = random.uniform(5, 20)
            flake[2] = random.uniform(-20, 20)

def draw_mountain():
    """Dibuja una montaña básica usando triángulos"""
    glPushMatrix()
    glTranslatef(-20, 0, -35)  # Posiciona la montaña detrás de la escena
    glScalef(30, 25, 1)  # Escala la montaña para que sea grande y alta
    glBegin(GL_TRIANGLES)

    glColor3f(0.404, 0.639, 0.847)  # Verde oscuro para la montaña

    # Triángulo principal (base)
    glVertex3f(-1, 0, 0)  # Punto inferior izquierdo
    glVertex3f(1, 0, 0)   # Punto inferior derecho
    glVertex3f(0, 1, 0)   # Pico de la montaña

    # Añadir más triángulos para dar textura a la montaña
    glColor3f(1, 1, 1)  # Otro tono de verde
    glVertex3f(-0.5, 0, 0)
    glVertex3f(0.5, 0, 0)
    glVertex3f(0, 0.7, 0)

    glEnd()
    glPopMatrix()

def draw_snowman():
    """Dibuja un muñeco de nieve"""
    # Cuerpo
    glColor3f(1.0, 1.0, 1.0)  # Blanco
    glPushMatrix()
    glTranslatef(3, 0, -5)  # Posiciona el muñeco en la escena
    glutSolidSphere(0.5, 32, 32)  # Base (esfera inferior)
    glTranslatef(0, 0.6, 0)  # Mueve hacia arriba para el cuerpo medio
    glutSolidSphere(0.35, 32, 32)  # Cuerpo medio
    glTranslatef(0, 0.5, 0)  # Mueve hacia arriba para la cabeza
    glutSolidSphere(0.25, 32, 32)  # Cabeza

    # Ojos
    glColor3f(0.0, 0.0, 0.0)  # Negro
    glPushMatrix()
    glTranslatef(-0.08, 0.1, 0.22)  # Ojo izquierdo
    glutSolidSphere(0.03, 16, 16)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.08, 0.1, 0.22)  # Ojo derecho
    glutSolidSphere(0.03, 16, 16)
    glPopMatrix()

    # Nariz
    glColor3f(1.0, 0.5, 0.0)  # Naranja
    glPushMatrix()
    glTranslatef(0, 0, 0.25)  # Nariz
    glRotatef(-90, 1, 0, 0)  # Rotar para que el cono apunte hacia adelante
    glutSolidCone(0.05, 0.2, 16, 16)
    glPopMatrix()

    glPopMatrix()

def draw_snow():
    """Dibuja los copos de nieve"""
    glColor3f(1.0, 1.0, 1.0)  # Blanco
    glPointSize(4.0)
    glBegin(GL_POINTS)
    for flake in snowflakes:
        glVertex3f(flake[0], flake[1], flake[2])
    glEnd()

def draw_santa():
    """Dibuja un Santa Claus simplificado"""
    glPushMatrix()
    glTranslatef(-2, 0, 6)  # Posiciona a Santa Claus en la escena

    # Cuerpo (esfera roja)
    glColor3f(1.0, 0.0, 0.0)  # Rojo
    glutSolidSphere(0.5, 32, 32)

    # Cinturón (cubo negro)
    glColor3f(0.0, 0.0, 0.0)  # Negro
    glPushMatrix()
    glScalef(1.2, 0.1, 1.2)
    glTranslatef(0, 4.8, 0)  # Ajustar posición del cinturón
    glutSolidCube(0.5)
    glPopMatrix()

    # Cabeza (esfera de piel)
    glColor3f(1.0, 0.8, 0.6)  # Color piel
    glTranslatef(0, 0.7, 0)  # Subir la cabeza
    glutSolidSphere(0.3, 32, 32)

    # Sombrero (cono rojo)
    glColor3f(1.0, 0.0, 0.0)  # Rojo
    glPushMatrix()
    glTranslatef(0, 0.4, 0)  # Ajustar posición del sombrero
    glRotatef(-90, 1, 0, 0)  # Apuntar el cono hacia arriba
    glutSolidCone(0.2, 0.5, 32, 32)
    glPopMatrix()

    # Pompón del sombrero (esfera blanca)
    glColor3f(1.0, 1.0, 1.0)  # Blanco
    glPushMatrix()
    glTranslatef(0, 1.2, 0)  # Ajustar posición del pompón
    glutSolidSphere(0.1, 32, 32)
    glPopMatrix()

    glPopMatrix()

def draw_cube():
    """Dibuja el cubo (base de la casa)"""
    glBegin(GL_QUADS)
    glColor3f(0.678, 0.063, 0.212)
    # Frente
    glVertex3f(-1, 0, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)

    # Atrás
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)

    # Izquierda
    glVertex3f(-1, 0, -1)
    glVertex3f(-1, 0, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1, -1)

    # Derecha
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, 1, -1)

    # Arriba
    glColor3f(0.9, 0.6, 0.3)  # Color diferente para el techo
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)

    glEnd()

def draw_roof():
    """Dibuja el techo (pirámide)"""
    glBegin(GL_TRIANGLES)
    glColor3f(0.84, 0.741, 0.765)  # Rojo brillante

    # Frente
    glVertex3f(-1, 1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(0, 2, 0)

    # Atrás
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(0, 2, 0)

    # Izquierda
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)
    glVertex3f(0, 2, 0)

    # Derecha
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(0, 2, 0)
    glEnd()

def draw_ground():
    """Dibuja un plano para representar el suelo o calle"""
    glBegin(GL_QUADS)
    glColor3f(0.76, 0.772, 0.788)  # Gris oscuro para la calle

    # Coordenadas del plano
    glVertex3f(-100, 0, 100)
    glVertex3f(100, 0, 100)
    glVertex3f(100, 0, -100)
    glVertex3f(-100, 0, -100)
    glEnd()

def draw_elf():
    """Dibuja un duende simplificado"""
    glPushMatrix()
    glTranslatef(-5, 0, -10)  # Posiciona el duende en la escena

    # Cuerpo (esfera verde)
    glColor3f(0.0, 0.8, 0.0)  # Verde
    glutSolidSphere(0.5, 32, 32)

    # Cabeza (esfera de piel)
    glPushMatrix()
    glTranslatef(0, 0.6, 0)  # Subir la cabeza
    glColor3f(1.0, 0.8, 0.6)  # Color piel
    glutSolidSphere(0.3, 32, 32)
    glPopMatrix()  # Fin de la cabeza

    # Sombrero (cono rojo con pompón)
    glPushMatrix()
    glTranslatef(0, 1.0, 0)  # Posición del sombrero
    glRotatef(-90, 1, 0, 0)  # Girar el cono hacia arriba
    glColor3f(1.0, 0.0, 0.0)  # Rojo
    glutSolidCone(0.25, 0.5, 32, 32)

    # Pompón del sombrero
    glPushMatrix()
    glTranslatef(0, 0, 0.5)
    glColor3f(1.0, 1.0, 1.0)  # Blanco
    glutSolidSphere(0.08, 16, 16)
    glPopMatrix()  # Fin del pompón
    glPopMatrix()  # Fin del sombrero

    # Brazos (cubos verdes)
    glColor3f(0.0, 0.8, 0.0)  # Verde
    for x in [-0.7, 0.7]:  # Brazo izquierdo y derecho
        glPushMatrix()
        glTranslatef(x, 0.2, 0)  # Ajusta la posición de cada brazo
        glScalef(0.1, 0.4, 0.1)  # Escalar para formar un brazo
        glutSolidCube(1)
        glPopMatrix()

    # Piernas (cubos verdes)
    for x in [-0.2, 0.2]:  # Pierna izquierda y derecha
        glPushMatrix()
        glTranslatef(x, -0.5, 0)  # Ajusta la posición de cada pierna
        glScalef(0.15, 0.5, 0.15)  # Escalar para formar una pierna
        glutSolidCube(1)
        glPopMatrix()

    glPopMatrix()  # Fin del cuerpo del duende

def draw_reindeer():
    """Dibuja un reno simplificado"""
    glPushMatrix()
    glTranslatef(-10, 0, -5)  # Posiciona el reno en la escena

    # Cuerpo (esfera marrón)
    glColor3f(0.6, 0.3, 0.1)  # Marrón
    glutSolidSphere(0.5, 32, 32)

    # Cabeza (esfera más pequeña)
    glPushMatrix()
    glTranslatef(0, 0.6, 0.4)
    glutSolidSphere(0.3, 32, 32)
    glPopMatrix()  # Fin de la cabeza

    # Patas (cubos marrones)
    glColor3f(0.4, 0.2, 0.1)
    for x, z in [(-0.2, 0.2), (0.2, 0.2), (-0.2, -0.2), (0.2, -0.2)]:
        glPushMatrix()
        glTranslatef(x, -0.5, z)
        glScalef(0.1, 0.5, 0.1)  # Escalar el cubo para parecer una pata
        glutSolidCube(1)
        glPopMatrix()  # Fin de cada pata

    # Orejas (esferas pequeñas)
    glColor3f(0.6, 0.3, 0.1)
    for x in [-0.2, 0.2]:
        glPushMatrix()
        glTranslatef(x, 0.8, 0.3)
        glutSolidSphere(0.1, 16, 16)
        glPopMatrix()  # Fin de cada oreja

    # Cuernos (conos marrones)
    glColor3f(0.4, 0.2, 0.1)
    for x in [-0.15, 0.15]:
        glPushMatrix()
        glTranslatef(x, 1.0, 0.3)
        glRotatef(-45, 0, 1, 0)  # Angula los cuernos hacia afuera
        glRotatef(-90, 1, 0, 0)
        glutSolidCone(0.1, 0.5, 16, 16)
        glPopMatrix()  # Fin de cada cuerno

    # Nariz roja
    glColor3f(1.0, 0.0, 0.0)  # Rojo
    glPushMatrix()
    glTranslatef(0, 0.5, 0.6)
    glutSolidSphere(0.08, 16, 16)
    glPopMatrix()  # Fin de la nariz

    glPopMatrix()  # Fin del cuerpo del reno

def draw_reindeer():
    """Dibuja un reno simplificado"""
    glPushMatrix()
    glTranslatef(-10, 3, 0)  # Posiciona el reno en la escena

    # Cuerpo (esfera marrón)
    glColor3f(0.6, 0.3, 0.1)  # Marrón
    glutSolidSphere(0.5, 32, 32)

    # Cabeza (esfera más pequeña)
    glPushMatrix()
    glTranslatef(0, 0.6, 0.4)
    glutSolidSphere(0.3, 32, 32)
    glPopMatrix()  # Fin de la cabeza

    # Patas (cubos marrones)
    glColor3f(0.4, 0.2, 0.1)
    for x, z in [(-0.2, 0.2), (0.2, 0.2), (-0.2, -0.2), (0.2, -0.2)]:
        glPushMatrix()
        glTranslatef(x, -0.5, z)
        glScalef(0.1, 0.5, 0.1)  # Escalar el cubo para parecer una pata
        glutSolidCube(1)
        glPopMatrix()  # Fin de cada pata

    # Orejas (esferas pequeñas)
    glColor3f(0.6, 0.3, 0.1)
    for x in [-0.2, 0.2]:
        glPushMatrix()
        glTranslatef(x, 0.8, 0.3)
        glutSolidSphere(0.1, 16, 16)
        glPopMatrix()  # Fin de cada oreja

    # Cuernos (conos marrones)
    glColor3f(0.4, 0.2, 0.1)
    for x in [-0.15, 0.15]:
        glPushMatrix()
        glTranslatef(x, 1.0, 0.3)
        glRotatef(-45, 0, 1, 0)  # Angula los cuernos hacia afuera
        glRotatef(-90, 1, 0, 0)
        glutSolidCone(0.1, 0.5, 16, 16)
        glPopMatrix()  # Fin de cada cuerno

    # Nariz roja
    glColor3f(1.0, 0.0, 0.0)  # Rojo
    glPushMatrix()
    glTranslatef(0, 0.5, 0.6)
    glutSolidSphere(0.08, 16, 16)
    glPopMatrix()  # Fin de la nariz

    glPopMatrix()  # Fin del cuerpo del reno

def draw_house():
    """Dibuja una casa (base + techo)"""
    draw_cube()  # Base de la casa
    draw_roof()  # Techo

def draw_spiral():
    """Dibuja la espiral"""
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)  # Rotar 90 grados sobre el eje X para alinear la espiral al eje Z
    z = 7  # Inicia desde un valor alto en Z
    glPointSize(4.0)
    glColor3f(0.0, 0.5, 0.1)
    glBegin(GL_POINTS)  # Inicia el bloque de puntos

    for i in range(int(turns * points_per_turn)):
        t = i / points_per_turn
        x = a * t * math.cos(t)
        y = a * t * math.sin(t)
        glVertex3f(x, y, z)
        z -= 0.000175

    glEnd()  # Termina el bloque de puntos
    glPopMatrix()

def draw_scene():
    """Dibuja toda la escena con 4 casas, la espiral y la nieve"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(-3, 5, 13,
              0, 0, 0,
              0, 1, 0)

    draw_ground()
    draw_mountain()
    draw_elf()
    elf_positions = [
        (-5, 0, 10),
        (-16, 0, -2),
        (15, 0, 10),
        (0, 0, 14)
    ]
    for pos in elf_positions:
        glPushMatrix()
        glTranslatef(*pos)
        draw_elf()
        glPopMatrix()
    draw_reindeer()
    draw_santa()
    reindeer_positions = [
        (-10, 0, -10),
        (-12, 0, -8),
        (-8, 0, -12),
        (-14, 0, -6),
        (-16, 0, -4)
    ]
    for lugar in reindeer_positions:
        glPushMatrix()
        glTranslatef(*lugar)
        draw_reindeer()
        glPopMatrix()
    snowman_positions = [
        (-12, 0, 3),
        (-8, 0, 5),
        (0, 0, 12),
        (9, 0, 0),
        (4,0,-2)
    ]
    for position in snowman_positions:
        glPushMatrix()
        glTranslatef(*position)
        draw_snowman()
        glPopMatrix()


    # Dibujar las casas
    positions = [
        (-6, 0, -6),  # Casa 1
        (6, 0, -6),  # Casa 2
        (-6, 0, 6),  # Casa 3
        (6, 0, 6)  # Casa 4
    ]
    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)
        draw_house()
        glPopMatrix()

    # Dibujar la espiral al lado de la primera casa
    glPushMatrix()
    glTranslatef(0, 0, 2)
    draw_spiral()
    glPopMatrix()

    # Dibujar la nieve
    draw_snow()

    glfw.swap_buffers(window)

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()

    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Villa Navideña", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()
    init_snow()  # Inicializa la nieve

    # Bucle principal
    while not glfw.window_should_close(window):
        update_snow()  # Actualiza la posición de la nieve
        draw_scene()
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()