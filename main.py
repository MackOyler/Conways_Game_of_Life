import pygame
import random
import numpy as np
import pickle

# Initialize Pygame
pygame.init()

# Constants
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
DARK_GREY = (50, 50, 50)

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
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

def gen_random(num, seed=None):
    if seed is not None:
        random.seed(seed)
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
    total = np.sum(grid[max(0, x-1):min(GRID_HEIGHT, x+2), max(0, y-1):min(GRID_WIDTH, y+2)]) - grid[x, y]
    # Wrap around edges
    if x == 0:
        total += np.sum(grid[GRID_HEIGHT-1:max(0, x+2), max(0, y-1):min(GRID_WIDTH, y+2)]) - grid[GRID_HEIGHT-1, y]
    if x == GRID_HEIGHT - 1:
        total += np.sum(grid[0:2, max(0, y-1):min(GRID_WIDTH, y+2)]) - grid[0, y]
    if y == 0:
        total += np.sum(grid[max(0, x-1):min(GRID_HEIGHT, x+2), GRID_WIDTH-1:max(0, y+2)]) - grid[x, GRID_WIDTH-1]
    if y == GRID_WIDTH - 1:
        total += np.sum(grid[max(0, x-1):min(GRID_HEIGHT, x+2), 0:2]) - grid[x, 0]
    return total

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

def save_grid(grid, filename="grid.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(grid, f)

def load_grid(filename="grid.pkl"):
    with open(filename, "rb") as f:
        return pickle.load(f)

# Track button clicks
button_pressed = {
    "step_forward": False,
    "step_backward": False
}

def draw_button(screen, text, x, y, w, h, inactive_color, active_color, action=None, button_name=None):
    global button_pressed
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            if not button_pressed[button_name]:
                button_pressed[button_name] = True
                action()
        elif click[0] == 0:
            button_pressed[button_name] = False
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=((x + (w / 2)), (y + (h / 2))))
    screen.blit(text_surface, text_rect)

def clear_grid():
    global grid, grid_history, history_index
    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
    grid_history = [grid.copy()]
    history_index = 0

def regenerate_grid():
    global grid, grid_history, history_index
    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
    positions = gen_random(random.randrange(4, 10) * GRID_WIDTH)
    for pos in positions:
        grid[pos[1], pos[0]] = ALIVE
    grid_history = [grid.copy()]
    history_index = 0

def step_forward():
    global grid, grid_history, history_index
    grid = update_grid(grid)
    history_index += 1
    if history_index < len(grid_history):
        grid_history[history_index] = grid.copy()
    else:
        grid_history.append(grid.copy())

def step_backward():
    global grid, grid_history, history_index
    if history_index > 0:
        history_index -= 1
        grid = grid_history[history_index].copy()

def main():
    global grid, grid_history, history_index, button_pressed
    running = True
    playing = False
    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
    grid_history = [grid.copy()]
    history_index = 0
    step = False
    speed = 1

    while running:
        clock.tick(FPS * speed)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col, row = x // TILE_SIZE, y // TILE_SIZE
                if y > 40:  # Avoid clicking the buttons
                    grid[row, col] = ALIVE if grid[row, col] == DEAD else DEAD

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                elif event.key == pygame.K_c:
                    clear_grid()
                    playing = False
                elif event.key == pygame.K_g:
                    regenerate_grid()
                elif event.key == pygame.K_s:
                    save_grid(grid)
                elif event.key == pygame.K_l:
                    grid = load_grid()
                    grid_history = [grid.copy()]
                    history_index = 0
                elif event.key == pygame.K_RIGHT:
                    step_forward()
                elif event.key == pygame.K_LEFT:
                    step_backward()
                elif event.key == pygame.K_UP:
                    speed = min(speed + 1, 10)
                elif event.key == pygame.K_DOWN:
                    speed = max(speed - 1, 1)
        
        if playing or step:
            step_forward()
            step = False
        
        screen.fill(GREY)
        draw_grid(grid)

        # Draw buttons
        draw_button(screen, "Clear", 10, 5, 120, 30, DARK_GREY, BLACK, clear_grid)
        draw_button(screen, "Regenerate", 140, 5, 140, 30, DARK_GREY, BLACK, regenerate_grid)
        draw_button(screen, "Step <-", 290, 5, 120, 30, DARK_GREY, BLACK, step_backward, button_name="step_backward")
        draw_button(screen, "Step ->", 420, 5, 120, 30, DARK_GREY, BLACK, step_forward, button_name="step_forward")
        draw_button(screen, "Save", 550, 5, 120, 30, DARK_GREY, BLACK, lambda: save_grid(grid))
        
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main()
