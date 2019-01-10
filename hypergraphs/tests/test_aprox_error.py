import os
from unittest import TestCase
from bitplot import AproxError


class TestAproxError(TestCase):
    def setUp(self):
        self.BITMAP_R = [
            [128, 255],
            [128, 255]
        ]
        self.BITMAP_G = [
            [128, 0],
            [255, 128]
        ]
        self.BITMAP_B = [
            [128, 128],
            [255, 255]
        ]

    def test_simple_aprox_error(self):
        p = AproxError(self.BITMAP_R, self.BITMAP_G, self.BITMAP_B)

        def check_matrix(m):
            for i in m:
                for c in i:
                    self.assertEqual(c, 0.0)

        result = p.aprox_err(0, 0, 1, 1, (255, 0, 128), (255, 128, 255), (128, 128, 128), (128, 255, 255))
        self.assertEqual(result, 0.0)
        check_matrix(p.DIFF_R)
        check_matrix(p.DIFF_G)
        check_matrix(p.DIFF_B)
