import os

import networkx as nx
from PIL import Image

from unittest import TestCase
from bitplot import AproxError
from bitplot import AproxPlot

from typing import Tuple
from productions import P1
from utils import get_node_id


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

        result = p.aprox_err(0, 0, 1, 1, (255, 0, 128), (255, 128, 255), (128, 128, 128), (128, 255, 255))
        self.assertEqual(result, 0.0)
        self.check_matrix(p.DIFF_R)
        self.check_matrix(p.DIFF_G)
        self.check_matrix(p.DIFF_B)

    def test_green_color_aprox_error(self):
        self.__test_bitmap((2, 2), (0, 255, 0))

    def test_blue_color_aprox_error(self):
        self.__test_bitmap((2, 2), (0, 0, 255))

    def check_matrix(self, m):
        for i in m:
            for c in i:
                self.assertEqual(c, 0.0)

    def __test_bitmap(self, img_size: Tuple[int, int], rgb: Tuple[int, int, int]):
        graph = nx.Graph()
        image = Image.new('RGB', img_size, color=rgb)
        x_max = img_size[0] - 1
        y_max = img_size[1] - 1
        P1(graph, x_max, y_max, image)

        p = AproxError.from_image(image)

        i_hyperedges_ids = self.__hyperedges_ids(graph)

        error = p.aprox_err_from_graph(graph, i_hyperedges_ids[0], AproxPlot(x_max, y_max))
        self.assertEqual(error, 0.0)
        self.check_matrix(p.DIFF_R)
        self.check_matrix(p.DIFF_G)
        self.check_matrix(p.DIFF_B)

    def __hyperedges_ids(self, graph: nx.Graph):
        return [node_id for node_id, data in graph.nodes(data=True) if data['is_hyperedge'] and data['label'] == 'I']

