import pygame
from pygame import mixer
import sys
import random
from teeko2_player import Teeko2Player

pygame.init()

# Constants
SCREEN_WIDTH = 530
SCREEN_HEIGHT = 580

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Setup screen, clock and fonts
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
menu_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
tutorial_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
tutorial_surface.fill(BLUE)
pygame.display.set_caption("Teeko")
clock = pygame.time.Clock()

# Fonts
pygame.font.init()
myfont = pygame.font.Font('CubicCoreMono.ttf', 40)
hover_font = pygame.font.Font('CubicCoreMono.ttf', 50)
teeko_font = pygame.font.Font('CubicCoreMono.ttf', 150)
text_bar_font = pygame.font.SysFont('segoeuiblack', 25)

# Images
red = pygame.image.load('red_piece.png')
black = pygame.image.load('black_piece.png')
hexagon = pygame.image.load('hexagon.png')
pygame.display.set_icon(hexagon)

# Sounds
piece_down = mixer.Sound('piece_down.mp3')
music = mixer.music.load('music.mp3')
mixer.music.play(-1)


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
            text_bar.update_text(str(self.cell_coord))
            piece_down.play()
            self.color = pieceColor

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, (self.x, self.y,
                                          Cell.CELL_LENGTH, Cell.CELL_LENGTH))
        if self.has_piece():
            surface.blit(self.color, (self.x + 15, self.y + 15))


class Board:
    PADDING = 5
    cells = []

    def __init__(self):
        # print('creating board')
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


class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = myfont

    def draw(self, surface):
        pygame.draw.rect(
            surface, WHITE, (self.x, self.y, self.width, self.height))
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

    def clicked(self):
        if(self.text == 'START'):
            run_game()
        if(self.text == 'TUTORIAL'):
            run_tutorial()
        if(self.text == 'EXIT'):
            sys.exit()


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


board = Board()
text_bar = TextBar('click on a square', Board.PADDING,
                   SCREEN_WIDTH - Board.PADDING, SCREEN_WIDTH / 2, 45, BLACK)


def get_cell_coord(pos):
    # Given a position coordinate, this function returns the cell coordinate
    return (pos[1] // (Cell.CELL_LENGTH + Board.PADDING),
            pos[0] // (Cell.CELL_LENGTH + Board.PADDING))


def place_piece(cell_coord, color):
    # Change a specific cell's color
    y = cell_coord[0]
    x = cell_coord[1]
    board.cells[y][x].put_piece(color)


def move_piece(source, desti):
    # Get the cells from the board
    sourceCell = board.cells[source[0]][source[1]]
    destiCell = board.cells[desti[0]][desti[1]]
    # Checking if there is a piece to move
    if(not sourceCell.has_piece()):
        return False
    # Checking if there an open cell to move to
    if(destiCell.has_piece()):
        return False
    # Checking if the two cells are adjacent
    if(not isAdjacent(source, desti)):
        return False
    # No erros, moving piece
    sourceCell.put_piece()
    destiCell.put_piece()
    # Succesfully moved the piece
    return True


def isAdjacent(pos1, pos2):
    return (abs(pos1[0] - pos2[0]) <= 1) and (abs(pos1[1] - pos2[1]) <= 1)


def check_buttons(buttons, click_pos):
    for button in buttons:
        if(click_pos[0] >= button.x and click_pos[0] <= (button.x + button.width)):
            if(click_pos[1] >= button.y and click_pos[1] <= (button.y + button.height)):
                return button
            else:
                continue

# Run Game


def run_game():
    running = True

    # Create the AI object
    ai = Teeko2Player()

    drop_phase(ai)
    move_phase(ai)

    '''while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Left click
                if pygame.mouse.get_pressed()[0]:
                    # USER TURN
                    # User places a piece
                    pos = pygame.mouse.get_pos()
                    cell_coord = get_cell_coord(pos)
                    place_piece(cell_coord)
'''


def drop_phase(ai):
    piece_count = 0
    # Randomly choose whether user or Ai goes first
    userTurn = random.choice([True, False])
    # Randomly choose user's piece color
    userColor = random.choice([red, black])
    # Choose the AI's color to be opposite of user's color
    AIColor = None
    if(userColor is red):
        AIColor = black
    else:
        AIColor = red

    # Loop until all pieces are placed
    while piece_count < 8:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                quitHandler()
            # User's turn
            if(userTurn):
                # Wait for user to click on rectangle
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if(userDropHandler(event, ai, userColor)):
                        piece_count += 1
                        userTurn = False
            # AI's turn
            else:
                ai_move = ai.make_move(ai.board)
                ai.place_piece(ai_move, ai.my_piece)
                place_piece(ai_move[0], AIColor)
                piece_count += 1
                userTurn = True
        # Draw board at end of each loop
        draw_board()


def userDropHandler(event, ai, userColor):
    # Check if left click, then place piece
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        cell_coord = get_cell_coord(pos)
        cur_cell = board.cells[cell_coord[0]][cell_coord[1]]
        if(cur_cell.has_piece()):
            return False
        place_piece(cell_coord, userColor)
        ai.opponent_move([cell_coord])
    return True


def move_phase(ai):

    # Opening menu
    return


def draw_board():
    board.draw(game_surface)
    text_bar.draw(game_surface)
    screen.blit(game_surface, (0, 0))
    pygame.display.update()
    clock.tick(60)


def run_tutorial():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(tutorial_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)

# Opening menu


def run_menu():
    start = Button('START', 200, 250, 100, 40)
    tutorial = Button('TUTORIAL', 200, 300, 100, 40)
    exit = Button('EXIT', 200, 350, 100, 40)
    buttons = [start, tutorial, exit]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    clicked_button = check_buttons(buttons, pos)
                    if clicked_button is not None:
                        clicked_button.clicked()

        menu_surface.blit(hexagon, (12, 12))

        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.update(mouse_pos)
            button.draw(menu_surface)

        teeko_text = teeko_font.render('TEEKO', True, RED)
        menu_surface.blit(teeko_text, (120, 120))

        screen.blit(menu_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)


# Main event handler loop
def handleEvents():
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            quitHandler()
        elif event.type is pygame.MOUSEBUTTONDOWN:
            clickHandler()

# Individual event handlers


def quitHandler():
    sys.exit()


def clickHandler(event):
    pos = pygame.mouse.get_pos()
    clickedButton = check_buttons(buttons, pos)
    if clickedButton is not None:
        clickedButton.clicked()


run_menu()
pygame.quit()
