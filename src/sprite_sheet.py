import pygame


class SpriteSheet:

    def __init__(self, sheet:pygame.Surface, rows, cols, width, height, keys = None) -> None:

        self.sheet = sheet
        self.width = self.sheet.get_width()
        self.height = self.sheet.get_height()
        self.rows = rows
        self.cols = cols
        self.width_sprite = width
        self.height_sprite = height
        self.keys = keys


    # Metodo 2
    def get_animations_dict(self, scale = 1):

        self.width = scale * self.width
        self.height = scale * self.height
        self.width_sprite = scale * self.width_sprite
        self.height_sprite = scale * self.height_sprite
        

        self.sheet = pygame.transform.scale(self.sheet, (self.width, self.height))
        cont_cols = 0
        animation_dict = {}

        for row in range(self.rows):
            animation_row = []

            for _ in range(self.cols):
                animation_row.append(self.sheet.subsurface((cont_cols * self.width_sprite, row * self.height_sprite, self.width_sprite, self.height_sprite)))
                cont_cols += 1

            animation_dict[self.keys[row]] = animation_row
            cont_cols = 0
        
        return animation_dict
    
    # Metodo 1
    def get_animations(self, scale = 1):

        self.width = scale * self.width
        self.height = scale * self.height
        self.width_sprite = scale * self.width_sprite
        self.height_sprite = scale * self.height_sprite
        

        self.sheet = pygame.transform.scale(self.sheet, (self.width, self.height))
        cont_cols = 0
        animation_list = []

        for row in range(self.rows):
            animation_row = []

            for _ in range(self.cols):
                animation_row.append(self.sheet.subsurface((cont_cols * self.height_sprite, row * self.width_sprite, self.width_sprite, self.height_sprite)))
                cont_cols += 1

            cont_cols = 0
            animation_list.append(animation_row)
        
        return animation_list
    


    

    # Metodo 3
    def get_animations_list(self, scale = 1):

        self.width = scale * self.width
        self.height = scale * self.height
        self.width_sprite = scale * self.width_sprite
        self.height_sprite = scale * self.height_sprite
        

        self.sheet = pygame.transform.scale(self.sheet, (self.width, self.height))
        cont_cols = 0
        animation_list = []

        for row in range(self.rows):

            for _ in range(self.cols):
                animation_list.append(self.sheet.subsurface((cont_cols * self.height_sprite, row * self.width_sprite, self.width_sprite, self.height_sprite)))
                cont_cols += 1

            cont_cols = 0
        
        return animation_list
    