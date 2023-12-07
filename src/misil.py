import pygame
from pygame.locals import *
from config import *


class Misil(pygame.sprite.Sprite):

    def __init__(self, groups, coordenadas, dir=None) -> None:

        super().__init__(*groups)

        self.image = pygame.transform.scale(pygame.image.load("./src/assets/images/energy_ball.png").convert_alpha(), (40, 20))
        self.rect = self.image.get_rect(midright = coordenadas)
        if dir == "right":
            self.speed_x = 10
        if dir == "left":
            self.speed_x = -10

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left >= WIDTH:
            self.kill() #Eliminamos el misil
        if self.rect.right <= 0:
            self.kill()


class MisilEnemigo(pygame.sprite.Sprite):

    def __init__(self, groups, coordenadas, dir) -> None:

        super().__init__(*groups)

        self.image = pygame.transform.scale(pygame.image.load("./src/assets/images/energy_ball_2.png").convert_alpha(), (40, 20))
        self.rect = self.image.get_rect(center= coordenadas)
        self.speed_x = 10

    def update(self):
        self.rect.x -= self.speed_x
        if self.rect.right <= 0:
            self.kill()
        if self.rect.left >= WIDTH:
            self.kill()



class MisilBoss(pygame.sprite.Sprite):

    def __init__(self, groups, coordenadas, dir) -> None:

        super().__init__(*groups)

        self.image = pygame.transform.scale(pygame.image.load("./src/assets/images/energy_ball_3.png").convert_alpha(), (40, 20))
        self.rect = self.image.get_rect(center= coordenadas)
        self.speed_x = 15

    def update(self):
        self.rect.x -= self.speed_x
        if self.rect.right <= 0:
            self.kill()
        if self.rect.left >= WIDTH:
            self.kill()
