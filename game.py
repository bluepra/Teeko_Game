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
win_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
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

# Create the Board
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


def move_piece(sourceCell, destiCell):
    # Checking if there is a piece to move
    if(not sourceCell.has_piece()):
        return False
    # Checking if there an open cell to move to
    if(destiCell.has_piece()):
        return False
    # Checking if the two cells are adjacent
    if(not isAdjacent(sourceCell, destiCell)):
        return False
    # Save sourceCell's old color
    tempColor = sourceCell.color
    # No errors, moving piece
    sourceCell.put_piece(sourceCell.color)
    destiCell.put_piece(tempColor)
    # Succesfully moved the piece
    return True


def isAdjacent(cell1, cell2):
    pos1 = cell1.cell_coord
    pos2 = cell2.cell_coord
    return (abs(pos1[0] - pos2[0]) <= 1) and (abs(pos1[1] - pos2[1]) <= 1)


def check_buttons(buttons, click_pos):
    for button in buttons:
        if(click_pos[0] >= button.x and click_pos[0] <= (button.x + button.width)):
            if(click_pos[1] >= button.y and click_pos[1] <= (button.y + button.height)):
                return button
            else:
                continue


def generateColors():
    # Randomly choose user's piece color
    userColor = random.choice([red, black])
    # Choose the AI's color to be opposite of user's color
    AIColor = None
    if(userColor is red):
        AIColor = black
    else:
        AIColor = red
    colors = (userColor, AIColor)
    return colors


def run_game():
    # Randomly choose whether user or Ai goes first
    userTurn = random.choice([True, False])
    # Randomly generate user & AI piece colors
    colors = generateColors()

    # Create the AI object
    ai = Teeko2Player()

    # Run drop phase
    drop_phase(ai, userTurn, colors)
    # Run move phase
    winner = move_phase(ai, userTurn, colors)

    # Display winner
    win_screen(winner)
    


def drop_phase(ai, userTurn, colors):
    piece_count = 0
    userColor = colors[0]
    AIColor = colors[1]

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
        cur_cell = getMouseCell()
        cell_coord = cur_cell.cell_coord
        if(cur_cell.has_piece()):
            return False
        place_piece(cell_coord, userColor)
        ai.opponent_move([cell_coord])
    return True


def move_phase(ai, userTurn, colors):
    userColor = colors[0]
    AIColor = colors[1]

    user_source = None
    user_desti = None

    # Loop while game is still undecided
    while ai.game_value(ai.board) == 0:
        # Get all current events
        for event in pygame.event.get():
            # Quit event
            if event.type is pygame.QUIT:
                quitHandler()
            # User's turn
            if(userTurn):
                # Check if user clicked on a rectangle
                if checkLeftClick(event):
                    # Get the cell that has been clicked
                    cell = getMouseCell()
                    # If the cell has a piece, select source cell
                    if(cell.has_piece and cell.color is userColor):
                        user_source = cell
                    # If the cell is empty, select a destination cell
                    if(not cell.has_piece() and user_source is not None):
                        user_desti = cell
                # User has selected a source and destination,
                if user_source is not None and user_desti is not None:
                    # try to move the piece
                    if move_piece(user_source, user_desti):
                        ai.opponent_move(
                            [user_desti.cell_coord, user_source.cell_coord])
                        userTurn = False
                    # failed to move the piece, reset selection
                    else:
                        user_source = None
                        user_desti = None
            # AI's turn
            else:
                ai_move = ai.make_move(ai.board)
                ai.place_piece(ai_move, ai.my_piece)
                AISource = getCellFromCoord(ai_move[1])
                AIDesti = getCellFromCoord(ai_move[0])
                move_piece(AISource, AIDesti)
                userTurn = True
        # Draw board at end of each loop
        draw_board()
    if ai.game_value(ai.board) == 1:
        return "AI wins!"
    else:
        return "You win!"


def checkLeftClick(event):
    return event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]


def getMouseCellCoord():
    pos = pygame.mouse.get_pos()
    return get_cell_coord(pos)


def getMouseCell():
    coord = getMouseCellCoord()
    return getCellFromCoord(coord)


def getCellFromCoord(coord):
    return board.cells[coord[0]][coord[1]]


def draw_board():
    board.draw(game_surface)
    text_bar.draw(game_surface)
    screen.blit(game_surface, (0, 0))
    pygame.display.update()
    clock.tick(60)


def win_screen(winner):
    # play_again = Button('PLAY AGAIN', 200, 250, 300, 60, BLACK)
    # exit = Button('EXIT', 200, 350, 300, 60, BLACK)
    # buttons = [play_again, exit]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if pygame.mouse.get_pressed()[0]:
            #         pos = pygame.mouse.get_pos()
            #         clicked_button = check_buttons(buttons, pos)
            #         if clicked_button is not None:
            #             if(clicked_button.text == 'PLAY AGAIN'):
            #             	board.reset()
            #             if(clicked_button.text == 'EXIT'):
            #            	sys.exit()
        
        # mouse_pos = pygame.mouse.get_pos()
        # for button in buttons:
        # 	button.update(mouse_pos)
        # 	button.draw(win_surface)

       	# winner_text = teeko_font.render(winner, True, RED)
        # win_surface.blit(winner_text, (50, 120))
        
       	text_bar.update_text(winner)
       	draw_board()
        
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


def run_menu():
	# Opening menu
    start = Button('START', 200, 250, 100, 40, WHITE)
    tutorial = Button('TUTORIAL', 200, 300, 100, 40, WHITE)
    exit = Button('EXIT', 200, 350, 100, 40, WHITE)
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
                        if(clicked_button.text == 'START'):
                            run_game()
                        if(clicked_button.text == 'TUTORIAL'):
                            run_tutorial()
                        if(clicked_button.text == 'EXIT'):
                            sys.exit()

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


def quitHandler():
    sys.exit()


run_menu()
pygame.quit()
