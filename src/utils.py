import pygame
from config import *
from pygame.locals import *



def terminar():
    """
    Esta función se encarga de cerrar la aplicación del juego.
    """
    pygame.quit()
    exit()

                                
def crear_rectangulo(imagen=None, left:float=100, top:float=100, ancho:float=80, largo:float=50, color=BLUE, borde:float=3, radio:float=0) -> dict:
    """
    Crea un rectángulo con opciones personalizables en un diccionario.

    Args:
        imagen (Surface, opcional): La imagen a mostrar en el rectángulo. Valor por defecto: None.
        left (float): La coordenada x del extremo izquierdo del rectángulo. Valor por defecto: 100.
        top (float): La coordenada y del extremo superior del rectángulo. Valor por defecto: 100.
        ancho (float): El ancho del rectángulo. Valor por defecto: 80.
        largo (float): El largo del rectángulo. Valor por defecto: 50.
        color (color): El color del rectángulo si no se proporciona una imagen. Valor por defecto: blue.
        borde (float): El ancho del borde del rectángulo. Valor por defecto: 3.
        radio (float): El radio de las esquinas del rectángulo. Valor por defecto: 0.

    Returns:
        dict: Un diccionario que contiene la información del rectángulo, incluyendo su imagen, su rectángulo, su color, el ancho de su borde y su radio de las esquinas.
    """
    rect = pygame.Rect(left, top, ancho, largo)
    if imagen:
        imagen = pygame.transform.scale(imagen, (ancho, largo))
    return {
        "imagen":imagen,
        "rect":rect,
        "color":color,
        "borde":borde,
        "radio":radio
        }
       
def mostrar_texto(superficie, texto, fuente, coordenadas, color_fuente=WHITE, color_fondo=BLACK):
    """
    Renderiza y muestra texto en una superficie.

    Args:
        superficie (Surface): La superficie en la que se mostrará el texto.
        texto (str): El texto que se va a mostrar.
        fuente (Font): La fuente utilizada para el texto.
        coordenadas (tupla): Las coordenadas (x, y) donde se mostrará el texto.
        color_fuente (color): El color del texto. Valor por defecto: white.
        color_fondo (color): El color del fondo del texto. Valor por defecto: black.
    """
    texto_renderizado = fuente.render(texto, True, color_fuente, color_fondo) #Convierte el texto en una imagen/superficie que pueda ser mostrada en una screen.
    texto_rectangulo = texto_renderizado.get_rect(topleft=coordenadas)
    superficie.blit(texto_renderizado, texto_rectangulo)
    


def crear_boton(superficie, left: float = 100, top: float = 100, ancho: float = 80, largo: float = 50, color=BLUE, borde: float = 3, radio: float = 0, texto=None, fuente=None, color_fuente=WHITE):
    rect = pygame.Rect(left, top, ancho, largo)
    dict = {
        "rect": rect,
        "color": color,
        "borde": borde,
        "radio": radio,
        "texto": texto
    }
    pygame.draw.rect(superficie, dict["color"], dict["rect"], dict["borde"], dict["radio"])
    texto = mostrar_texto(superficie, texto, fuente, (dict["rect"].topleft), color_fuente, None)
    return dict  
