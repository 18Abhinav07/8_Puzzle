import time
import pygame
from pygame.locals import *
from solver_ai import *

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
cur = State([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
gol = State([[0, 1, 2], [3, 4, 5], [6, 7, 8]])


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
            text_surface, rect = GAME_FONT.render(str(state[i][j]) if state[i][j] != 0 else " ", TURQ)
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
    draw_window(cur.board, message)
    time.sleep(2)
    solver = Solver(cur, gol, 3)

    if solver.check_solvability(cur):
        if solver.solver():
            while run:
                clock.tick(60)

                draw_window(cur.board, "The solver has found a way")
                time.sleep(2)
                draw_window(cur.board, "The solver is starting the implementation.")
                time.sleep(2)

                solution_set = solver.path

                for state in solution_set:
                    time.sleep(0.005)
                    draw_window(state, "Working it out")

                draw_window(solver.goal_state.board, f"Done. The puzzle has been solved.")
                time.sleep(3.0)
                run = False
        else:
            draw_window(cur.board, "Not solvable")
            time.sleep(2)
    else:
        draw_window(cur.board, "Not solvable")
        time.sleep(2)
    pygame.quit()


if __name__ == "__main__":
    main()
