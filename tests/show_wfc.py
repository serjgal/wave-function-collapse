import pygame
from PIL.Image import Image
from pygame.sprite import Sprite
from PIL import Image

from tests.show_neighbors import width
from wfc import *
import sys
import math

clock = pygame.time.Clock()
running = True

img_path = "../images/City.png"
img = Image.open(img_path)

width, height = img.size
tiles = generate_tiles(img)
for t in tiles: t.set_neighbors(tiles)

cell_size = 30
width, height = 16, 16

pygame.init()
w, h = width * cell_size, height * cell_size
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("wfc show")

sim = wfc_sim(width, height, tiles)

group = pygame.sprite.Group()

data = sim.get_image()
data = pygame.transform.scale(data, (w, h))
r = pygame.Rect(0,0,w,h)

sprite = Sprite(group)
sprite.image = data
sprite.rect = r

if __name__ == "__main__":
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((227, 148, 185))
        group.draw(screen)

        sim.iterate()

        data = sim.get_image()
        data = pygame.transform.scale(data, (w, h))

        sprite.image = data

        pygame.display.flip()
        clock.tick(100)  # limit to 60 FPS

    pygame.quit()
    sys.exit()
