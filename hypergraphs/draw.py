import networkx as nx
from typing import Tuple
from PIL import Image

class Draw:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.APPROX_R = [[0.0 for x in range(abs(x1-x2)+1)] for y in range(abs(y1-y2)+1)]
        self.APPROX_G = [[0.0 for x in range(abs(x1-x2)+1)] for y in range(abs(y1-y2)+1)]
        self.APPROX_B = [[0.0 for x in range(abs(x1-x2)+1)] for y in range(abs(y1-y2)+1)]
    def approx(self, rgb1: Tuple[int, int, int],
                     rgb2: Tuple[int, int, int],
                     rgb3: Tuple[int, int, int],
                     rgb4: Tuple[int, int, int]):
        x_abs = int(abs(self.x1 - self.x2))
        y_abs = int(abs(self.y1 - self.y2))
        approx_t = (self.APPROX_R, self.APPROX_G, self.APPROX_B)

        for approx_v, c1, c2, c3, c4 in zip(approx_t, rgb1, rgb2, rgb3, rgb4):
            for x in range(x_abs+1):
                for y in range(y_abs+1):
                    approx_v[x][y] += c1*(1.0 - (x/x_abs))*(y/y_abs)
                    approx_v[x][y] += c2*(x/x_abs)*(y/y_abs)
                    approx_v[x][y] += c3*(1.0 - (x/x_abs))*(1.0 - (y/y_abs))
                    approx_v[x][y] += c4*(x/x_abs)*(1.0 - (y/y_abs))

    def draw(self):
        x_abs = int(abs(self.x1 - self.x2))
        y_abs = int(abs(self.y1 - self.y2))
        bitmap = Image.new('RGB', (x_abs+1, y_abs+1), "black")
        pixels = bitmap.load()
        for x in range(x_abs+1):
            for y in range(y_abs+1):
                pixels[x, y] = (int(round(self.APPROX_R[x][y])),
                                int(round(self.APPROX_G[x][y])),
                                int(round(self.APPROX_B[x][y])))
        #bitmap.save("plik.jpg")
        bitmap.show()

    def get_approx(self):
        return (self.APPROX_R, self.APPROX_G, self.APPROX_B)

# d = Draw(0,0,100,100)
# d.approx((255,0,0),(0,255,0),(0,0,255),(255,255,255))
# d.draw()
