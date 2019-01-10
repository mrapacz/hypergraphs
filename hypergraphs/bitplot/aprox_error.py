import networkx as nx

from typing import Tuple
from copy import copy, deepcopy

# Zad14
# Author: Michał Pluta


class AproxError:
    def __init__(self, BITMAP_R, BITMAP_G, BITMAP_B):
        self.DIFF_R = deepcopy(BITMAP_R)
        self.DIFF_G = deepcopy(BITMAP_G)
        self.DIFF_B = deepcopy(BITMAP_B)

    def aprox_err(self, x1: int, y1: int, x2: int, y2: int, rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int], rgb3: Tuple[int, int, int], rgb4: Tuple[int, int, int]):
        def update_diffs(x: int, y: int, mul: float, rgb: Tuple[int, int, int]):
            self.DIFF_R[x][y] -= rgb[0] * mul
            self.DIFF_G[x][y] -= rgb[1] * mul
            self.DIFF_B[x][y] -= rgb[2] * mul

        for px in [x1, x2]:
            for py in [y1, y2]:
                px1 = (px - x1) / (x2 - x1)
                py1 = (py - y1) / (y2 - y1)

                mul1 = (1.0 - px1) * py1
                update_diffs(px, py, mul1, rgb1)

                mul2 = px1 * py1
                update_diffs(px, py, mul2, rgb2)

                mul3 = (1.0 - px1) * (1.0 - py1)
                update_diffs(px, py, mul3, rgb3)

                mul4 = px1 * (1.0 - py1)
                update_diffs(px, py, mul4, rgb4)

        ERROR = 0.0
        for px in [x1, x2]:
            for py in [y1, y2]:
                ERROR += 0.5*(self.DIFF_R[px][py]) ** 2 + 0.3 * (self.DIFF_G[px][py]) ** 2 + 0.2 * (self.DIFF_B[px][py]) ** 2
        return ERROR
