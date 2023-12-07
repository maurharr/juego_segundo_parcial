import pygame
from pygame.locals import *
from config import *
from sprite_sheet import SpriteSheet
from misil import Misil
from math import sin


class Jugador(pygame.sprite.Sprite):
    
    def __init__(self, groups, scale, all_sprites, jugador_shoot, cambiar_salud, sonidos):    
        super().__init__(groups)

        # Manejo de sprites del jugador
        sprite_sheet_player = SpriteSheet(pygame.image.load("./src/assets/images/characters.png").convert_alpha(), 4, 24, WIDTH_BODY, HEIGHT_BODY, ["front", "left", "right", "back"])
        self.animaciones = sprite_sheet_player.get_animations_dict(scale)
        self.sprite_actual = 9
        self.image = self.animaciones["right"][self.sprite_actual]
        self.rect = self.image.get_rect(topleft=(100, 0))
        self.ultima_actualizacion = pygame.time.get_ticks()
        self.tiempo_animacion = 75

        # Manejo del movimiento del jugador
        self.vel_x = 6
        self.vel_y = 0
        self.fuerza_salto = -18
        self.tocando_piso = False

        # Manejo de los misiles del jugador
        self.puede_disparar = True
        self.direccion_misil = "right"

        # Grupo de sprites
        self.all_sprites = all_sprites
        self.jugador_shoot = jugador_shoot

        # Manejo de la salud del jugador
        self.cambiar_salud = cambiar_salud
        self.inmortalidad = False
        self.inmortalidad_duracion = 2000
        self.daño_tiempo = 0
        self.sonidos = sonidos

    def manejar_eventos(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if keys[K_d]:
            self.direccion_misil = "right"
            if self.rect.right < WIDTH:
                self.rect.x += self.vel_x
                if current_time - self.ultima_actualizacion >= self.tiempo_animacion:
                    self.sprite_actual += 1
                    self.image = self.animaciones["right"][self.sprite_actual]
                    if self.sprite_actual == 11:
                        self.sprite_actual = 9
                    self.ultima_actualizacion = current_time

        if keys[K_a]:
            self.direccion_misil = "left"
            if self.rect.left > 0:
                self.rect.x -= self.vel_x
                if current_time - self.ultima_actualizacion >= self.tiempo_animacion:
                    self.sprite_actual += 1
                    self.image = self.animaciones["left"][self.sprite_actual]
                    if self.sprite_actual == 11:
                        self.sprite_actual = 9
                    self.ultima_actualizacion = current_time

        if keys[K_SPACE] and self.tocando_piso: #Si apreto SPACE y mi PJ esta en el piso
            self.saltar()

        if keys[K_LCTRL] and self.puede_disparar:  
            self.disparar()
            self.puede_disparar = False
            self.sonidos.reproducir_disparo()

        if not keys[K_LCTRL]:
            self.puede_disparar = True

        # Gravedad
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y


    def saltar(self):
        self.vel_y += self.fuerza_salto
        self.tocando_piso = False


    def disparar(self):
        # Aquí puedes agregar lógica para crear instancias de misiles o realizar acciones de disparo
        if self.direccion_misil == "left":
            Misil([self.all_sprites, self.jugador_shoot], (self.rect.left, self.rect.centery), 'left')
        else:
            Misil([self.all_sprites, self.jugador_shoot], (self.rect.right+30, self.rect.centery), 'right')
     

    def recibir_daño(self):
        if not self.inmortalidad:
            self.cambiar_salud(-33)
            self.inmortalidad = True
            self.daño_tiempo = pygame.time.get_ticks()
            self.sonidos.reproducir_jugador_lastimado()
            

    def inmortalidad_timer(self):
        if self.inmortalidad:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.daño_tiempo >= self.inmortalidad_duracion:
                self.inmortalidad = False


    def valor_onda(self):
        valor = sin(pygame.time.get_ticks())
        if valor >= 0:
            return 255
        else:
            return 0


    def animar(self):
        if self.inmortalidad:
            transparencia = self.valor_onda()
            self.image.set_alpha(transparencia)
        else:
            self.image.set_alpha(255)


    def update(self):
        self.manejar_eventos()
        self.inmortalidad_timer()
        self.valor_onda()
        self.animar()
