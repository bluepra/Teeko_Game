import pygame
pygame.init()

#Constants
SCREEN_WIDTH = 560
SCREEN_HEIGHT = 600
WHITE = (255,255,255)
PADDING = 10
BOX_LENGTH = 100

#Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Teeko")

# Draws the 5x5 game board onto the screen
def better_draw_board():
	for i in range(5):
		for j in range(5):
			x = PADDING + (BOX_LENGTH + PADDING) * i
			y = PADDING + (BOX_LENGTH + PADDING) * j
			pygame.draw.rect(screen, WHITE, (x,y, BOX_LENGTH, BOX_LENGTH))
	return

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	better_draw_board()
	pygame.display.update()
	

pygame.quit()