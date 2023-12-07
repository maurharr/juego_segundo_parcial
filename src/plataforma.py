import pygame
from pygame.locals import *



class Platform(pygame.sprite.Sprite):

    def __init__(self, groups, image, rectangulo: pygame.Rect):
        super().__init__(groups)

        # Cargar la imagen y escalarla
        scaled_width = rectangulo[2]
        scaled_height = rectangulo[3]
        self.image = pygame.transform.scale(image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect(topleft=(rectangulo[0], rectangulo[1]))


        # Crear rectángulos a cada lado
        altura_barra = 60  # Puedes ajustar el espacio entre los rectángulos
        alto_barra = 50
        padding = 10
        self.rect_left = pygame.Rect(self.rect.left - padding, self.rect.top - altura_barra, padding, alto_barra)
        self.rect_right = pygame.Rect(self.rect.right, self.rect.top - altura_barra, padding, alto_barra)


class VerticalPlatform(pygame.sprite.Sprite):

    def __init__(self, groups, image, rectangulo: pygame.Rect, velocidad):
        super().__init__(groups)

        # Cargar la imagen y escalarla
        scaled_width = int(rectangulo[2])
        scaled_height = int(rectangulo[3])
        self.image = pygame.transform.scale(image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect(topleft=(rectangulo[0], rectangulo[1]))

        # Movimiento
        self.velocidad = velocidad

    def update(self):
        # Actualizar la posición en cada fotograma
        self.rect.y += self.velocidad

        # Comprobar límites y cambiar dirección si es necesario
        if self.rect.top <= 250 and self.velocidad < 0:
            self.velocidad = -self.velocidad
        elif self.rect.bottom >= 550 and self.velocidad > 0:
            self.velocidad = -self.velocidad

