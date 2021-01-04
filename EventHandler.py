# Ryan Almizyed
# Prannav Arora
# Teeko Game

import pygame

#Main event handler loop
def handleEvents():
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            quitHandler()
        elif event.type is pygame.MOUSEBUTTONDOWN:
            clickHandler()

#Individual event handlers
def quitHandler(event):
    pygame.quit()


def clickHandler(event):
    pos = pygame.mouse.get_pos()
