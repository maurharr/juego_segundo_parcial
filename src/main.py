import pygame
from pygame.locals import *
from config import *
from niveles import Nivel
from ui import UI
from utils import *
from sonidos import Sonidos
import json


class Game:
    
    def __init__(self) -> None:
        
        # Inicializar modulos de Pygame
        pygame.init()

        # Pantalla
        self.superficie = pygame.display.set_mode((resolucion))
        pygame.display.set_caption("2do juego de Programación")

        # Configuración de reloj
        self.clock = pygame.time.Clock()

        # Configuración del buble principal
        self.is_running = True

        # Definir fuentes para los textos
        self.fuente = pygame.font.Font("./src/assets/fonts/BlockKie.ttf", 36)  
        self.fuente_pausa = pygame.font.Font("./src/assets/fonts/BlockKie.ttf", 72)
        self.fuente_botones = pygame.font.Font("./src/assets/fonts/BlockKie.ttf", 54)
        self.fuente_titulo = pygame.font.Font("./src/assets/fonts/ARCADEPI.ttf", 46)
        self.fuente_texto = pygame.font.Font("./src/assets/fonts/ARCADEPI.ttf", 28)
        self.fuente_color = WHITE

        # Configuración del sonido
        self.sonidos = Sonidos()

        # Configuración del fondo
        self.background = pygame.image.load("./src/assets/images/background_menu.png").convert_alpha()
        self.background_rect = self.background.get_rect()
        self.background_x = 0
        self.background_y = 0

        # Configuración de la salud
        self.salud_maxima = 99
        self.salud_actual = 99

        # Configuración de los puntos
        self.cantidad_puntos = 0

        # Textdraw
        self.ui = UI(self.superficie, self.fuente)

        # Flags de niveles
        self.flag_mostrar_controles = True
        self.desbloquear_nivel_2 = False
        self.desbloquear_nivel_3 = False

        # Inicio el menú
        self.menu_principal()


    def menu_principal(self):
        self.entro_al_menu = True
        self.sonidos.activar_musica_menu()
        while self.entro_al_menu:
            self.superficie.blit(self.background, ORIGEN)
            pausa_rect = crear_rectangulo(None, 350, 100, 500, 400, MENU_COLOR, 0)
            pygame.draw.rect(self.superficie, pausa_rect["color"], pausa_rect["rect"], pausa_rect["radio"])
            mostrar_texto(self.superficie, "Rebel Skeleton", self.fuente_titulo, (390, 130), self.fuente_color, None)
            boton_jugar = crear_boton(self.superficie, 532, 220, 130, 50, MENU_BOTON_COLOR, 0, 3, "JUGAR", self.fuente_botones)
            boton_opciones = crear_boton(self.superficie, 503, 320, 193, 50, MENU_BOTON_COLOR, 0, 3, "OPCIONES", self.fuente_botones)
            boton_salir = crear_boton(self.superficie, 540, 420, 115, 50, MENU_BOTON_COLOR, 0, 3, "SALIR", self.fuente_botones)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminar()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        terminar()

                if event.type == MOUSEBUTTONDOWN:
                    if boton_jugar["rect"].collidepoint(event.pos):
                        self.seleccionar_nivel()
                    if boton_opciones["rect"].collidepoint(event.pos):
                        self.opciones()
                    if boton_salir["rect"].collidepoint(event.pos):
                        terminar()


    def opciones(self):

        while True:
            pausa_rect = crear_rectangulo(None, 350, 100, 500, 400, MENU_COLOR, 0)
            pygame.draw.rect(self.superficie, pausa_rect["color"], pausa_rect["rect"], pausa_rect["radio"])
            mostrar_texto(self.superficie, "Opciones", self.fuente_titulo, (485, 130), self.fuente_color, None)

            boton_sonido_dct = crear_boton(self.superficie, 486, 220, 228, 35, MENU_BOTON_COLOR_2, 0, 3, "DESACTIVAR SFX", self.fuente)
            boton_sonido_act = crear_boton(self.superficie, 513, 275, 173, 35, MENU_BOTON_COLOR, 0, 3, "ACTIVAR SFX", self.fuente)
            boton_musica_dct = crear_boton(self.superficie, 462, 330, 276, 35, MENU_BOTON_COLOR_2, 0, 3, "DESACTIVAR MUSICA", self.fuente)
            boton_musica_act = crear_boton(self.superficie, 489, 390, 222, 35, MENU_BOTON_COLOR, 0, 3, "ACTIVAR MUSICA", self.fuente)
            boton_retroceder = crear_boton(self.superficie, 512, 450, 176, 35, MENU_BOTON_COLOR_2, 0, 3, "RETROCEDER", self.fuente)
            pygame.display.flip() 
        
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminar()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    
                if event.type == MOUSEBUTTONDOWN:
                    if boton_sonido_dct["rect"].collidepoint(event.pos):
                        self.sonidos.apagar_sonido()
                    elif boton_sonido_act["rect"].collidepoint(event.pos):
                        self.sonidos.encender_sonido()
                    elif boton_musica_dct["rect"].collidepoint(event.pos):
                        self.sonidos.apagar_musica()
                    elif boton_musica_act["rect"].collidepoint(event.pos):
                        self.sonidos.activar_musica_menu()
                    elif boton_retroceder["rect"].collidepoint(event.pos):
                        return
                    

    def seleccionar_nivel(self):

        while True:
            
            self.superficie.blit(self.background, ORIGEN)
            nivel_rect = crear_rectangulo(None, 50, 100, 500, 400, MENU_COLOR, 0)
            pygame.draw.rect(self.superficie, nivel_rect["color"], nivel_rect["rect"], nivel_rect["radio"])
            mostrar_texto(self.superficie, "Selecciona nivel", self.fuente_titulo, (70, 130), self.fuente_color, None)

            boton_nivel_1 = crear_boton(self.superficie, 250, 220, 100, 35, MENU_BOTON_COLOR, 0, 3, "NIVEL 1", self.fuente)

            if not self.desbloquear_nivel_2:
                boton_nivel_2 = crear_boton(self.superficie, 250, 275, 100, 35, MENU_BOTON_COLOR_2, 0, 3, "NIVEL 2", self.fuente)
            else:
                boton_nivel_2 = crear_boton(self.superficie, 250, 275, 100, 35, MENU_BOTON_COLOR, 0, 3, "NIVEL 2", self.fuente)

            if not self.desbloquear_nivel_3:
                boton_nivel_3 = crear_boton(self.superficie, 250, 330, 100, 35, MENU_BOTON_COLOR_2, 0, 3, "NIVEL 3", self.fuente)
            else:
                boton_nivel_3 = crear_boton(self.superficie, 250, 330, 100, 35, MENU_BOTON_COLOR, 0, 3, "NIVEL 3", self.fuente)

            boton_retroceder = crear_boton(self.superficie, 212, 420, 176, 35, MENU_BOTON_COLOR_2, 0, 3, "RETROCEDER", self.fuente)

            tabla_rect = crear_rectangulo(None, 650, 100, 500, 400, MENU_COLOR, 0)
            pygame.draw.rect(self.superficie, tabla_rect["color"], tabla_rect["rect"], tabla_rect["radio"])
            mostrar_texto(self.superficie, "Tabla posiciones", self.fuente_titulo, (670, 130), self.fuente_color, None)
            self.mostrar_puntuaciones()
            pygame.display.flip() 
        

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminar()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    
                if event.type == MOUSEBUTTONDOWN:
                    if boton_nivel_1["rect"].collidepoint(event.pos):
                        self.sonidos.apagar_musica()
                        self.mostrar_controles()
                        self.desbloquear_nivel_2 = False
                        self.nivel = Nivel("./src/data/nivel_1.json", 1, self.superficie, self.cambiar_salud, self.sumar_puntos, self.sonidos, self.fuente, self.game_over, self.siguiente_nivel, self.menu_principal, self.reiniciar_stats, self.terminar_juego, self.calculo_puntos)
                        self.run()
                    
                    elif boton_nivel_2["rect"].collidepoint(event.pos):
                        if self.desbloquear_nivel_2:
                            self.sonidos.apagar_musica()
                            self.nivel = Nivel("./src/data/nivel_2.json", 2, self.superficie, self.cambiar_salud, self.sumar_puntos, self.sonidos, self.fuente, self.game_over, self.siguiente_nivel, self.menu_principal, self.reiniciar_stats, self.terminar_juego, self.calculo_puntos)
                            self.run()

                    elif boton_nivel_3["rect"].collidepoint(event.pos):
                        if self.desbloquear_nivel_3:
                            self.sonidos.apagar_musica()
                            self.nivel = Nivel("./src/data/nivel_3.json", 3, self.superficie, self.cambiar_salud, self.sumar_puntos, self.sonidos, self.fuente, self.game_over, self.siguiente_nivel, self.menu_principal, self.reiniciar_stats, self.terminar_juego, self.calculo_puntos)
                            self.run()
                    
                    elif boton_retroceder["rect"].collidepoint(event.pos):
                        self.menu_principal()


    def game_over(self):

        self.sonidos.apagar_musica()
        while True:

            self.superficie.fill(BLACK)
            game_over_rect = crear_rectangulo(None, 350, 100, 500, 400, MENU_COLOR, 0)
            pygame.draw.rect(self.superficie, game_over_rect["color"], game_over_rect["rect"], game_over_rect["radio"])
            mostrar_texto(self.superficie, "GAME OVER", self.fuente_titulo, (450, 130), self.fuente_color, None)
            boton_salir = crear_boton(self.superficie, 540, 420, 115, 50, MENU_BOTON_COLOR, 0, 3, "SALIR", self.fuente_botones)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminar()

                if event.type == MOUSEBUTTONDOWN:
                    if boton_salir["rect"].collidepoint(event.pos):
                        self.reiniciar_stats()
                        self.seleccionar_nivel()


    def terminar_juego(self):
        self.sonidos.apagar_musica()
        input_box = pygame.Rect(360, 300, 200, 32)
        color_inactivo = MENU_BOTON_COLOR_2
        color_activo = BLACK
        color_texto = WHITE 
        color = color_inactivo
        prompt_texto = ""
        prompt_activo = False

        while True:
            self.superficie.fill(BLACK)

            terminar_juego_rect = crear_rectangulo(None, 350, 100, 500, 400, MENU_COLOR, 0)
            pygame.draw.rect(self.superficie, terminar_juego_rect["color"], terminar_juego_rect["rect"], terminar_juego_rect["radio"])
            mostrar_texto(self.superficie, "COMPLETASTE EL", self.fuente_titulo, (352, 130), self.fuente_color, None)
            mostrar_texto(self.superficie, "JUEGO", self.fuente_titulo, (500, 170), self.fuente_color, None)
            mostrar_texto(self.superficie, f"Puntuacion: {self.cantidad_puntos}", self.fuente_botones, (360, 250), self.fuente_color, None)
            boton_salir = crear_boton(self.superficie, 540, 420, 115, 50, MENU_BOTON_COLOR, 0, 3, "SALIR", self.fuente_botones)

            sup_texto = self.fuente.render(prompt_texto, True, color_texto)
            prompt_width = max(300, sup_texto.get_width() + 15)
            input_box.w = prompt_width

            pygame.draw.rect(self.superficie, color, input_box)
            self.superficie.blit(sup_texto, (input_box.x + 5, input_box.y + 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminar()

                if event.type == MOUSEBUTTONDOWN:
                    if boton_salir["rect"].collidepoint(event.pos):
                        self.reiniciar_stats()
                        self.seleccionar_nivel()
                    elif input_box.collidepoint(event.pos):
                        prompt_activo = not prompt_activo
                        if prompt_activo:
                            color = color_activo
                        else:
                            color = color_inactivo
                    else:
                        prompt_activo = False
                        color = color_inactivo

                if event.type == KEYDOWN:
                    if prompt_activo:
                        if event.key == K_RETURN:
                            self.guardar_puntuacion(prompt_texto, self.cantidad_puntos)
                            prompt_texto = ""
                        elif event.key == K_BACKSPACE:
                            prompt_texto = prompt_texto[:-1]
                        else:
                            prompt_texto += event.unicode


    def mostrar_controles(self):
        
        while self.flag_mostrar_controles:

            self.superficie.fill(BLACK)
            rect = crear_rectangulo(None, 350, 100, 500, 400, MENU_COLOR, 0)
            pygame.draw.rect(self.superficie, rect["color"], rect["rect"], rect["radio"])
            mostrar_texto(self.superficie, "CONTROLES", self.fuente_titulo, (450, 130), self.fuente_color, None)
            mostrar_texto(self.superficie, "Te moves con A y D", self.fuente, (450, 200), self.fuente_color, None)
            mostrar_texto(self.superficie, "Saltas con Espacio", self.fuente, (450, 250), self.fuente_color, None)
            mostrar_texto(self.superficie, "Disparas con CRTL", self.fuente, (450, 300), self.fuente_color, None)
            boton_jugar = crear_boton(self.superficie, 540, 420, 130, 50, MENU_BOTON_COLOR, 0, 3, "JUGAR", self.fuente_botones)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminar()

                if event.type == MOUSEBUTTONDOWN:
                    if boton_jugar["rect"].collidepoint(event.pos):
                        self.flag_mostrar_controles = False
                        pass


    def reiniciar_stats(self):
        self.cantidad_puntos = 0
        self.salud_actual = 99


    def siguiente_nivel(self):

        self.sonidos.apagar_musica()
        while True:

            self.superficie.fill(BLACK)
            signivel_rect = crear_rectangulo(None, 350, 100, 500, 400, MENU_COLOR, 0)
            pygame.draw.rect(self.superficie, signivel_rect["color"], signivel_rect["rect"], signivel_rect["radio"])
            mostrar_texto(self.superficie, "Pasaste el nivel", self.fuente_titulo, (365, 130), self.fuente_color, None)
            mostrar_texto(self.superficie, "Desbloqueaste el", self.fuente_texto, (450, 200), self.fuente_color, None)
            mostrar_texto(self.superficie, "siguiente nivel!", self.fuente_texto, (450, 230), self.fuente_color, None)
            boton_continuar = crear_boton(self.superficie, 496, 320, 220, 50, MENU_BOTON_COLOR, 0, 3, "CONTINUAR", self.fuente_botones)
            boton_salir = crear_boton(self.superficie, 540, 420, 115, 50, MENU_BOTON_COLOR, 0, 3, "SALIR", self.fuente_botones)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminar()

                if event.type == MOUSEBUTTONDOWN:


                    if boton_continuar["rect"].collidepoint(event.pos):
                        if not self.desbloquear_nivel_2:
                            self.desbloquear_nivel_2 = True
                            self.cantidad_puntos = self.cantidad_puntos 
                            self.nivel = Nivel("./src/data/nivel_2.json", 2, self.superficie, self.cambiar_salud, self.sumar_puntos, self.sonidos, self.fuente, self.game_over, self.siguiente_nivel, self.menu_principal, self.reiniciar_stats, self.terminar_juego, self.calculo_puntos)
                            self.run()       

                        if not self.desbloquear_nivel_3 and self.desbloquear_nivel_2:
                            self.desbloquear_nivel_3 = True
                            self.nivel = Nivel("./src/data/nivel_3.json", 3, self.superficie, self.cambiar_salud, self.sumar_puntos, self.sonidos, self.fuente, self.game_over, self.siguiente_nivel, self.menu_principal, self.reiniciar_stats, self.terminar_juego, self.calculo_puntos)
                            self.run()

                    elif boton_salir["rect"].collidepoint(event.pos):
                        if  not self.desbloquear_nivel_2:
                            self.desbloquear_nivel_2 = True
                            self.reiniciar_stats()
                            self.seleccionar_nivel()

                        if not self.desbloquear_nivel_3 and self.desbloquear_nivel_2:
                            self.desbloquear_nivel_3 = True
                            self.reiniciar_stats()
                            self.seleccionar_nivel()                        


    def sumar_puntos(self, cantidad):
        self.cantidad_puntos += cantidad


    def calculo_puntos(self, cantidad):
        self.cantidad_puntos *= (cantidad * 10)


    def guardar_puntuacion(self, nombre, puntos):
        try:
            with open('./src/data/puntuaciones.json', 'r') as file:
                data = json.load(file)

        except FileNotFoundError:
            data = {"puntuaciones": []}

        # Agrego la nueva puntuación al final de la lista
        data["puntuaciones"].append({"nombre": nombre, "puntos": puntos})

        # Abre el archivo JSON en modo escritura para guardar
        with open('./src/data/puntuaciones.json', 'w') as file:
            json.dump(data, file, indent=4)


    def cargar_puntuaciones(self):
        try:
            with open('./src/data/puntuaciones.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            return [] # Si el archivo no existe, devuelve una lista vacia

        # Ordena la lista de puntuaciones por puntaje de mayor a menor
        puntuaciones_ordenadas = sorted(data["puntuaciones"], key=lambda x: x["puntos"], reverse=True)

        return puntuaciones_ordenadas


    def mostrar_puntuaciones(self):
        puntuaciones = self.cargar_puntuaciones()

        y_pos = 200  # Posición vertical inicial
        for i, puntuacion in enumerate(puntuaciones[:3]):  # Muestra las primeras 3 puntuaciones
            nombre = puntuacion["nombre"]
            puntos = puntuacion["puntos"]
            texto = f"{i + 1}. {nombre}: {puntos} puntos"
            mostrar_texto(self.superficie, texto, self.fuente, (680, y_pos), self.fuente_color, None)
            y_pos += 50


    def cambiar_salud(self, cantidad):
        self.salud_actual += cantidad
        if self.salud_actual > 99:
            self.salud_actual = 99
        if self.salud_actual == 0:
            self.game_over()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.nivel.pausa()
                

    def update(self):
        self.ui.mostrar_vida(self.salud_actual, self.salud_maxima)
        self.ui.mostrar_puntos(self.cantidad_puntos)
        pygame.display.flip()


    def run(self):
        while self.is_running:
            self.clock.tick(FPS)
            self.nivel.update()
            self.handle_events()
            self.update()
        self.close()


    def close(self):
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run() 



