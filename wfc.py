import random
from random import choice
random.seed(4)

import pygame
import numpy as np
from support import *

class Tile:
    img: pygame.Surface
    img_data: np.ndarray

    center_img: pygame.Surface
    center_img_data: np.ndarray

    tile_size: int = 3

    neighbors: dict[str, list['Tile']]

    def __init__(self, source_img_data: np.ndarray, x: int, y: int):
        self.img_data = wrapped_subimg(source_img_data, x, y, self.tile_size, self.tile_size)
        self.img = pygame.surfarray.make_surface(self.img_data)

        px = self.img_data[self.tile_size // 2, self.tile_size // 2]  # shape (3,)
        self.center_img_data = px
        self.center_img = pygame.surfarray.make_surface(np.array([[px]])) # shape (1,1,3)

        self.neighbors = {"top": [], "right": [], "bottom": [], "left": []}

    def draw_full(self, surface, x, y, size):
        scaled = pygame.transform.scale(self.img, (size, size))
        surface.blit(scaled, (x, y))

    def draw_center(self, surface, x, y, size):
        scaled = pygame.transform.scale(self.center_img, (size, size))
        surface.blit(scaled, (x, y))

    def set_neighbors(self, all: list['Tile']):
        midI = self.tile_size // 2

        for other in all:
            # top
            if np.array_equal(self.img_data[:, :midI + 1], other.img_data[:, midI:]):
                self.neighbors["top"].append(other)
            # right
            if np.array_equal(self.img_data[midI:, :], other.img_data[:midI + 1, :]):
                self.neighbors["right"].append(other)
            # bottom
            if np.array_equal(self.img_data[:, midI:], other.img_data[:, :midI + 1]):
                self.neighbors["bottom"].append(other)
            # left
            if np.array_equal(self.img_data[:midI + 1, :], other.img_data[midI:, :]):
                self.neighbors["left"].append(other)

class Cell:

    x: int
    y: int

    posable_tiles: list[Tile]
    is_collapsed: bool
    is_checked: bool

    img: pygame.Surface
    img_data: np.ndarray

    FAIL_COLOR: tuple[int, int, int] = (0,0,0)

    def __init__(self, all: list[Tile], x: int, y: int):
        self.x = x
        self.y = y

        self.posable_tiles = all[::]
        self.is_collapsed = False
        self.is_checked = False

        self.img_data = np.array(self.get_average_color())
        color = tuple(int(c) for c in self.img_data)
        self.img = pygame.Surface((1, 1))
        self.img.fill(color)

        self.is_error = False

    def get_average_color(self):
        n = len(self.posable_tiles)
        r = g = b = 0

        for t in self.posable_tiles:
            cx = t.center_img_data.astype(int)  # rgb array shape (3,)
            r += cx[0]
            g += cx[1]
            b += cx[2]

        return r // n, g // n, b // n

    def draw(self, surface, size: int):
        dx, dy = self.x * size, self.y * size
        pos = (dx, dy)

        # if self.is_error: return
        if len(self.posable_tiles) == 0:
            self.img_data = np.array(Cell.FAIL_COLOR)
            # self.is_collapsed = True
            self.is_error = True

        if self.is_collapsed:
            self.posable_tiles[0].draw_center(surface, dx, dy, size)
        else:
            if self.is_error:
                self.img_data = np.array(Cell.FAIL_COLOR)
            else:
                self.img_data = np.array(self.get_average_color())
            color = tuple(int(c) for c in self.img_data)
            self.img = pygame.Surface((1, 1))
            self.img.fill(color)

            scaled = pygame.transform.scale(self.img, (size, size))
            surface.blit(scaled, pos)

            pygame.draw.rect(surface, (0, 0, 0), (dx, dy, size, size), 1)

    def get_entropy(self): return len(self.posable_tiles)

    @classmethod
    def set_fail_color(cls, color: tuple[int, int, int]):
        cls.FAIL_COLOR = color

def reduce_entropy(cells: list[Cell], cell: Cell, dim: int, depth: int = 0, max_depth: int = 1):
    if depth >= max_depth: return

    if cell.is_checked or cell.is_error: return
    cell.is_checked = True

    toI = lambda x, y: x * dim + y
    x, y = cell.x, cell.y

    def check_neighbor(dx: int, dy: int, direction: str):
        nx = x + dx
        ny = y + dy

        if not (0 <= nx < dim and 0 <= ny < dim): return
        neighbor = cells[toI(nx, ny)]
        if neighbor.is_collapsed or neighbor.is_error: return

        valid = []
        for t in cell.posable_tiles:
            valid.extend(t.neighbors[direction])

        neighbor.posable_tiles = [t for t in neighbor.posable_tiles if t in valid]
        reduce_entropy(cells, neighbor, dim, depth + 1)

    checks = [
        (1, 0, "right"),
        (-1, 0, "left"),
        (0, 1, "bottom"),
        (0, -1, "top"),
    ]

    for dx, dy, direction in checks:
        check_neighbor(dx, dy, direction)



def wfc(cells: list[Cell], dim: int) -> bool:
    avalable_cells = [c for c in cells if not c.is_collapsed and not c.is_error]

    if len(avalable_cells) == 0: return True

    minE = min([c.get_entropy() for c in avalable_cells])
    min_cells = [c for c in avalable_cells if c.get_entropy() == minE]
    target = choice(min_cells)

    target.is_collapsed = True
    target.posable_tiles = [choice(target.posable_tiles)]

    reduce_entropy(cells, target, dim)

    return False



