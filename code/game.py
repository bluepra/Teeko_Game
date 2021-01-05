import pygame
from pygame import mixer
import sys
import random
from teeko2_player import Teeko2Player
from classes import *
from assets import *

pygame.init()

# Constants
SCREEN_WIDTH = 530
SCREEN_HEIGHT = 580

# Setup screen, clock and fonts
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
menu_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
tutorial_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
win_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Teeko")
pygame.display.set_icon(hexagon)
clock = pygame.time.Clock()


# Create the Board
board = Board()
text_bar = TextBar('click on a square', Board.PADDING,
                   SCREEN_WIDTH - Board.PADDING, SCREEN_WIDTH / 2, 45, BLACK)


def get_cell_coord(pos):
    # Given a position coordinate, this function returns the cell coordinate
    return (pos[1] // (Cell.CELL_LENGTH + Board.PADDING),
            pos[0] // (Cell.CELL_LENGTH + Board.PADDING))





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
    # Reset board
    board.reset()
    text_bar.reset()
    
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
                board.place_piece(ai_move[0], AIColor)
                piece_count += 1
                userTurn = True
        # Draw board at end of each loop
        draw_board()
        clock.tick(60)
        #print('running drop')


def userDropHandler(event, ai, userColor):
    # Check if left click, then place piece
    if pygame.mouse.get_pressed()[0]:
        cur_cell = getMouseCell()
        cell_coord = cur_cell.cell_coord
        if(cur_cell.has_piece()):
            return False
        board.place_piece(cell_coord, userColor)
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
        clock.tick(60)
        #print('running move')
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
    


def win_screen(winner):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        text_bar.update_text(winner)
        draw_board()
        #print('running win')
        
        pygame.display.update()
        clock.tick(60)


def run_tutorial():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # print('running tutorial')
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
            if checkLeftClick(event):
                pos = pygame.mouse.get_pos()
                clicked_button = check_buttons(buttons, pos)
                if clicked_button is not None:
                    if(clicked_button.text == 'START'):
                        run_game()
                    if(clicked_button.text == 'TUTORIAL'):
                        run_tutorial()
                    if(clicked_button.text == 'EXIT'):
                        sys.exit()
        #print('running menu')
        screen.fill(BLACK)
        menu_surface.blit(hexagon, (12, 12))
        teeko_text = teeko_font.render('TEEKO', True, RED)
        menu_surface.blit(teeko_text, (120, 120))
        

        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.update(mouse_pos)
            button.draw(menu_surface)

        

        screen.blit(menu_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)


def quitHandler():
    pygame.quit()
    sys.exit()


run_menu()
quitHandler()
