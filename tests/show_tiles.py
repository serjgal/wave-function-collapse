import pygame
from PIL.Image import Image
from pygame.sprite import Sprite
from PIL import Image
from wfc import *
import sys
import math

clock = pygame.time.Clock()
running = True

img_path = "../images/City.png"
img = Image.open(img_path)

width, height = img.size
tiles = generate_tiles(img)

tile_size = 50

pygame.init()
print(len(tiles))
d = int(math.sqrt(len(tiles)))
w, h = d * tile_size * 2, d * tile_size * 2
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Tile show")

group = pygame.sprite.Group()
for i, t in enumerate(tiles):
    data = t.get_image()
    data = pygame.transform.scale(data, (tile_size, tile_size))
    cx = i % d
    cy = i // d
    r = pygame.Rect(cx * 3 / 2 * tile_size, cy * 3 / 2 * tile_size, tile_size, tile_size)

    sprite = Sprite(group)
    sprite.image = data
    sprite.rect = r

print([t.weight for t in tiles])

if __name__ == "__main__":
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((227, 148, 185))
        group.draw(screen)

        pygame.display.flip()
        clock.tick(1)  # limit to 60 FPS

    pygame.quit()
    sys.exit()
