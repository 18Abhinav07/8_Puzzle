import time

import pygame
from pygame.locals import *
from Puzzle_AI import *

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 400, 400
ROWS, COLS = 3, 3
SQUARE_SIZE = WIDTH // (COLS + 2)  # Leave space for margins
MARGIN = SQUARE_SIZE  # Margin size

# Set up the display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the puzzle state
start_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]


def draw_window(state, message):
    WIN.fill((255, 255, 255))

    # Draw the grid
    for i in range(ROWS):
        for j in range(COLS):
            pygame.draw.rect(WIN, (0, 0, 0),
                             (MARGIN + j * SQUARE_SIZE, MARGIN + i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

            # Draw the numbers
            font = pygame.font.Font(None, 36)
            text = font.render(str(state[i][j]), 1, (0, 0, 0))
            WIN.blit(text, (MARGIN + j * SQUARE_SIZE + SQUARE_SIZE // 2 - text.get_width() // 2,
                            MARGIN + i * SQUARE_SIZE + SQUARE_SIZE // 2 - text.get_height() // 2))

    # Draw the message
    font = pygame.font.Font(None, 24)
    text = font.render(message, 1, (0, 0, 0))
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - MARGIN // 2 - text.get_height() // 2))

    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    message = "Welcome to 8 Puzzle!"

    while run:
        clock.tick(60)
        solver = PUZZLE_SOlVER(start_state)
        draw_window(start_state, "The solver has found a way")

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                run = False

        solution_set = solver.get_solution()

        for state in solution_set:
            time.sleep(0.05)
            draw_window(state, "Working it out")

        draw_window(solver.GOAL_STATE, f"Done. The puzzle has been solved in {solver.count} steps.")
        time.sleep(2.0)
        run = False
    pygame.quit()


if __name__ == "__main__":
    main()
