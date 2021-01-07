import pygame, random, sys
from teeko_bot import TeekoBot
from classes import *

class Game:
    # Constants - dont change
    SCREEN_WIDTH = 530
    SCREEN_HEIGHT = 580

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
        self.game_surface = pygame.Surface((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
        self.menu_surface = pygame.Surface((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
        self.tutorial_surface = pygame.Surface((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
        #self.win_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.settings_surface = pygame.Surface((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))

        pygame.display.set_caption("Teeko")
        pygame.display.set_icon(hexagon)
        self.clock = pygame.time.Clock()

        # Create the Board and TextBar for game
        self.board = Board()
        self.text_bar = TextBar('', Board.PADDING,
                   Game.SCREEN_WIDTH, Game.SCREEN_WIDTH - 75, 45, BLACK, WHITE)

        # Game music
        self.music_on = True
        self.sounds_on = True
        pygame.mixer.music.set_volume(.5)
        pygame.mixer.music.play(-1)

        #0 -> menu, 1 -> game, 2 -> tutorial, 3 -> settings, -1 -> exit
        self.states = {'menu': 0, 'game': 1, 'tutorial': 2, 'settings': 3, 'exit': -1}
        self.state = self.states['menu']

        # Difficulty of AI bot -> 1 is easy, 2 is medium, 3 is hard
        self.level = 1

    def run(self):
        while(self.state >= 0):
            # Menu
            if self.state == self.states['menu']:
                self.run_menu()

            # Game
            elif self.state == self.states['game']:
                self.run_game()

            # Tutorial
            elif self.state == self.states['tutorial']:
                self.run_tutorial()

            # Settings
            elif self.state == self.states['settings']:
                self.run_settings()

            # Exit
            else:
                self.quitHandler()

    def run_game(self):
        # Create the AI object and colors dictionary
        ai = TeekoBot(random.choice(['b', 'r']), self.level)
        colors = self.generateColors(ai)

        # Randomly choose whether user or Ai goes first
        userTurn = ai.my_piece == ai.pieces[0]

        # Run drop phase
        self.drop_phase(ai, colors, userTurn)

        # Run move phase
        winner = self.move_phase(ai, colors, userTurn)

        # Display winner
        self.win_screen(winner)
        
    def drop_phase(self, ai, colors, userTurn):
        userColor = colors['player']
        AIColor = colors['ai']

        # Loop until all pieces are placed or someone wins
        while self.board.num_pieces < 8 and ai.game_value(ai.board) == 0:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    self.quitHandler()
                # User's turn
                if(userTurn):
                    # Wait for user to left-click on a cell
                    self.text_bar.update_text('Your turn, click a cell')
                    self.draw_board()
                    if self.checkLeftClick(event):
                        if(self.userDropHandler(event, ai, userColor)):
                            userTurn = False
                # AI's turn
                else:
                    self.text_bar.update_text('AI\'s turn')
                    self.draw_board()
                    ai_move = ai.make_move(ai.board)
                    ai.place_piece(ai_move, ai.my_piece)
                    self.board.place_piece(ai_move[0], AIColor)
                    userTurn = True

            # Draw board at end of each loop
            self.draw_board()
            self.clock.tick(60)
            #print('running drop')

    def userDropHandler(self, event, ai, userColor):
        cell = self.get_cell_from_coord(self.cell_coord_from_mouse())
        cell_coord = cell.cell_coord
        if(cell.has_piece()):
            return False

        self.board.place_piece(cell_coord, userColor)
        ai.opponent_move([cell_coord])
        return True            

    def move_phase(self, ai, colors, userTurn):
        userColor = colors['player']
        AIColor = colors['ai']

        user_source = None
        user_desti = None

        # Loop while game is still undecided
        while ai.game_value(ai.board) == 0:
            # Get all current events
            for event in pygame.event.get():
                # Quit event
                if event.type is pygame.QUIT:
                    self.quitHandler()
                # User's turn
                if(userTurn):
                    if user_source is None:
                        self.text_bar.update_text('Your turn, choose one piece to move')
                        self.draw_board()
                    # Check if user clicked on a rectangle
                    if self.checkLeftClick(event):
                        # Get the cell that has been clicked
                        cell = self.get_cell_from_coord(self.cell_coord_from_mouse())
                        # If the cell has a piece, select source cell
                        if(cell.has_piece() and cell.color is userColor):
                            user_source = cell
                            self.text_bar.update_text('Click adjacent empty cell')
                            self.draw_board()
                        # If the cell is empty, select a destination cell
                        if(not cell.has_piece() and user_source is not None):
                            user_desti = cell
                    # User has selected a source and destination,
                    if user_source is not None and user_desti is not None:
                        # try to move the piece
                        if self.move_piece(user_source, user_desti):
                            move_str = 'Moved piece from' + str(user_source.cell_coord) + ' to ' + str(user_desti.cell_coord)
                            self.text_bar.update_text(move_str)
                            self.draw_board()
                            ai.opponent_move([user_desti.cell_coord, user_source.cell_coord])
                            userTurn = False
                        # failed to move the piece, reset selection
                        else:
                            self.text_bar.update_text('Try again')
                            self.draw_board()
                            user_source = None
                            user_desti = None
                # AI's turn
                else:
                    self.text_bar.update_text('AI\'s turn')
                    self.draw_board()
                    ai_move = ai.make_move(ai.board)
                    ai.place_piece(ai_move, ai.my_piece)
                    AI_source = self.get_cell_from_coord(ai_move[1])
                    AI_desti = self.get_cell_from_coord(ai_move[0])
                    self.move_piece(AI_source, AI_desti)
                    userTurn = True

            # Draw board at end of each loop
            self.draw_board()
            # self.clock.tick(60)
            
        if ai.game_value(ai.board) == 1:
            return "AI wins!"
        else:
            return "You win!"

    def move_piece(self, sourceCell, destiCell):
        # Checking if there is a piece to move
        if(not sourceCell.has_piece()):
            return False
        # Checking if there an open cell to move to
        if(destiCell.has_piece()):
            return False
        # Checking if the two cells are adjacent
        if(not self.is_adjacent(sourceCell, destiCell)):
            return False

        # Save sourceCell's old color
        tempColor = sourceCell.color
        # No errors, moving piece
        sourceCell.put_piece(sourceCell.color)
        destiCell.put_piece(tempColor)
        # Succesfully moved the piece
        return True

    def is_adjacent(self, cell1, cell2):
        pos1 = cell1.cell_coord
        pos2 = cell2.cell_coord
        return (abs(pos1[0] - pos2[0]) <= 1) and (abs(pos1[1] - pos2[1]) <= 1)

    def generateColors(self, ai):
        colors = {}
        if(ai.my_piece == 'r'):
            colors['ai'] = red
            colors['player'] = black
        else:
            colors['ai'] = black
            colors['player'] = red
        return colors

    def cell_coord_from_mouse(self):
        pos = pygame.mouse.get_pos()
        # Given a position coordinate, this function returns the cell's coordinate
        return (pos[1] // (Cell.CELL_LENGTH + Board.PADDING),
                pos[0] // (Cell.CELL_LENGTH + Board.PADDING))

    def get_cell_from_coord(self, coord):
        # Returns a specific cell given the board coordinates of that cell
        return self.board.cells[coord[0]][coord[1]]

    def draw_board(self):
        self.board.draw(self.game_surface)
        self.text_bar.draw(self.game_surface)
        self.screen.blit(self.game_surface, (0, 0))
        pygame.display.update()
        self.clock.tick(60)

    def quitHandler(self):
        pygame.quit()
        sys.exit()

    def checkLeftClick(self, event):
        # Return True if left click detected
        return event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]

    def run_tutorial(self):
        back_to_menu = Button('BACK TO MENU', 10, Game.SCREEN_HEIGHT - 50, 235, 45, BLACK)
        buttons = [back_to_menu]

        line_height = 50
        # RULES
        rules = TextBar('Rules:', 10, 10, Game.SCREEN_WIDTH, line_height, BLACK, RED)
        line1 = TextBar('- You vs AI Bot', 10, line_height, Game.SCREEN_WIDTH, line_height, BLACK, WHITE)
        line3 = TextBar('- Place one piece at a time', 10, 2*line_height, Game.SCREEN_WIDTH, line_height, BLACK, WHITE)
        line4 = TextBar('- After 4 pieces each down,', 10, 3*line_height, Game.SCREEN_WIDTH, line_height, BLACK, WHITE)
        line5 = TextBar('  move one piece to adjacent, empty spot', 10, 4*line_height, Game.SCREEN_WIDTH, line_height, BLACK, WHITE)
        
        # Objective
        objective = TextBar('Objective:', 10, 6*line_height, Game.SCREEN_WIDTH, line_height, BLACK, RED)
        line6 = TextBar('First to get 4 pieces in a', 10, 7*line_height, Game.SCREEN_WIDTH, line_height, BLACK, WHITE)
        line7 = TextBar('horizontal, vertical, diagonal', 10, 8*line_height, Game.SCREEN_WIDTH, line_height, BLACK, WHITE)
        line8 = TextBar('or diamond shape wins!', 10, 9*line_height, Game.SCREEN_WIDTH, line_height, BLACK, WHITE)
        
        lines = [rules, line1, line3, line4, line5, objective, line6, line7, line8]
        
        while self.state == self.states['tutorial']:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = self.states['exit']
                if self.checkLeftClick(event):
                    for button in buttons:
                        #Check if a button was clicked
                        if button.check_if_clicked(mouse_pos):
                            if(button.text == 'BACK TO MENU'):
                                self.state = self.states['menu']
            
            self.screen.fill(BLACK)                 
            
            for button in buttons:
                back_to_menu.update(mouse_pos)
                back_to_menu.draw(self.tutorial_surface)

            for line in lines:
                line.draw(self.tutorial_surface)

            self.screen.blit(self.tutorial_surface, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    def run_settings(self):
        level_button = Button('TOGGLE LEVEL', 140, 200, 250, 50, BLACK)
        toggle_music = Button('TOGGLE MUSIC', 140, 250, 250, 50, BLACK)
        back_to_menu = Button('BACK TO MENU', 140, 300, 300, 50, BLACK)
        buttons = [level_button, toggle_music, back_to_menu]

        user_level = TextBar(str(self.level), 400, 200, 50, 50, BLACK, WHITE)
        music_indicator = TextBar('ON', 400, 250, 100, 50, BLACK, WHITE)

        if(not self.music_on):
            music_indicator.update_text('OFF') 
        
        words = [user_level, music_indicator]

        while self.state == self.states['settings']:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = self.states['exit']
                if self.checkLeftClick(event):
                    for button in buttons:
                        #Check if a button was clicked
                        if button.check_if_clicked(mouse_pos):
                            if(button.text == 'TOGGLE LEVEL'):
                                self.level = (self.level + 1) % 4
                                if self.level == 0:
                                    self.level += 1
                                user_level.update_text(str(self.level))
                            if(button.text == 'BACK TO MENU'):
                                self.state = self.states['menu']
                            if(button.text == 'TOGGLE MUSIC'):
                                self.music_on = not self.music_on
                                if(not self.music_on):
                                    pygame.mixer.music.pause()
                                    music_indicator.update_text('OFF') 
                                else:
                                    pygame.mixer.music.unpause()
                                    music_indicator.update_text('ON') 

            self.screen.fill(BLACK)

            for word in words:
                word.draw(self.settings_surface)

            for button in buttons:
                button.update(mouse_pos)
                button.draw(self.settings_surface)

            self.screen.blit(self.settings_surface, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    def run_menu(self):
        # Opening menu
        start = Button('START', 200, 230, 100, 40, WHITE)
        tutorial = Button('TUTORIAL', 200, 280, 150, 40, WHITE)
        settings = Button('SETTINGS', 200, 330, 150, 40, WHITE)
        exit = Button('EXIT', 200, 380, 80, 40, WHITE)
        buttons = [start, tutorial, settings, exit]

        while self.state == 0:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = self.states['exit']
                if self.checkLeftClick(event):
                    for button in buttons:
                        #Check if a button was clicked
                        if button.check_if_clicked(mouse_pos):
                            if(button.text == 'START'):
                                self.state = self.states['game']
                            if(button.text == 'TUTORIAL'):
                                self.state = self.states['tutorial']
                            if(button.text == 'SETTINGS'):
                                self.state = self.states['settings']
                            if(button.text == 'EXIT'):
                                self.state = self.states['exit']

            # Draw text and hexagon on screen
            self.screen.fill(BLACK)
            self.menu_surface.blit(hexagon, (12, 12))
            teeko_text = teeko_font.render('TEEKO', True, RED)
            self.menu_surface.blit(teeko_text, (120, 120))

            # Draw buttons
            for button in buttons:
                button.update(mouse_pos)
                button.draw(self.menu_surface)

            self.screen.blit(self.menu_surface, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    def win_screen(self, winner):
        while self.state == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = -1
            
            self.text_bar.update_text(winner)
            self.draw_board()
            
            pygame.display.update()
            self.clock.tick(60)

game = Game()
game.run()

