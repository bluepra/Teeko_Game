# Ryan Almizyed
# Prannav Arora
# Teeko Game

import pygame


def eventHandlers(event):
    if event.type is pygame.QUIT:
        quitHandler()
    elif event.type is pygame.MOUSEBUTTONDOWN:
        clickHandler()


def quitHandler(event):
    pygame.quit()


def clickHandler(event):
    pos = pygame.mouse.get_pos()
