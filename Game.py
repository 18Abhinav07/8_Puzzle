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
start_state = np.asarray([[1, 2, 3], [4, 5, 6], [7, 8, 0]])


def draw_window(state, message):
    TURQ = (0, 230, 230)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WIN.fill(BLACK)

    import pygame.freetype  # Import the freetype module.

    GAME_FONT = pygame.freetype.Font(None, 30)

    for i in range(ROWS):
        for j in range(COLS):
            # Change the color of the rectangles.
            pygame.draw.rect(WIN, RED if (i + j) % 2 == 0 else BLUE,
                             (MARGIN + j * SQUARE_SIZE, MARGIN + i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

            # Draw the numbers in a different color.
            text_surface, rect = GAME_FONT.render(str(state[i][j]), TURQ)
            WIN.blit(text_surface, (MARGIN + j * SQUARE_SIZE + SQUARE_SIZE // 2 - rect.width // 2,
                                    MARGIN + i * SQUARE_SIZE + SQUARE_SIZE // 2 - rect.height // 2))

    # Draw the message in a different color and font.
    MESSAGE_FONT = pygame.freetype.Font(None, 18)
    text_surface, rect = MESSAGE_FONT.render(message, TURQ)
    WIN.blit(text_surface, (WIDTH // 2 - rect.width // 2, HEIGHT - MARGIN // 2 - rect.height // 2))

    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    message = "Welcome to 8 Puzzle!"
    draw_window(start_state, message)
    time.sleep(2)
    solver = PUZZLE_SOlVER(start_state)

    if solver.isSolvable(start_state):
        if solver.start_analysis(start_state):
            while run:
                clock.tick(60)

                draw_window(start_state, "The solver has found a way")
                time.sleep(2)
                draw_window(start_state, "The solver is starting the implementation.")
                time.sleep(2)

                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        run = False

                solution_set = solver.get_solution()

                for state in solution_set:
                    time.sleep(0.005)
                    draw_window(state, "Working it out")

                draw_window(solver.GOAL_STATE, f"Done. The puzzle has been solved.")
                time.sleep(2.0)
                run = False
        else:
            draw_window(start_state, "Not solvable")
            time.sleep(2)
    else:
        draw_window(start_state, "Not solvable")
        time.sleep(2)
    pygame.quit()


if __name__ == "__main__":
    main()
