from unittest import TestCase

from PIL import Image

from procedures import approx_error

img_size = (100, 100)
x1 = 0
x2 = img_size[0] - 1
y1 = 0
y2 = img_size[0] - 1


class TestApproxError(TestCase):

    def _test_x_bitmap(self, r, g, b):
        img = Image.new('RGB', img_size, color=(r, g, b))
        error = approx_error(self, img, x1, x2, y1, y2, r, g, b, r, g, b, r, g, b, r, g, b)
        self.assertEqual(error, 0.0)

    def test_red_bitmap(self):
        self._test_x_bitmap(255, 0, 0)

    def test_green_bitmap(self):
        self._test_x_bitmap(0, 255, 0)

    def test_blue_bitmap(self):
        self._test_x_bitmap(0, 0, 255)

    def test_white_bitmap(self):
        self._test_x_bitmap(255, 255, 255)

    def test_black_bitmap(self):
        self._test_x_bitmap(0, 0, 0)
