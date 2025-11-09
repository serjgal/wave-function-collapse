from collections import Counter
import math

from PIL import Image
import PIL
import pygame

TILE_DIMENSIONS = (3, 3)
class tile:
    data: list[tuple] # list of RBG values
    weight: int

    north_p: list['tile']
    south_p: list['tile']
    east_p: list['tile']
    west_p: list['tile']

    def __init__(self, data: list[tuple], weight) -> None:
        # print(len(data))
        assert len(data) == TILE_DIMENSIONS[0] * TILE_DIMENSIONS[1]
        assert weight > 0

        self.data = data
        self.weight = weight

        self.north_p = []
        self.south_p = []
        self.east_p = []
        self.west_p = []

    def get_top(self):
        half = math.ceil(TILE_DIMENSIONS[1] / 2)
        ei = half * TILE_DIMENSIONS[0]
        return self.data[:ei]

    def get_bottom(self):
        half = math.ceil(TILE_DIMENSIONS[1] / 2)
        si = TILE_DIMENSIONS[1] - half
        si *= TILE_DIMENSIONS[0]
        return self.data[si:]

    def get_left(self):
        w, h = TILE_DIMENSIONS
        half = math.ceil(w / 2)
        left_half = []

        for y in range(h):
            start = y * w
            end = start + half
            left_half.extend(self.data[start:end])
        return left_half

    def get_right(self):
        w, h = TILE_DIMENSIONS
        half = math.ceil(w / 2)
        right_half = []

        for y in range(h):
            start = y * w + (w - half)
            end = start + half
            right_half.extend(self.data[start:end])
        return right_half

    def set_neighbors(self, tiles: list['tile']) -> None:
        st = self.get_top()
        sb = self.get_bottom()
        sr = self.get_right()
        sl = self.get_left()

        for t in tiles:
            if t is self: continue

            tt = t.get_top()
            tb = t.get_bottom()
            tr = t.get_right()
            tl = t.get_left()

            if st == tb: self.north_p.append(t)
            elif sb == tt: self.south_p.append(t)
            elif sr == tl: self.east_p.append(t)
            elif tl == tb: self.west_p.append(t)

    def get_image(self) -> pygame.Surface:
        # Create the PIL image
        img = Image.new("RGB", TILE_DIMENSIONS)
        img.putdata(self.data)

        # Convert the PIL image to a Pygame surface
        mode = img.mode
        size = img.size
        data = img.tobytes()
        surface = pygame.image.fromstring(data, size, mode)

        return surface

def generate_tiles(img: PIL.Image.Image) -> list[tile]:
    width, height = img.size
    pixels = img.load()

    safeX = lambda x: x % width
    safeY = lambda y: y % height

    dx = TILE_DIMENSIONS[0] // 2
    dy = TILE_DIMENSIONS[1] // 2

    tile_data = []
    for x in range(width):
        for y in range(height):
            tile_data.append(
                tuple(pixels[safeX(nx), safeY(ny)]
                           for ny in range(x - dx, x + dx + 1)
                           for nx in range(y - dy, y + dy + 1))
            )

    count = Counter(tile_data)
    tiles = [tile(d, c) for d, c in count.items()]
    return tiles
