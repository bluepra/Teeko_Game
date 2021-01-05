import pygame
from pygame import mixer
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
pygame.font.init()
myfont = pygame.font.Font('../assets/CubicCoreMono.ttf', 40)
hover_font = pygame.font.Font('../assets/CubicCoreMono.ttf', 50)
teeko_font = pygame.font.Font('../assets/CubicCoreMono.ttf', 150)
text_bar_font = pygame.font.SysFont('segoeuiblack', 25)

# Images
red = pygame.image.load('../assets/red_piece.png')
black = pygame.image.load('../assets/black_piece.png')
hexagon = pygame.image.load('../assets/hexagon.png')


# Sounds
piece_down = pygame.mixer.Sound('../assets/piece_down.mp3')
music = pygame.mixer.music.load('../assets/music.mp3')
music_volume = 0.5
pygame.mixer.music.set_volume(music_volume)
mixer.music.play(-1)