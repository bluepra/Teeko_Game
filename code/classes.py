import pygame
import random
import sys
from assets import *
from teeko_bot import TeekoBot

class Cell:
    CELL_LENGTH = 100

    def __init__(self, x, y, cell_coord):
        # print('creating cell')
        self.x = x
        self.y = y
        self.color = None
        self.cell_coord = cell_coord

    def __str__(self):
        return str(self.cell_coord)

    def has_piece(self):
        return self.color is not None

    def put_piece(self, pieceColor):
        if self.has_piece():
            piece_down.play()
            self.color = None
        else:
            # text_bar.update_text(str(self.cell_coord))
            piece_down.play()
            self.color = pieceColor

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, (self.x, self.y,
                                          Cell.CELL_LENGTH, Cell.CELL_LENGTH))
        if self.has_piece():
            surface.blit(self.color, (self.x + 15, self.y + 15))

class Board:
    PADDING = 5
    
    def __init__(self):
        self.num_pieces = 0
        self.cells = []
        for row in range(5):
            row_of_cells = []
            for col in range(5):
                x = Board.PADDING + (Cell.CELL_LENGTH + Board.PADDING) * col
                y = Board.PADDING + (Cell.CELL_LENGTH + Board.PADDING) * row
                new_cell = Cell(x, y, (row, col))
                row_of_cells.append(new_cell)
            self.cells.append(row_of_cells)

    # Draws the 5x5 game board onto the screen
    def draw(self, surface):
        for row in range(5):
            for col in range(5):
                curr_cell = self.cells[row][col]
                curr_cell.draw(surface)

    def place_piece(self, cell_coord, color):
        # Change a specific cell's color
        y = cell_coord[0]
        x = cell_coord[1]
        self.cells[y][x].put_piece(color)
        self.num_pieces += 1

    def reset(self):
        temp_cells = []
        for row in range(5):
            row_of_cells = []
            for col in range(5):
                x = Board.PADDING + (Cell.CELL_LENGTH + Board.PADDING) * col
                y = Board.PADDING + (Cell.CELL_LENGTH + Board.PADDING) * row
                new_cell = Cell(x, y, (row, col))
                row_of_cells.append(new_cell)
            temp_cells.append(row_of_cells)
        self.cells = temp_cells
        self.num_pieces = 0

class TextBar:
    def __init__(self, text, x, y, width, height, color):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(
            surface, self.color, (self.x, self.y, self.width, self.height))
        word = text_bar_font.render(self.text, True, WHITE)
        surface.blit(word, (self.x, self.y + 10))

    def update_text(self, new_text):
        self.text = new_text

    def reset(self):
        self.text = 'click on a square'

class Button:
    def __init__(self, text, x, y, width, height, color):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = myfont
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(
            surface, self.color, (self.x, self.y, self.width, self.height))
        word = self.font.render(self.text, True, (255, 0, 0))
        surface.blit(word, (self.x, self.y + 10))

    def update(self, mouse_pos):
        if mouse_pos[0] >= self.x and mouse_pos[0] <= (self.x + self.width):
            if mouse_pos[1] >= self.y and mouse_pos[1] <= (self.y + self.height):
                self.font = hover_font
            else:
                self.font = myfont
        else:
            self.font = myfont

    def check_if_clicked(self, mouse_pos):
        if mouse_pos[0] >= self.x and mouse_pos[0] <= (self.x + self.width):
            if mouse_pos[1] >= self.y and mouse_pos[1] <= (self.y + self.height):
                return True
            else:
                return False
        else:
            return False