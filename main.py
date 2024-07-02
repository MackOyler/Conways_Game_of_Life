import pygame
import random
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

# Rules for Conway's Game of Life
ALIVE = 1
DEAD = 0
STAY_ALIVE = [2, 3]
COME_ALIVE = [3]

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def gen_random(num):
    return {(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT)) for _ in range(num)}

def draw_grid(grid):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            color = YELLOW if grid[row, col] == ALIVE else GREY
            top_left = (col * TILE_SIZE, row * TILE_SIZE)
            pygame.draw.rect(screen, color, (*top_left, TILE_SIZE, TILE_SIZE))

    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))

def get_neighbors_count(grid, pos):
    x, y = pos
    return np.sum(grid[max(0, x-1):min(GRID_HEIGHT, x+2), max(0, y-1):min(GRID_WIDTH, y+2)]) - grid[x, y]

def update_grid(grid):
    new_grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            alive_neighbors = get_neighbors_count(grid, (row, col))
            if grid[row, col] == ALIVE and alive_neighbors in STAY_ALIVE:
                new_grid[row, col] = ALIVE
            elif grid[row, col] == DEAD and alive_neighbors in COME_ALIVE:
                new_grid[row, col] = ALIVE
    return new_grid

def main():
    running = True
    playing = False
    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
    
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col, row = x // TILE_SIZE, y // TILE_SIZE
                grid[row, col] = ALIVE if grid[row, col] == DEAD else DEAD

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                elif event.key == pygame.K_c:
                    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
                    playing = False
                elif event.key == pygame.K_g:
                    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
                    positions = gen_random(random.randrange(4, 10) * GRID_WIDTH)
                    for pos in positions:
                        grid[pos[1], pos[0]] = ALIVE
        
        if playing:
            grid = update_grid(grid)
        
        screen.fill(GREY)
        draw_grid(grid)
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main()
