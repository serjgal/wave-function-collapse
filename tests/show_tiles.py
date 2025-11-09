import pygame
from PIL.Image import Image
from pygame.sprite import Sprite
from PIL import Image
from wfc import *
import sys

clock = pygame.time.Clock()
running = True

img_path = "../images/City.png"
img = Image.open(img_path)

width, height = img.size
tiles = generate_tiles(img)

tile_size = 50

pygame.init()
print(len(tiles))
w, h = len(tiles) // width, len(tiles) // height
w, h = w * tile_size * 2, h * tile_size * 2
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Tile show")

group = pygame.sprite.Group()
for i, t in enumerate(tiles):
    d = t.get_image()
    d = pygame.transform.scale(d, (tile_size, tile_size))
    cx = i % width
    cy = i // height
    r = pygame.Rect(cx * 3 / 2 * tile_size, cy * 3 / 2 * tile_size, tile_size, tile_size)

    sprite = Sprite(group)
    sprite.image = d
    sprite.rect = r

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
