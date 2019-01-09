from unittest import TestCase

import networkx as nx
from PIL import Image

from main import approx

x1 = 0
x2 = 10
y1 = 0
y2 = 10

class aproxtests(TestCase):

    def test_red_bitmap(self):
        img = Image.new('RGB', (10, 10), color = (255, 0, 0))
        error = approx(img, x1, x2, y1, y2, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0)
        self.assertEqual( error, 0.00)


    def test_green_bitmap(self):
        img = Image.new('RGB', (10, 10), color = (0, 255, 0))
		error = approx(img, x1, x2, y1, y2, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0)
        self.assertEqual( error, 0.00)


    def test_blue_bitmap(self):
        img = Image.new('RGB', (10, 10), color = (0, 0, 255))
        error = approx(img, x1, x2, y1, y2, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255)
        self.assertEqual( error, 0.00)


    def test_white_bitmap(self):
        img = Image.new('RGB', (10, 10), color = (255, 255, 255))
        error = approx(img, x1, x2, y1, y2, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255)
        self.assertEqual( error, 0.00)


    def test_black_bitmap(self):
        img = Image.new('RGB', (10, 10), color = (0, 0, 0))
        error = approx(img, x1, x2, y1, y2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.assertEqual( error, 0.00)