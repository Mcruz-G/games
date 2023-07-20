import pygame
import sys
import random

pygame.font.init()

# Game configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
GRID_SIZE = 40
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

SHAPES = [
    {"shape": [[1, 1, 1, 1]], "color": (0, 255, 255)},  # Cyan I
    {"shape": [[1, 1], [1, 1]], "color": (255, 255, 0)},  # Yellow O
    {"shape": [[1, 1, 0], [0, 1, 1]], "color": (255, 165, 0)},  # Orange S
    {"shape": [[0, 1, 1], [1, 1]], "color": (0, 0, 255)},  # Blue Z
    {"shape": [[1, 1, 1], [0, 1, 0]], "color": (128, 0, 128)},  # Purple T
]

class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color

    def rotate(self):
        """Rotate the shape clockwise"""
        self.shape = [list(x)[::-1] for x in zip(*self.shape)]

def draw_grid(surface):
    """Draw the grid on the screen"""
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (WINDOW_WIDTH, y))

def draw_tetromino(surface, tetromino, x, y):
    """Draw a tetromino on the screen"""
    for row in range(len(tetromino.shape)):
        for col in range(len(tetromino.shape[row])):
            if tetromino.shape[row][col]:
                pygame.draw.rect(surface, tetromino.color, (x + col * GRID_SIZE, y + row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def check_collision(board, tetromino, x, y):
    """Check if the tetromino collides with the board"""
    for row in range(len(tetromino.shape)):
        for col in range(len(tetromino.shape[row])):
            if tetromino.shape[row][col]:
                if x + col < 0 or x + col >= GRID_WIDTH or y + row < 0 or y + row >= GRID_HEIGHT:
                    return True
                if board[y + row][x + col] != WHITE:
                    return True
    return False

def remove_row(board, row):
    """Remove a row from the board"""
    del board[row]
    board.insert(0, [WHITE for _ in range(GRID_WIDTH)])
    return 1

def move_shape(board, tetromino, x, y, dx, dy):
    """Move a tetromino"""
    x += dx
    y += dy
    if check_collision(board, tetromino, x, y):
        x -= dx
        y -= dy
    return x, y

def rotate_shape(board, tetromino, x, y):
    """Rotate a tetromino"""
    tetromino.rotate()
    if check_collision(board, tetromino, x, y):
        for _ in range(3):  # Rotate back to the original orientation
            tetromino.rotate()

def game_lost(board):
    """Check if the game is lost"""
    return any(board[0][i] != WHITE for i in range(GRID_WIDTH))

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame Tetris")

    board = [[WHITE for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    current_tetromino = Tetromino(random.choice(SHAPES)["shape"], random.choice(SHAPES)["color"])
    x, y = GRID_WIDTH // 2, 0
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x, y = move_shape(board, current_tetromino, x, y, -1, 0)
                elif event.key == pygame.K_RIGHT:
                    x, y = move_shape(board, current_tetromino, x, y, 1, 0)
                elif event.key == pygame.K_DOWN:
                    x, y = move_shape(board, current_tetromino, x, y, 0, 1)
                elif event.key == pygame.K_UP:
                    rotate_shape(board, current_tetromino, x, y)

        x, y = move_shape(board, current_tetromino, x, y, 0, 1)
        if check_collision(board, current_tetromino, x, y):
            for row in range(len(current_tetromino.shape)):
                for col in range(len(current_tetromino.shape[row])):
                    if current_tetromino.shape[row][col]:
                        board[y + row - 1][x + col] = current_tetromino.color
            current_tetromino = Tetromino(random.choice(SHAPES)["shape"], random.choice(SHAPES)["color"])
            x, y = GRID_WIDTH // 2, 0
            if game_lost(board):
                print("Game Over! Your score is:", score)
                pygame.quit()
                sys.exit()

        for i, row in enumerate(board):
            if all(cell != WHITE for cell in row):
                score += remove_row(board, i)

        screen.fill(WHITE)
        draw_grid(screen)
        draw_tetromino(screen, current_tetromino, x * GRID_SIZE, y * GRID_SIZE)
        pygame.display.flip()
        clock.tick(5)

if __name__ == "__main__":
    main()
