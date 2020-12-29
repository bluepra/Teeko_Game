import pygame, sys
from teeko2_player import Teeko2Player

pygame.init()

#Constants
SCREEN_WIDTH = 530
SCREEN_HEIGHT = 580

#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

#Setup screen, clock and fonts
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
menu_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Teeko")
clock = pygame.time.Clock()
pygame.font.init()
myfont = pygame.font.Font('techno_hideo.ttf', 30)
teeko_font = pygame.font.Font('techno_hideo.ttf', 90)

class Cell:
	CELL_LENGTH = 100
	def __init__(self, x, y, color, cell_coord):
		#print('creating cell')
		self.x = x
		self.y = y
		self.color = color
		self.cell_coord = cell_coord


	def __str__(self):
		return str(self.cell_coord)

	def change_color(self, new_color):
		print(self.cell_coord)
		self.color = new_color

	def draw(self, surface):
		pygame.draw.rect(surface, self.color, (self.x, self.y, Cell.CELL_LENGTH, Cell.CELL_LENGTH))

class Board:
	PADDING = 5
	cells = []
	def __init__(self):
		#print('creating board')
		for row in range(5):
			row_of_cells = []
			for col in range(5):
				x = Board.PADDING + (Cell.CELL_LENGTH + Board.PADDING) * col
				y = Board.PADDING + (Cell.CELL_LENGTH + Board.PADDING) * row
				new_cell = Cell(x, y, WHITE, (row, col))
				row_of_cells.append(new_cell)
			self.cells.append(row_of_cells)

	# Draws the 5x5 game board onto the screen
	def draw(self, surface):
		for row in range(5):
			for col in range(5):
				curr_cell = self.cells[row][col]
				curr_cell.draw(surface)

class Button:
	def __init__(self, text, x, y, width, height, color):
		self.text = text
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color

	def draw(self, surface):
		pygame.draw.rect(surface, BLACK,(self.x, self.y, self.width, self.height))
		word = myfont.render(self.text, True, (255,0,0))
		surface.blit(word, (self.x, self.y + 10))

	def clicked(self):
		if(self.text == 'START'):
			run_game()
		if(self.text == 'EXIT'):
			sys.exit()



# Given a position coordinate, this function returns the cell coordinate
def get_cell_coord(pos):
	return (pos[1] // (Cell.CELL_LENGTH + Board.PADDING), pos[0] // (Cell.CELL_LENGTH + Board.PADDING))

#Change a specific cell's color
def change_cell_color(cell_coord, new_color):
		y = cell_coord[0]
		x = cell_coord[1]
		board.cells[y][x].change_color(new_color)

def check_buttons(buttons, click_pos):
	for button in buttons:
		if(click_pos[0] >= button.x and click_pos[0] <= (button.x + button.width)):
			if(click_pos[1] >= button.y and click_pos[1] <= (button.y + button.height)):
				return button
			else:
				continue

board = Board()

#Run Game
def run_game():
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				#Left click
				if pygame.mouse.get_pressed()[0]:
					pos = pygame.mouse.get_pos()
					cell_coord = get_cell_coord(pos)
					change_cell_color(cell_coord, RED)
					#print('left click at: ' + str(cell_coord))
		board.draw(game_surface)
		screen.blit(game_surface, (0,0))
		pygame.display.update()
		clock.tick(60)

#Opening menu 
def run_menu():
	start = Button('START', 200, 200, 100, 40, WHITE)
	exit =  Button('EXIT', 200, 300, 100, 40, WHITE)
	buttons = [start, exit]

	running = True
	while running:
		#print(start.activated)
		#print(exit.activated)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0]:
					pos = pygame.mouse.get_pos()
					clicked_button = check_buttons(buttons, pos)
					if clicked_button != None:
						clicked_button.clicked()
		
		start.draw(menu_surface)
		exit.draw(menu_surface)

		teeko_text = teeko_font.render('TEEKO', True, (255,255,255))
		menu_surface.blit(teeko_text, (100, 100))
		screen.blit(menu_surface, (0,0))
		pygame.display.update()
		clock.tick(60)

run_menu()
pygame.quit()