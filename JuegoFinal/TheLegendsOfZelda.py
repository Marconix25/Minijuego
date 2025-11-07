"""
Fecha =01/11/22
Name= desastre_espacial.py
Developer= Marco Antonio Ceballos Cruz
Description= "Realizar un videojuego tipo galagar"
"""
# Importamos librerias
import pygame
import random
# Iniciación de Pygame
pygame.init()
# inicializacion de sonidos
pygame.mixer.init()

# cargamos musica de fondo
musica_fondo = pygame.mixer.Sound(
    'TheLegendOfZelda/sonido/ostfondo.wav')
# reproducimos en blucle
musica_fondo.play(-1)
# ajustamos volumen
musica_fondo.set_volume(0.2)
# cargamos los demas sonidos
laser_sonido = pygame.mixer.Sound(
    'TheLegendOfZelda/sonido/golpe.wav')
laser_enemigo = pygame.mixer.Sound(
    'TheLegendOfZelda/sonido/disparo_enemigo.wav')
explosion_sonido = pygame.mixer.Sound(
    'TheLegendOfZelda/sonido/explosion.wav')
herida_sonido = pygame.mixer.Sound(
    'TheLegendOfZelda/sonido/herida.wav')
# Pantalla - ventana
W, H = 1000, 600
PANTALLA = pygame.display.set_mode((W, H))
pygame.display.set_caption('TLOZ')
icono = pygame.image.load(
    'TheLegendOfZelda/imagenes/link/link_abajo1.png')
pygame.display.set_icon(icono)


# Control de FPS
reloj = pygame.time.Clock()

# Puntuacion
score = 0
# Fondo del juego
fondo = pygame.image.load('TheLegendOfZelda/imagenes/fondo.png')
# Pantalla de inicio
intro = pygame.image.load(
    'TheLegendOfZelda/imagenes/intro/intro.png')
# personaje sin movimiento
quieto = pygame.image.load(
    'TheLegendOfZelda/imagenes/link/link_abajo1.png')
# arreglo de explosion
explosion_list = []
for i in range(1, 13):
    explosion = pygame.image.load(
        f'TheLegendOfZelda/explosion/{i}.png')
    explosion_list.append(explosion)
blanco = (255, 255, 255)
negro = (0, 0, 0)


# hacemos fuente de escritura
def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_text_negro(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# presentacion de tabla de puntos


def texto_puntuacion(frame, text, size, x, y):
    font = pygame.font.SysFont('Small Fonts', size, bold=True)
    text_frame = font.render(text, True, blanco, negro)
    text_rect = text_frame.get_rect()
    text_rect.midtop = (x, y)
    frame.blit(text_frame, text_rect)


# barra de vida
def barra_vida(frame, x, y, nivel):
    longitud = 100
    alto = 20
    fill = int((nivel/100)*longitud)
    border = pygame.Rect(x, y, longitud, alto)
    fill = pygame.Rect(x, y, fill, alto)
    pygame.draw.rect(frame, (255, 0, 55), fill)
    pygame.draw.rect(frame, negro, border, 4)
# Clase jugador


class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.px = 500
        self.py = 450
        self.salto = False
        self.velocidad = 5
        self.ancho = 40
        # Contador de salto
        self.cuentaSalto = 10

        # Variables dirección
        self.izquierda = False
        self.derecha = False
        self.arriba = False
        self.abajo = False
        # Pasos
        self.cuentaPasos = 0
        # Fotogramas animados ((sprites))
        self.quieto = pygame.image.load(
            'TheLegendOfZelda/imagenes/link/link_abajo1.png')
        self.caminaDerecha = [pygame.image.load('TheLegendOfZelda/imagenes/link/link_der6.png'),
                              pygame.image.load(
                                  'TheLegendOfZelda/imagenes/link/link_der5.png'),
                              pygame.image.load(
                                  'TheLegendOfZelda/imagenes/link/link_der4.png'),
                              pygame.image.load(
                                  'TheLegendOfZelda/imagenes/link/link_der3.png'),
                              pygame.image.load(
                                  'TheLegendOfZelda/imagenes/link/link_der2.png'),
                              pygame.image.load('TheLegendOfZelda/imagenes/link/link_der1.png')]

        self.caminaIzquierda = [pygame.image.load('TheLegendOfZelda/imagenes/link/link_izq1.png'),
                                pygame.image.load(
                                    'TheLegendOfZelda/imagenes/link/link_izq2.png'),
                                pygame.image.load(
                                    'TheLegendOfZelda/imagenes/link/link_izq3.png'),
                                pygame.image.load(
                                    'TheLegendOfZelda/imagenes/link/link_izq4.png'),
                                pygame.image.load(
                                    'TheLegendOfZelda/imagenes/link/link_izq5.png'),
                                pygame.image.load('TheLegendOfZelda/imagenes/link/link_izq6.png')]
        self.caminaArriba = [pygame.image.load('TheLegendOfZelda/imagenes/link/link_arriba1.png'),
                             pygame.image.load(
                                 'TheLegendOfZelda/imagenes/link/link_arriba2.png'),
                             pygame.image.load(
                                 'TheLegendOfZelda/imagenes/link/link_arriba3.png'),
                             pygame.image.load(
                                 'TheLegendOfZelda/imagenes/link/link_arriba4.png'),
                             pygame.image.load(
                                 'TheLegendOfZelda/imagenes/link/link_arriba5.png'),
                             pygame.image.load(
                                 'TheLegendOfZelda/imagenes/link/link_arriba6.png'),
                             pygame.image.load(
                                 'TheLegendOfZelda/imagenes/link/link_arriba7.png'),
                             pygame.image.load(
                                 'TheLegendOfZelda/imagenes/link/link_arriba8.png'),
                             pygame.image.load(
                                 'TheLegendOfZelda/imagenes/link/link_arriba9.png'),
                             pygame.image.load('TheLegendOfZelda/imagenes/link/link_arriba10.png'),]

        self.caminaAbajo = [
            pygame.image.load(
                'TheLegendOfZelda/imagenes/link/link_abajo2.png'),
            pygame.image.load(
                'TheLegendOfZelda/imagenes/link/link_abajo3.png'),
            pygame.image.load(
                'TheLegendOfZelda/imagenes/link/link_abajo4.png'),
            pygame.image.load(
                'TheLegendOfZelda/imagenes/link/link_abajo5.png'),
            pygame.image.load(
                'TheLegendOfZelda/imagenes/link/link_abajo6.png'),
            pygame.image.load(
                'TheLegendOfZelda/imagenes/link/link_abajo7.png'),
            pygame.image.load(
                'TheLegendOfZelda/imagenes/link/link_abajo8.png'),
            pygame.image.load(
                'TheLegendOfZelda/imagenes/link/link_abajo9.png'),
            pygame.image.load(
                'TheLegendOfZelda/imagenes/link/link_abajo10.png'),
            pygame.image.load('TheLegendOfZelda/imagenes/link/link_abajo11.png')]
        self.salta = [pygame.image.load('TheLegendOfZelda/imagenes/link/link_salto1.png'),
                      pygame.image.load('TheLegendOfZelda/imagenes/link/link_salto2.png')]

        self.vida = 100

        # Contador de pasos
        self.cuentaPasos += 0

    def update(self):
        # si el fotograma pasa de 6, vuelve a 0 haciendo que se vea animado
        if self.cuentaPasos + 1 >= 6:

            self.cuentaPasos = 0
    # Movimiento a la izquierda

        if self.izquierda:
            self.image = (
                self.caminaIzquierda[self.cuentaPasos // 1])
            self.rect = self.image.get_rect()
            self.rect.x = self.px
            self.rect.y = self.py
            self.cuentaPasos += 1

        # Movimiento a la derecha
        elif self.derecha:
            self.image = (
                self.caminaDerecha[self.cuentaPasos // 1])
            self.rect = self.image.get_rect()
            self.rect.x = self.px
            self.rect.y = self.py
            self.cuentaPasos += 1
# Movimiento arriba

        elif self.arriba:
            self.image = (
                self.caminaArriba[self.cuentaPasos // 1])
            self.rect = self.image.get_rect()
            self.rect.x = self.px
            self.rect.y = self.py
            self.cuentaPasos += 1
        # Movimiento abajo
        elif self.abajo:
            self.image = (
                self.caminaAbajo[self.cuentaPasos // 1])
            self.rect = self.image.get_rect()
            self.rect.x = self.px
            self.rect.y = self.py
            self.cuentaPasos += 1
        # Salto
        elif self.salto + 1 >= 2:
            self.image = (
                self.salta[self.cuentaPasos // 1])
            self.rect = self.image.get_rect()
            self.rect.x = self.px
            self.rect.y = self.py
            self.cuentaPasos += 1
        # quieto
        else:
            self.image = (
                self.quieto)
            self.rect = self.image.get_rect()
            self.rect.x = self.px
            self.rect.y = self.py
        keys = pygame.key.get_pressed()
        # Tecla A - Moviemiento a la izquierda
        if keys[pygame.K_LEFT] and self.px > self.velocidad:
            self.px -= self.velocidad
            self.izquierda = True
            self.derecha = False
            self.arriba = False
            self.abajo = False
    # Tecla D - Moviemiento a la derecha
        elif keys[pygame.K_RIGHT] and self.px < 1000 - self.velocidad - self.ancho:
            self.px += self.velocidad
            self.izquierda = False
            self.derecha = True
            self.arriba = False
            self.abajo = False
# Tecla W - Moviemiento hacia arriba
        elif keys[pygame.K_UP] and self.py > 400:
            self.py -= self.velocidad
            self.izquierda = False
            self.derecha = False
            self.arriba = True
            self.abajo = False

    # Tecla S - Moviemiento hacia abajo
        elif keys[pygame.K_DOWN] and self.py < 500:
            self.py += self.velocidad
            self.izquierda = False
            self.derecha = False
            self.arriba = False
            self.abajo = True
    # Personaje quieto
        else:
            self.izquierda = False
            self.derecha = False
            self.arriba = False
            self.abajo = False
            self.cuentaPasos = 0

    # Tecla SPACE - Salto
        if not self.salto:
            if keys[pygame.K_SPACE]:
                self.salto = True
                self.izquierda = False
                self.derecha = False
                self.cuentaPasos = 0
        else:
            if self.cuentaSalto >= -10:
                self.py -= (self.cuentaSalto * abs(self.cuentaSalto)) * 0.5
                self.cuentaSalto -= 2
            else:
                self.cuentaSalto = 10
                self.salto = False
# Metodo disparar

    def disparar(self):
        bala = Balas(self.rect.centerx, self.rect.top)
        grupo_jugador.add(bala)
        grupo_balas_jugador.add(bala)
        laser_sonido.play()

# Clase enemigos


class Enemigos (pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(
            'TheLegendOfZelda/imagenes/enemigo/pulpo.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1, W-50)
        self.rect.y = 10
        self.velocidad_y = random.randrange(-5, 20)
# Generacion de enemigos aleatoriamente

    def update(self):
        self.time = random.randrange(-1, pygame.time.get_ticks()//5000)
        self.rect.x += self.time
        if self.rect.x >= W:
            self.rect.x = 0
            self.rect.y += 50
# metodo para que los enemigos disparen

    def disparar_enemigos(self):
        bala = Balas_enemigos(self.rect.centerx,  self.rect.bottom)
        grupo_jugador.add(bala)
        grupo_balas_enemigos.add(bala)
        laser_enemigo.play()
# clase de disparos


class Balas (pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(
            'TheLegendOfZelda/imagenes/link/espada.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.velocidad = -18

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0:
            self.kill()
# clase para las balas


class Balas_enemigos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(
            'TheLegendOfZelda/imagenes/enemigo/bala.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = random.randrange(10, W)
        self.velocidad_y = 4

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom > H:
            self.kill()
    # clase para la animacion explosion


class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = explosion_list[0]
        # redimiensionamos la escala de la imagen
        img_scala = pygame.transform.scale(self.image, (20, 20))
        self.rect = img_scala.get_rect()
        self.rect.center = position
        self.time = pygame.time.get_ticks()
        self.velocidad_explo = 30
        self.frames = 0

    def update(self):
        tiempo = pygame.time.get_ticks()
        if tiempo - self.time > self.velocidad_explo:
            self.time = tiempo
            self.frames += 1
            if self.frames == len(explosion_list):
                self.kill()
            else:
                position = self.rect.center
                self.image = explosion_list[self.frames]
                self.rect = self.image.get_rect()
                self.rect.center = position

# Definimos fondo  y tambien el texto, para la introduccion


def show_go_screen():

    PANTALLA.blit(intro, [0, 0])
    draw_text_negro(PANTALLA, "Presione cualquier boton para iniciar",
                    51, W // 2, H * 3/4)
    draw_text(PANTALLA, "Presione cualquier boton para iniciar",
              50, W // 2, H * 3/4)

    pygame.display.flip()
    waiting = True
    while waiting:
        reloj.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


# grupo de sprites
grupo_jugador = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_balas_jugador = pygame.sprite.Group()
grupo_balas_enemigos = pygame.sprite.Group()

# Posicion de la pantalla
POS = 0
# Grupo sprite
grupo_personaje = pygame.sprite.Group()
personaje = Jugador()
grupo_personaje.add(personaje)
# arrancamos juego
ejecuta = True
grupo_balas_jugador.add(personaje)
# Generacion de enemigos
for x in range(10):
    enemigo = Enemigos(10, 10)
    grupo_enemigos.add(enemigo)
    grupo_jugador.add(enemigo)
game_over = True
# Bucle de acciones y controles
while ejecuta:
    # FPS
    reloj.tick(30)
    # Pantalla de inicio
    if game_over:
        show_go_screen()
        game_over = False
        grupo_personaje.update()
        grupo_enemigos.update()
        grupo_balas_jugador.update()
        grupo_balas_enemigos.update()
    # Bucle del juego
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            ejecuta = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                personaje.disparar()

    # Fondo en movimiento
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_RIGHT]:
        POS -= 5
    if teclas[pygame.K_LEFT]:
        POS += 5
    colicion1 = pygame.sprite.groupcollide(
        grupo_enemigos, grupo_balas_jugador, True, True)
    # colicion de jugador a enemigo
    for i in colicion1:
        score += 10
        enemigo.disparar_enemigos()
        enemigo = Enemigos(300, 10)
        grupo_enemigos.add(enemigo)
        grupo_jugador.add(enemigo)

        explo = Explosion(i.rect.center)
        grupo_jugador.add(explo)
        explosion_sonido.set_volume(0.3)
        explosion_sonido.play()
# Colicion de enemigo a jugador
    colicion2 = pygame.sprite.spritecollide(
        personaje, grupo_balas_enemigos, True)
    for j in colicion2:
        personaje.vida -= 10

        if personaje.vida <= 0:
            # Bucle de game over y pantalla de inicio
            print("GAME OVER")

            game_over = True
            personaje.vida = +100
            score = 0
            explo1 = Explosion(j.rect.center)
            grupo_jugador.add(explo1)

        herida_sonido.set_volume(3)
        herida_sonido.play()
    # Colision directa enemigo
    hits = pygame.sprite.spritecollide(personaje, grupo_enemigos, False)
    for hit in hits:
        personaje.vida - 1000
        enemigos = Enemigos(10, 10)
        grupo_jugador.add(enemigos)
        grupo_enemigos.add(enemigos)
        if personaje.vida <= 0:
            ejecuta = False


# Movimiento en fondo
    x_relativa = POS % fondo.get_rect().width
    PANTALLA.blit(fondo, (x_relativa - fondo.get_rect().width, 0))
    if x_relativa < W:
        PANTALLA.blit(fondo, (x_relativa, 0))
# Dibujamos la pantalla y los personajes
    grupo_personaje.draw(PANTALLA)
    grupo_enemigos.draw(PANTALLA)
    grupo_balas_jugador.draw(PANTALLA)

    grupo_balas_enemigos.draw(PANTALLA)
    # Actualizamos pantalla
    grupo_personaje.update()
    grupo_enemigos.update()
    grupo_balas_jugador.update()
    grupo_balas_enemigos.update()
    # Puntuacion
    texto_puntuacion(
        PANTALLA, ('Puntos: '+str(score)+'          '), 30, W-85, 2)
    # Barra de vida
    barra_vida(PANTALLA, W - 305, 0, personaje.vida)
    pygame.display.update()
    # Llamada a la función de actualización de la ventana
    pygame.display.flip()

# Salida del juego
pygame.quit()
