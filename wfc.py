from PIL import Image
import PIL
import pygame

TILE_DIMENSIONS = (3, 3)
class tile:
    data: list[tuple] # list of RBG values

    def __init__(self, data: list[tuple]) -> None:
        # print(len(data))
        assert len(data) == TILE_DIMENSIONS[0] * TILE_DIMENSIONS[1]
        self.data = data

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

    tile_data = set()
    for x in range(width):
        for y in range(height):
            tile_data.add(
                tuple(pixels[safeX(nx), safeY(ny)]
                           for ny in range(x - dx, x + dx + 1)
                           for nx in range(y - dy, y + dy + 1))
            )

    tiles = [tile(d) for d in tile_data]
    return tiles
