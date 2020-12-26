import pygame
pygame.init()

#Constants
SCREEN_WIDTH = 530
SCREEN_HEIGHT = 600

#Colors
WHITE = (255,255,255)
RED = (255, 0, 0)

#Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Teeko")

class Cell:
	CELL_LENGTH = 100
	def __init__(self, x, y, color):
		#print('creating cell')
		self.x = x
		self.y = y
		self.color = color

	def change_color(self, new_color):
		self.color = new_color

	def draw(self):
		pygame.draw.rect(screen, self.color, (self.x, self.y, Cell.CELL_LENGTH, Cell.CELL_LENGTH))

class Board:
	PADDING = 5
	cells = []
	def __init__(self):
		#print('creating board')
		for i in range(5):
			row_of_cells = []
			for j in range(5):
				x = Board.PADDING + (Cell.CELL_LENGTH + Board.PADDING) * i
				y = Board.PADDING + (Cell.CELL_LENGTH + Board.PADDING) * j
				new_cell = Cell(x,y, WHITE)
				row_of_cells.append(new_cell)
			self.cells.append(row_of_cells)


	# Draws the 5x5 game board onto the screen
	def draw(self):
		for i in range(5):
			for j in range(5):
				curr_cell = self.cells[i][j]
				curr_cell.draw()


# Given a position coordinate, this function returns the cell coordinate
def get_cell_coord(pos):
	return (pos[0] // (Cell.CELL_LENGTH + Board.PADDING), pos[1] // (Cell.CELL_LENGTH + Board.PADDING))

def change_cell_color(cell_coord, new_color):
		x = cell_coord[0]
		y = cell_coord[1]
		board.cells[x][y].change_color(new_color)


board = Board()

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				cell_coord = get_cell_coord(pos)
				change_cell_color(cell_coord, RED)
				print('left click at: ' + str(cell_coord))

	board.draw()
	pygame.display.update()
	

pygame.quit()
