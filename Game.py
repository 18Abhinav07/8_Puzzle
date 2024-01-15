import sys
import pygame
from Values import *
from Mechanics import *
from Puzzle_AI import *


class GAME:
    def __init__(self):
        self.playing = None
        pygame.init()
        self.SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("8 Puzzle Game")
        self.SCREEN.fill(BLACK)

    def draw(self):
        self.drawGrid()

    def drawGrid(self):
        # Draw the grid
        for x in range(WINDOW_WIDTH // 4, WINDOW_WIDTH // 4 + blockSize * 3, blockSize):
            for y in range(WINDOW_WIDTH // 8, blockSize * 3, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(self.SCREEN, WHITE, rect, 1)

    def newGame(self):
        pass

    def run(self):
        self.playing = True
        while self.playing:
            self.draw()
            self.events()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    game = GAME()
    while True:
        game.newGame()
        game.run()
