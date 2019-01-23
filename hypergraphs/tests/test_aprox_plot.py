import os
from unittest import TestCase
from bitplot import AproxPlot


class TestAproxPlot(TestCase):

    def test_simple_aprox_plot(self):
        p = AproxPlot(1, 1)

        def check_matrix(result, expected):
            self.assertSequenceEqual(result, expected)

        p.aprox_zad12(0, 0, 1, 1, (255, 0, 128), (255, 128, 255), (128, 128, 128), (128, 255, 255))

        check_matrix(p.APPROX_R, [[128, 255], [128, 255]])
        check_matrix(p.APPROX_G, [[128, 0], [255, 128]])
        check_matrix(p.APPROX_B, [[128, 128], [255, 255]])
        p.draw()

    def test_large_aprox_plot(self):
        p = AproxPlot(2, 2)

        def check_matrix(result, expected):
            self.assertSequenceEqual(result, expected)

        p.aprox_zad12(0, 0, 2, 2, (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255))

        check_matrix(p.APPROX_R, [[0, 0, 0], [0, 63.75, 127.5], [0, 127.5, 255]])
        check_matrix(p.APPROX_G, [[255, 127.5, 0], [127.5, 63.75, 0], [0, 0, 0]])
        check_matrix(p.APPROX_B, [[0, 0, 0], [127.5, 63.75, 0], [255, 127.5, 0]])
        p.draw()

    def test_single_color_aprox_plot(self):
        p = AproxPlot(100, 100)
        p.aprox_zad12(0, 0, 100, 100, (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0))
        p.draw()

    def test_two_colors_aprox_plot(self):
        p = AproxPlot(100, 100)
        p.aprox_zad12(0, 0, 100, 100, (255, 0, 0), (0, 255, 0), (255, 0, 0), (0, 255, 0))
        p.draw()

    def test_two_diagonal_colors_aprox_plot(self):
        p = AproxPlot(100, 100)
        p.aprox_zad12(0, 0, 100, 100, (0, 0, 255), (0, 255, 0), (0, 255, 0), (0, 0, 255))
        p.draw()
