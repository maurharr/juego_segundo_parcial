import pygame
from config import *
from sprite_sheet import SpriteSheet
from misil import MisilEnemigo, MisilBoss
from utils import *


class Enemigo(pygame.sprite.Sprite):
    
    def __init__(self, groups, escala, tipo, x, y, plataformas, all_sprites, enemy_shoot, sonidos):
        
        super().__init__(groups)

        # Manejo de sprites del enemigo
        sprite_sheet_enemy = SpriteSheet(pygame.image.load("./src/assets/images/characters.png").convert_alpha(), 4, 24, WIDTH_BODY, HEIGHT_BODY, ["front", "left", "right", "back"])
        self.animaciones = sprite_sheet_enemy.get_animations_dict(escala)
        self.sprite_actual = 22
        self.image = self.animaciones["right"][self.sprite_actual]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.ultima_actualizacion = pygame.time.get_ticks()

        # Manejo de los misiles del enemigo
        self.vel_y = 0
        self.fuerza_salto = -10
        self.tipo = tipo

        # Grupo de sprites
        self.plataformas = plataformas
        self.all_sprites = all_sprites
        self.enemy_shoot = enemy_shoot

        # Configuración del sonido
        self.sonidos = sonidos
         
        # Configuración del enemigo 1
        if self.tipo == 1:
            self.sprite_actual = 0
            self.time_animation = 150
            self.vel_x = 4
            self.disparos_restantes = 5

        # Configuración del enemigo 2
        if self.tipo == 2:
            self.sprite_actual = 3
            self.time_animation = 150
            self.vel_x = 2
            self.disparos_restantes = 4

        # Configuración del enemigo 3
        if self.tipo == 3:
            self.sprite_actual = 13
            self.time_animation = 150
            self.vel_x = 6
            self.disparos_restantes = 2

        # Configuración del enemigo 4
        if self.tipo == 4:
            self.sprite_actual = 16
            self.time_animation = 150
            self.vel_x = 6
            self.disparos_restantes = 2

        # Configuración del enemigo 5
        if self.tipo == 5:
            self.sprite_actual = 22
            self.vel_x = 0
            self.image = self.animaciones["left"][self.sprite_actual]
            self.disparos_restantes = 4
            self.shoot_interval = 1000 #Milisegundos

        # Configuración del enemigo 6
        if self.tipo == 6:
            self.sprite_actual = 6
            self.vel_x = 0
            self.image = self.animaciones["left"][self.sprite_actual]
            self.disparos_restantes = 50
            self.shoot_interval = 1000 #Milisegundos

        # Configuración de la velocidad del Jefe
        self.velocidad = 5

    # Restar un disparo al contador
    def reducir_disparo(self):
        self.disparos_restantes -= 1
        if self.disparos_restantes <= 0:
            self.kill()


    def update(self):
        current_time = pygame.time.get_ticks()

        # Actualización del enemigo 1
        if self.tipo == 1:
            if current_time - self.ultima_actualizacion >= self.time_animation:
                self.sprite_actual += 1
                if self.sprite_actual == 2:
                    self.sprite_actual = 0
                self.ultima_actualizacion = current_time

                if self.vel_x > 0:
                    self.image = self.animaciones["right"][self.sprite_actual]
                elif self.vel_x < 0:
                    self.image = self.animaciones["left"][self.sprite_actual]
            self.rect.x += self.vel_x # Mover enemigo

            for plataforma in self.plataformas: # Cambiar dirección al llegar a los bordes
                if self.rect.colliderect(plataforma.rect) or self.rect.colliderect(plataforma.rect_left) or self.rect.colliderect(plataforma.rect_right): 
                    self.vel_x = -self.vel_x 

        # Actualización del enemigo 2
        if self.tipo == 2:
            if current_time - self.ultima_actualizacion >= self.time_animation:
                self.sprite_actual += 1
                if self.sprite_actual == 5:
                    self.sprite_actual = 3
                self.ultima_actualizacion = current_time

                if self.vel_x > 0:
                    self.image = self.animaciones["right"][self.sprite_actual]
                elif self.vel_x < 0:
                    self.image = self.animaciones["left"][self.sprite_actual]
            self.rect.x += self.vel_x

            for plataforma in self.plataformas:
                if self.rect.colliderect(plataforma.rect) or self.rect.colliderect(plataforma.rect_left) or self.rect.colliderect(plataforma.rect_right):
                    self.vel_x = -self.vel_x 

        # Actualización del enemigo 3
        if self.tipo == 3:
            if current_time - self.ultima_actualizacion >= self.time_animation:
                self.sprite_actual += 1
                if self.sprite_actual == 15:
                    self.sprite_actual = 13
                self.ultima_actualizacion = current_time

                if self.vel_x > 0:
                    self.image = self.animaciones["left"][self.sprite_actual]
                elif self.vel_x < 0:
                    self.image = self.animaciones["right"][self.sprite_actual]
            self.rect.x -= self.vel_x 
            
            for plataforma in self.plataformas:
                if self.rect.colliderect(plataforma.rect) or self.rect.colliderect(plataforma.rect_left) or self.rect.colliderect(plataforma.rect_right):
                    self.vel_x = -self.vel_x 

        # Actualización del enemigo 4
        if self.tipo == 4:
            if current_time - self.ultima_actualizacion >= self.time_animation:
                self.sprite_actual += 1
                if self.sprite_actual == 18:
                    self.sprite_actual = 16
                self.ultima_actualizacion = current_time

                if self.vel_x > 0:
                    self.image = self.animaciones["left"][self.sprite_actual]
                elif self.vel_x < 0:
                    self.image = self.animaciones["right"][self.sprite_actual]
            self.rect.x -= self.vel_x 

            for plataforma in self.plataformas:
                if self.rect.colliderect(plataforma.rect) or self.rect.colliderect(plataforma.rect_left) or self.rect.colliderect(plataforma.rect_right):
                    self.vel_x = -self.vel_x  

        # Actualización del enemigo 5
        if self.tipo == 5:

            if current_time - self.ultima_actualizacion >= self.shoot_interval:
                self.ultima_actualizacion = current_time  # Actualizar el tiempo del último disparo
                self.disparar()  # Realizar el disparo
                if self.rect.left < WIDTH:
                    self.sonidos.reproducir_disparo()


        #--------- GRAVEDAD ------------
        if self.tipo != 6:
            self.vel_y += GRAVITY
            self.rect.y += self.vel_y
        #-------------------------------


    def saltar(self):
        self.vel_y += self.fuerza_salto
        self.tocando_piso = False


    def disparar(self):
        MisilEnemigo([self.all_sprites, self.enemy_shoot], (self.rect.left, self.rect.centery), "left")

    def disparo_boss(self):
        MisilBoss([self.all_sprites, self.enemy_shoot], (self.rect.left, self.rect.centery), "left")

