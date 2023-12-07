import pygame
from config import *
from utils import mostrar_texto

class UI:
    def __init__(self, superficie, fuente):

        # configuración
        self.superficie = superficie
        self.fuente = fuente

        # barra de vida
        self.barra_salud = pygame.image.load("./src/assets/images/health_bar.png")
        self.barra_salud_topleft = (54, 39)
        self.barra_width_max = 152
        self.barra_height = 4


    def mostrar_vida(self, salud_actual, salud_maxima):
        self.superficie.blit(self.barra_salud, (20, 10))
        radio_salud_actual = salud_actual / salud_maxima
        barra_width_actual = self.barra_width_max * radio_salud_actual
        barra_salud_rect = pygame.Rect((self.barra_salud_topleft),(barra_width_actual,self.barra_height))
        pygame.draw.rect(self.superficie, RED, barra_salud_rect)


    def mostrar_puntos(self, cantidad_puntos):
        mostrar_texto(self.superficie, f"Puntos: {cantidad_puntos}", self.fuente, (30, 75), WHITE, None)

