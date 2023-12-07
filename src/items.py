import pygame



class Item(pygame.sprite.Sprite):

    def __init__(self, groups, image, rectangulo: pygame.Rect):
        super().__init__(groups)

        # Cargar la imagen y escalarla
        scaled_width = int(rectangulo[2])
        scaled_height = int(rectangulo[3])
        self.image = pygame.transform.scale(image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect(topleft=(rectangulo[0], rectangulo[1]))