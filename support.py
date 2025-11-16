import pygame
import numpy as np
import csv
import os

def wrapped_subimg(pixels, x, y, w, h):
    width, height = pixels.shape[:2]

    sub = np.zeros((w, h, 3), dtype=pixels.dtype)

    for i in range(w):
        for j in range(h):
            xi = (x + i) % width
            yj = (y + j) % height
            sub[i, j] = pixels[xi, yj]

    return sub

def get_max_contrast_color(surface: pygame.Surface) -> tuple[int, int, int]:
    # get the pixel array as (H, W, 3) uint8 array
    arr = pygame.surfarray.array3d(surface)
    arr = arr.astype(int)

    # compute average RGB of the image
    avg = arr.mean(axis=(0, 1))  # [r, g, b] floats
    avg_r, avg_g, avg_b = avg

    # compute opposite color for max contrast
    contrast_r = 255 - int(avg_r)
    contrast_g = 255 - int(avg_g)
    contrast_b = 255 - int(avg_b)

    return (contrast_r, contrast_g, contrast_b)

def log_kv_csv(filepath, **kwargs):
    """
    Appends a row of key=value data into a CSV file.
    Automatically creates the header if the file does not exist.
    """
    file_exists = os.path.exists(filepath)

    # Open in append mode
    with open(filepath, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=kwargs.keys())

        # If the file is new, write the header
        if not file_exists:
            writer.writeheader()

        # Write the actual row
        writer.writerow(kwargs)

