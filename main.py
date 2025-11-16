import random
import pygame
import numpy as np
import sys
from wfc import Tile, Cell, wfc
from support import get_max_contrast_color

# Initialization
pygame.init()

WIDTH = 800
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Blank Pygame Script")

clock = pygame.time.Clock()
FPS = 100

# WFC
DIMENSIONS = 20
CELL_D  = WIDTH // DIMENSIONS
base_img_path = "images/City.png"

# Main Game Loop
def main():
    base_img = pygame.image.load(base_img_path)
    base_img_data = pygame.surfarray.array3d(base_img)
    base_img_w, base_img_h, base_img_d = base_img_data.shape

    toI = lambda x, y: x * base_img_h + y
    fc = get_max_contrast_color(base_img)
    Cell.set_fail_color(fc)
    print(fc)

    all_tiles = []
    for x in range(base_img_w):
        for y in range(base_img_h):
            all_tiles.append(Tile(base_img_data, x, y))
    for tile in all_tiles:
        tile.set_neighbors(all_tiles)

    all_cells = []
    for x in range(DIMENSIONS):
        for y in range(DIMENSIONS):
            all_cells.append(Cell(all_tiles, x, y))


    running = True
    is_done = False
    while running:
        dt = clock.tick(1 if is_done else FPS) / 1000  # delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        is_done = wfc(all_cells, DIMENSIONS)

        # Drawing logic here
        screen.fill((247, 161, 239))  # Clear screen to black
        for cell in all_cells:
            cell.is_checked = False
            cell.draw(screen, CELL_D)




        pygame.display.flip()
    pygame.quit()
    sys.exit()

# test to find fail
def test(seed: int):
    random.seed(seed)

    base_img = pygame.image.load(base_img_path)
    base_img_data = pygame.surfarray.array3d(base_img)
    base_img_w, base_img_h, base_img_d = base_img_data.shape

    toI = lambda x, y: x * base_img_h + y

    all_tiles = []
    for x in range(base_img_w):
        for y in range(base_img_h):
            all_tiles.append(Tile(base_img_data, x, y))
    for tile in all_tiles:
        tile.set_neighbors(all_tiles)

    all_cells = []
    for x in range(DIMENSIONS):
        for y in range(DIMENSIONS):
            all_cells.append(Cell(all_tiles, x, y))

    is_done = False
    while not is_done:
        for c in all_cells:
            c.is_checked = False
        is_done = wfc(all_cells, DIMENSIONS)
    return True

# Start the program
if __name__ == "__main__":
    main()
