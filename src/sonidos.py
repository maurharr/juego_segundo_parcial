import pygame

class Sonidos:

    # -----------------------------------------------------


    def __init__(self):
        pygame.mixer.init()

        self.volumen = 0.5
        self.sonido_activado = True  

        # Efectos de sonidos del jugador
        self.jugador_lastimado = pygame.mixer.Sound("./src/assets/sounds/player_damage.mp3")
        self.jugador_get_reloj = pygame.mixer.Sound("./src/assets/sounds/time_left.mp3")
        self.jugador_get_monedas = pygame.mixer.Sound("./src/assets/sounds/get_coins.mp3")
        self.jugador_get_corazones = pygame.mixer.Sound("./src/assets/sounds/heal.mp3")

        # Efectos de sonidos de enemigo
        self.enemigo_muere = pygame.mixer.Sound("./src/assets/sounds/enemy_kill.mp3")
        self.enemigo_daño = pygame.mixer.Sound("./src/assets/sounds/enemy_damage.mp3") 

        # Efectos de sonidos independientes
        self.salto = pygame.mixer.Sound("./src/assets/sounds/jump.mp3") 
        self.disparo = pygame.mixer.Sound("./src/assets/sounds/energy_ball.mp3")

    # -----------------------------------------------------


    # Metodos de sonidos del Jugador 

    def reproducir_jugador_lastimado(self):    
        if self.sonido_activado:       
            self.jugador_lastimado.set_volume(self.volumen)
            self.jugador_lastimado.play()

    def reproducir_jugador_get_reloj(self):   
        if self.sonido_activado:     
            self.jugador_get_reloj.set_volume(self.volumen)
            self.jugador_get_reloj.play()

    def reproducir_jugador_get_monedas(self):   
        if self.sonido_activado:     
            self.jugador_get_monedas.set_volume(self.volumen)
            self.jugador_get_monedas.play()

    def reproducir_jugador_get_corazones(self):   
        if self.sonido_activado:     
            self.jugador_get_corazones.set_volume(self.volumen)
            self.jugador_get_corazones.play()

    #  Metodos de sonidos del Enemigo 

    def reproducir_enemigo_muere(self): 
        if self.sonido_activado:
            self.enemigo_muere.set_volume(self.volumen)
            self.enemigo_muere.play()

    def reproducir_enemigo_daño(self): 
        if self.sonido_activado:
            self.enemigo_daño.set_volume(self.volumen)
            self.enemigo_daño.play()

    #  Metodos de sonidos independientes 

    def reproducir_salto(self):       
        if self.sonido_activado:
            self.salto.set_volume(self.volumen)
            self.salto.play()

    def reproducir_disparo(self):
        if self.sonido_activado:
            self.disparo.set_volume(self.volumen)
            self.disparo.play()


    # -----------------------------------------------------
    def toggle_sonido(self):
        self.sonido_activado = not self.sonido_activado

    def esta_sonido_activado(self):
        return self.sonido_activado

    def apagar_sonido(self):
        self.sonido_activado = False

    def encender_sonido(self):
        self.sonido_activado = True
        self.reproducir_disparo()

    def apagar_musica(self):
        pygame.mixer.music.stop()

    def activar_musica(self):
        pygame.mixer.music.load("./src/assets/sounds/background.mp3")  
        pygame.mixer.music.play(-1)

    def activar_musica_menu(self):
        pygame.mixer.music.load("./src/assets/sounds/background_menu.mp3") 
        pygame.mixer.music.play(-1)

    def activar_musica_boss(self):
        pygame.mixer.music.load("./src/assets/sounds/boss.mp3") 
        pygame.mixer.music.play(-1)
    # -----------------------------------------------------
