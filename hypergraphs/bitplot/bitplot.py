import networkx as nx

from typing import Tuple

# Zad12
# Author: Sebastian Haracz

APPROX_R = [[]]
APPROX_G = [[]]
APPROX_B = [[]]


def aprox_zad12(x1: int, y1: int, x2: int, y2: int, rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int], rgb3: Tuple[int, int, int], rgb4: Tuple[int, int, int]):
    def update_matrix(x: int, y: int, mul: float, rgb: Tuple[int, int, int]):
        APPROX_R[x][y] += rgb[0] * mul
        APPROX_G[x][y] += rgb[1] * mul
        APPROX_B[x][y] += rgb[2] * mul

    for px in [x1, x2]:
        for py in [y1, y2]:
            px1 = (px - x1) / (x2 - x1)
            py1 = (py - y1) / (y2 - y1)

            mul1 = (1.0 - px1) * py1
            update_matrix(px, py, mul1, rgb1)

            mul2 = px1 * py1
            update_matrix(px, py, mul2, rgb2)

            mul3 = (1.0 - px1) * (1.0 - py1)
            update_matrix(px, py, mul3, rgb3)

            mul4 = px1 * (1.0 - py1)
            update_matrix(px, py, mul4, rgb4)
