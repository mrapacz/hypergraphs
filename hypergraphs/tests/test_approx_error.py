from unittest import TestCase

import networkx as nx
from PIL import Image

from procedures import approx_error
from productions import P1
from utils import HyperEdge

img_size = (10, 10)


class TestApproxError(TestCase):

    def test_red_bitmap(self):
        self.__test_x_bitmap(255, 0, 0)

    def test_green_bitmap(self):
        self.__test_x_bitmap(0, 255, 0)

    def test_blue_bitmap(self):
        self.__test_x_bitmap(0, 0, 255)

    def test_white_bitmap(self):
        self.__test_x_bitmap(255, 255, 255)

    def test_black_bitmap(self):
        self.__test_x_bitmap(0, 0, 0)

    def __test_x_bitmap(self, r, g, b):
        self.graph = nx.Graph()
        self.image = Image.new('RGB', img_size, color=(r, g, b))
        width, height = self.image.size
        self.x_max_idx = width - 1
        self.y_max_idx = height - 1
        P1(self.graph, self.x_max_idx, self.y_max_idx, self.image)
        # plot(self.graph)

        i_hyperedges_ids = self.__hyperedges_ids(HyperEdge.I)
        error = approx_error(self, self.image, self.graph, i_hyperedges_ids[0])
        self.assertEqual(error, 0.0)

    def __hyperedges_ids(self, label):
        return [idd for idd, data in self.__hyperedges(label)]

    def __hyperedges(self, label):
        return [(idd, data) for idd, data in self.graph.nodes(data=True)
                if 'label' in data.keys() and data['label'] == label.name]
