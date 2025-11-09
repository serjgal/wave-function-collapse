import random
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

    def get_color(self) -> tuple:
        return self.data[len(self.data)//2]


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

class cell:
    x: int
    y: int

    possible_tiles: list[tile]
    is_collapsed: bool

    color: tuple

    def __init__(self, x: int, y: int, all_tiles) -> None:
        self.x = x
        self.y = y

        self.possible_tiles = all_tiles[::]
        self.is_collapsed = False

    def get_avg_color(self) -> tuple:
        rs, gs, bs = 0, 0, 0
        for tile in self.possible_tiles:
            r, g, b, *_ = tile.get_color()
            rs += r
            gs += g
            bs += b
        rs /= len(self.possible_tiles)
        gs /= len(self.possible_tiles)
        bs /= len(self.possible_tiles)

        return int(rs), int(gs), int(bs)

    def get_entropy(self) -> float:
        if len(self.possible_tiles) == 1:
            return 0

        return sum(t.weight for t in self.possible_tiles) / len(self.possible_tiles)

    def collapse(self) -> None:
        self.is_collapsed = True
        weights = [p.weight for p in self.possible_tiles]
        r = random.choices(population= self.possible_tiles, weights =weights, k = 1)[0]

        self.possible_tiles = []
        self.color = r.get_color()


class wfc_sim:

    width: int
    height: int

    cells: list[cell]
    available_cells: list[cell]

    def __init__(self, width: int, height: int, all_tiles: list[tile]) -> None:
        self.width = width
        self.height = height

        self.cells = [
            cell(x, y, all_tiles)
            for y in range(height)
            for x in range(width)
        ]
        self.available_cells = self.cells[::]

    def get_cell(self, x: int, y: int) -> cell: return self.cells[y * self.width + x]

    def get_image(self) -> pygame.Surface:
        # Create the PIL image
        img = Image.new("RGB", (self.width, self.height))
        img_data = [c.get_avg_color() if not c.is_collapsed else c.color for c in self.cells]
        img.putdata(img_data)

        # Convert the PIL image to a Pygame surface
        mode = img.mode
        size = img.size
        data = img.tobytes()
        surface = pygame.image.fromstring(data, size, mode)

        return surface

    def iterate(self):
        if not self.available_cells: return

        min_cell = min(self.available_cells, key=lambda c: c.get_entropy())
        min_cell.collapse()
        self.available_cells.remove(min_cell)





