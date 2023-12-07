import pygame
from pygame.locals import *
from config import *
#--------------------------
from utils import *
import json
#--------------------------
from sprite_sheet import SpriteSheet
from plataforma import Platform, VerticalPlatform
from jugador import Jugador
from enemigo import Enemigo
from items import Item



class Nivel:

    def __init__(self, nivel, nivel_indice, superficie, cambiar_salud, sumar_puntos, sonidos, fuente, game_over, siguiente_nivel, menu_principal, reiniciar_stats, terminar_juego, calculo_puntos):

        # Configuración general
        self.nivel = nivel
        self.nivel_indice = nivel_indice
        self.superficie = superficie

        # Configuración de la salud
        self.cambiar_salud = cambiar_salud

        # Configuración del puntaje
        self.sumar_puntos = sumar_puntos
        self.calculo_puntos = calculo_puntos

        # Configuración de sonidos
        self.sonidos = sonidos
        if self.nivel_indice != 3:
            self.sonidos.activar_musica()
        else:
            self.sonidos.activar_musica_boss()

        # Configuración del game_over
        self.game_over = game_over
        self.siguiente_nivel = siguiente_nivel
        self.menu_principal = menu_principal
        self.reiniciar_stats = reiniciar_stats
        self.terminar_juego = terminar_juego

        # Configuración del background
        if self.nivel_indice == 1:
            self.background = pygame.image.load("./src/assets/images/background.png").convert_alpha()
        elif self.nivel_indice == 2:
            self.background = pygame.image.load("./src/assets/images/background2.png").convert_alpha()
        else:
            self.background = pygame.image.load("./src/assets/images/background3.png").convert_alpha()

        self.background_rect = self.background.get_rect()
        self.background_x = 0
        self.background_y = 0

        # Definir fuentes para los textos
        self.fuente = fuente
        self.fuente_pausa = pygame.font.Font("./src/assets/fonts/BlockKie.ttf", 72)
        self.fuente_botones = pygame.font.Font("./src/assets/fonts/BlockKie.ttf", 54)
        self.fuente_color = WHITE

        # Nueva configuración para el cronómetro
        self.tiempo_inicial = 60

        # Configuración de la lava
        self.lava = pygame.image.load("./src/assets/images/lava.png").convert_alpha()
        self.lava_rect = self.lava.get_rect()
        self.lava_x = 0
        self.lava_y = HEIGHT - 30

        #------------------------------------------------------------------------

        # Grupo de sprite Principal
        self.all_sprites = pygame.sprite.Group()

        # Grupo de Sprites
        self.enemigos = pygame.sprite.Group()
        self.plataformas = pygame.sprite.Group()
        self.jugador_shoot = pygame.sprite.Group()
        self.enemy_shoot = pygame.sprite.Group()

        # Grupos de Sprites para Items
        self.corazones = pygame.sprite.Group()
        self.monedas = pygame.sprite.Group()
        self.relojes = pygame.sprite.Group()
        self.trampas = pygame.sprite.Group()
        self.meta = pygame.sprite.Group()

        #Jugador
        self.jugador = Jugador([self.all_sprites], 2, self.all_sprites, self.jugador_shoot, self.cambiar_salud, self.sonidos)

        #------------------------------------------------------------------------

        # Carga el archivo JSON
        with open(self.nivel, 'r') as file:
            data = json.load(file)

        # Crea instancias de las clases usando la información del JSON
        
        if self.nivel_indice == 3:
            for plataforma_data in data['plataformas']:
                VerticalPlatform([self.all_sprites, self.plataformas], pygame.image.load(plataforma_data['image_path']).convert_alpha(), plataforma_data['rect'], plataforma_data['velocidad'])
        else:
            for plataforma_data in data['plataformas']:
                Platform([self.all_sprites, self.plataformas], pygame.image.load(plataforma_data['image_path']).convert_alpha(), plataforma_data['rect'])

            for item_data in data['trampas']:
                Item([self.all_sprites, self.trampas], pygame.image.load(item_data['image_path']).convert_alpha(), item_data['rect'])

            for item_data in data['meta']:
                Item([self.all_sprites, self.meta], pygame.image.load(item_data['image_path']).convert_alpha(), item_data['rect'])

            for item_data in data['corazones']:
                Item([self.all_sprites, self.corazones], pygame.image.load(item_data['image_path']).convert_alpha(), item_data['rect'])

            for item_data in data['relojes']:
                Item([self.all_sprites, self.relojes], pygame.image.load(item_data['image_path']).convert_alpha(), item_data['rect'])

            for item_data in data['monedas']:
                Item([self.all_sprites, self.monedas], pygame.image.load(item_data['image_path']).convert_alpha(), item_data['rect'])

        for enemigo_data in data['enemigos']:
            Enemigo([self.all_sprites, self.enemigos], enemigo_data['escala'], enemigo_data['type'], enemigo_data['posicion_x'], enemigo_data['posicion_y'], self.plataformas, self.all_sprites, self.enemy_shoot, self.sonidos)


    def colision_meta(self):
        # Colosion del jugador con los corazones
        if pygame.sprite.spritecollide(self.jugador, self.meta, False):
            self.tiempo_almacenado = int(self.tiempo_inicial)
            self.calculo_puntos(int(self.tiempo_inicial))
            self.siguiente_nivel()


    def colision_trampas(self):
        # Colosion del jugador con los corazones
        if pygame.sprite.spritecollide(self.jugador, self.trampas, False):
            self.jugador.recibir_daño()


    def colision_corazones(self):
        # Colosion del jugador con los corazones
        if pygame.sprite.spritecollide(self.jugador, self.corazones, True):
            self.sonidos.reproducir_jugador_get_corazones()
            self.cambiar_salud(33)


    def colision_monedas(self):
        # Colosion del jugador con las monedas
        if pygame.sprite.spritecollide(self.jugador, self.monedas, True):
            self.sonidos.reproducir_jugador_get_monedas()
            self.sumar_puntos(5)


    def colision_relojes(self):
        # Colosion del jugador con los relojes
        if pygame.sprite.spritecollide(self.jugador, self.relojes, True):
            self.sonidos.reproducir_jugador_get_reloj()
            self.tiempo_inicial += 30


    def colision_jugador_plataforma(self):
        # Colosion del jugador con las plataformas para poder subirse encima
        objetos_a_colisionar = pygame.sprite.spritecollide(self.jugador, self.plataformas, False)
        for objeto in objetos_a_colisionar:
            if self.jugador.rect.bottom >= objeto.rect.top and self.jugador.vel_y > 0:
                self.jugador.rect.bottom = objeto.rect.top
                self.jugador.vel_y = 0
                self.jugador.tocando_piso = True


    def colision_enemigo_plataforma(self):
        # Colosion de los enemigos con las plataformas para poder subirse encima
        for enemigo in self.enemigos:
            objetos_a_colisionar = pygame.sprite.spritecollide(enemigo, self.plataformas, False)
            for objeto in objetos_a_colisionar:
                if enemigo.rect.bottom >= objeto.rect.top and enemigo.vel_y > 0:
                    enemigo.rect.bottom = objeto.rect.top
                    enemigo.vel_y = 0
                    enemigo.tocando_piso = True
                    if enemigo.tipo == 3 or enemigo.tipo == 4:
                        enemigo.saltar()


    def movimiento_boss(self):
        for enemigo in self.enemigos:
            if enemigo.tipo == 6:

                velocidad = enemigo.velocidad
                enemigo.rect.y += velocidad

                # Configuración del movimiento
                if enemigo.rect.top <= 0 and velocidad < 0:
                    enemigo.velocidad = -enemigo.velocidad
                if enemigo.rect.bottom >= 600 and velocidad > 0:
                    enemigo.velocidad = -enemigo.velocidad

                # Configuración de las rafagas
                if enemigo.rect.top < 70 and velocidad > 0:
                    enemigo.disparo_boss()
                    self.sonidos.reproducir_disparo()
                elif enemigo.rect.bottom > 530 and velocidad < 0:
                    enemigo.disparo_boss()
                    self.sonidos.reproducir_disparo()


    def detectar_boss_muerto(self):
        if len(self.enemigos) == 0:
            self.tiempo_almacenado = int(self.tiempo_inicial)
            self.calculo_puntos(int(self.tiempo_inicial))
            self.terminar_juego() 


    def colision_bala(self):
        # Colision de los enemigos con las balas del jugador
        hits = pygame.sprite.groupcollide(self.enemigos, self.jugador_shoot, False, True)
        for enemy, shoot_list in hits.items():
            for _ in shoot_list:
                enemy.reducir_disparo()
                self.sonidos.reproducir_enemigo_daño()
                if enemy.disparos_restantes == 0:
                    self.sonidos.reproducir_enemigo_muere()
                    self.sumar_puntos(5)


    def colision_bala_enemiga(self):
        #Si el jugador choca con una bala enemiga
        if not self.jugador.inmortalidad and pygame.sprite.spritecollide(self.jugador, self.enemy_shoot, True):
            self.jugador.recibir_daño() 
                

    def colision_enemigo(self):
        # Colision del jugador con los enemigos
        if pygame.sprite.spritecollide(self.jugador, self.enemigos, False):
            self.jugador.recibir_daño() 
            
        
    def detectar_caida(self):
        # Detectar cuando el jugador se caiga del juego
        if self.jugador.rect.top > HEIGHT:
            self.game_over()
     

    def movimiento_camara(self, vel):
        if self.background_x > WIDTH - self.background_rect.width:
            self.background_x -= vel
            self.lava_x -= vel
            if self.jugador.rect.left != 0:
                self.jugador.rect.x -= vel

            for plataforma in self.plataformas:
                plataforma.rect.x -= vel
                plataforma.rect_left.x -= vel
                plataforma.rect_right.x -= vel

            for enemy in self.enemigos:
                enemy.rect.x -= vel
                # if enemy.tipo == 5:
                #     enemy.collision_rect.x -= vel

            for relojes in self.relojes:
                relojes.rect.x -= vel

            for monedas in self.monedas:
                monedas.rect.x -= vel

            for corazones in self.corazones:
                corazones.rect.x -= vel

            for trampas in self.trampas:
                trampas.rect.x -= vel

            for meta in self.meta:
                meta.rect.x -= vel


    def pausa(self):
        while True:
            pausa_rect = crear_rectangulo(None, 350, 100, 500, 400, BROWN, 0)
            pygame.draw.rect(self.superficie, pausa_rect["color"], pausa_rect["rect"], pausa_rect["radio"])
            mostrar_texto(self.superficie, "PAUSA", self.fuente_pausa, (515, 130), self.fuente_color, None)
            boton_continuar = crear_boton(self.superficie, 490, 220, 220, 50, CUSTOM_BOTON_COLOR, 0, 3, "CONTINUAR", self.fuente_botones)
            boton_opciones = crear_boton(self.superficie, 503, 320, 193, 50, CUSTOM_BOTON_COLOR, 0, 3, "OPCIONES", self.fuente_botones)
            boton_salir = crear_boton(self.superficie, 540, 420, 115, 50, CUSTOM_BOTON_COLOR, 0, 3, "SALIR", self.fuente_botones)
            pygame.display.flip() 

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminar()
                    
                if event.type == MOUSEBUTTONDOWN:
                    if boton_continuar["rect"].collidepoint(event.pos):
                        return 
                    if boton_opciones["rect"].collidepoint(event.pos):
                        self.pausa_opciones()
                    if boton_salir["rect"].collidepoint(event.pos):
                        self.reiniciar_stats()
                        self.menu_principal()


    def pausa_opciones(self):
        while True:
            pausa_rect = crear_rectangulo(None, 350, 100, 500, 400, BROWN, 0)
            pygame.draw.rect(self.superficie, pausa_rect["color"], pausa_rect["rect"], pausa_rect["radio"])
            mostrar_texto(self.superficie, "PAUSA", self.fuente_pausa, (515, 130), self.fuente_color, None)
            boton_sonido_dct = crear_boton(self.superficie, 486, 220, 228, 35, CUSTOM_BOTON_COLOR_2, 0, 3, "DESACTIVAR SFX", self.fuente)
            boton_sonido_act = crear_boton(self.superficie, 513, 275, 173, 35, CUSTOM_BOTON_COLOR, 0, 3, "ACTIVAR SFX", self.fuente)
            boton_musica_dct = crear_boton(self.superficie, 462, 330, 276, 35, CUSTOM_BOTON_COLOR_2, 0, 3, "DESACTIVAR MUSICA", self.fuente)
            boton_musica_act = crear_boton(self.superficie, 489, 390, 222, 35, CUSTOM_BOTON_COLOR, 0, 3, "ACTIVAR MUSICA", self.fuente)
            boton_retroceder = crear_boton(self.superficie, 512, 450, 176, 35, CUSTOM_BOTON_COLOR_2, 0, 3, "RETROCEDER", self.fuente)
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
                        if self.nivel_indice != 3:
                            self.sonidos.activar_musica()
                        else:
                             self.sonidos.activar_musica_boss()
                    elif boton_retroceder["rect"].collidepoint(event.pos):
                        return
                    
                    
    def tiempo(self):
        if self.tiempo_inicial >= 0:
            self.tiempo_inicial -= 0.02
        if self.tiempo_inicial <= 0:
            self.game_over()
        mostrar_texto(self.superficie, f"Tiempo: {int(self.tiempo_inicial)}", self.fuente, (30, 115), self.fuente_color, None)


    def draw(self):
        self.superficie.blit(self.background, (self.background_x, self.background_y))
        self.all_sprites.draw(self.superficie)
        self.superficie.blit(self.lava, (self.lava_x, self.lava_y))
        self.tiempo()

        # # Dibujar los rectángulos left y right de cada plataforma

        # for plataforma in self.plataformas:
        #     pygame.draw.rect(self.superficie, RED, plataforma.rect_left)
        #     pygame.draw.rect(self.superficie, GREEN, plataforma.rect_right)
        
    
    def update(self):
        self.all_sprites.update()
        self.draw()
        self.colision_meta()
        self.colision_trampas()
        self.colision_corazones()
        self.colision_relojes()
        self.colision_monedas()
        self.colision_jugador_plataforma()
        self.colision_enemigo_plataforma()
        self.colision_bala()
        self.colision_enemigo()
        self.colision_bala_enemiga()
        self.detectar_caida()
        self.movimiento_boss()

        if self.nivel_indice != 3:
            self.movimiento_camara(vel=2)
        else:
            self.detectar_boss_muerto()        