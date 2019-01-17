from unittest import TestCase

import networkx as nx
from PIL import Image
from procedures import approx_error
from productions import P1, P2
import utils
from utils import HyperEdge, get_common_nodes, init

img_size = (10, 10)

class TestApproxError(TestCase):

    def __init_APPROX(self, r, g, b):
        init()
        init_r, init_g, init_b = [], [], []

        utils.APPROX_R, utils.APPROX_G, utils.APPROX_B = [], [], []

        for _ in range(self.image.width):
            init_r.append(r)
            init_g.append(g)
            init_b.append(b)
        for _ in range(self.image.height):
            utils.APPROX_R.append(init_r.copy())
            utils.APPROX_G.append(init_g.copy())
            utils.APPROX_B.append(init_b.copy())

    def test_only_I_hyperedge_passes(self):
        self.graph = nx.Graph()
        self.image = Image.new('RGB', img_size, color=(0, 0, 0))
        width, height = self.image.size
        self.x_max_idx = width - 1
        self.y_max_idx = height - 1
        P1(self.graph, self.x_max_idx, self.y_max_idx, self.image)
        i_hyperedges_ids = self.__hyperedges_ids(HyperEdge.I)
        # P5(self.graph, i_hyperedges_ids[0], self.image)
        # P2(self.graph, i_hyperedges_ids[0], self.image)
        # plot(self.graph)

        b_hyperedges_ids = self.__hyperedges_ids(HyperEdge.B)
        # f1_hyperedges_ids = self.__hyperedges_ids(Direction.N) + self.__hyperedges_ids(Direction.S)
        # f2_hyperedges_ids = self.__hyperedges_ids(Direction.E) + self.__hyperedges_ids(Direction.W)
        self.assertRaises(ValueError, approx_error, self, self.image, self.graph, b_hyperedges_ids[0])
        # self.assertRaises(ValueError, approx_error, self, self.image, self.graph, f1_hyperedges_ids[0])
        # self.assertRaises(ValueError, approx_error, self, self.image, self.graph, f2_hyperedges_ids[0])

        common_node_id = get_common_nodes(self.graph, b_hyperedges_ids[0])[0]
        self.assertRaises(ValueError, approx_error, self, self.image, self.graph, common_node_id)

    def test_I_hyperedge_with_one_common_node_not_passes(self):
        self.graph = nx.Graph()
        self.image = Image.new('RGB', img_size, color=(0, 0, 0))
        width, height = self.image.size
        self.x_max_idx = width - 1
        self.y_max_idx = height - 1
        P1(self.graph, self.x_max_idx, self.y_max_idx, self.image)
        # plot(self.graph)

        i_hyperedge_id = self.__hyperedges_ids(HyperEdge.I)[0]
        common_nodes_ids = get_common_nodes(self.graph, i_hyperedge_id)
        for i in range(3):
            self.graph.remove_node(common_nodes_ids[i])
        self.assertRaises(ValueError, approx_error, self, self.image, self.graph, i_hyperedge_id)

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
        self.image = Image.new('RGB', img_size, color=(r, g, b))
        width, height = self.image.size
        self.x_max_idx = width - 1
        self.y_max_idx = height - 1
        self.__init_APPROX(r, g, b)

        # 4 common nodes
        self.__graph_init()
        error = approx_error(self, self.image, self.graph, self.i_hyperedge_id)
        self.assertEqual(error, 0.0)

        #3 common nodes -  4 variants
        for i in range(4):
            self.__graph_init()

            self.graph.remove_node(self.common_nodes_ids[i]) #czy na pewno beda do kolejne wierzcholki??
            error = approx_error(self, self.image, self.graph, self.i_hyperedge_id)
            self.assertEqual(error, 0.0)
            self.graph.add_node(self.common_nodes_ids[i], **self.common_nodes[i])

        #2 common nodes - 2 variants
        self.__graph_init()
        self.graph.remove_node(self.common_nodes_ids[0])
        self.graph.remove_node(self.common_nodes_ids[2])
        error = approx_error(self, self.image, self.graph, self.i_hyperedge_id)
        self.assertEqual(error, 0.0)
        self.graph.add_node(self.common_nodes_ids[0], **self.common_nodes[0])
        self.graph.add_node(self.common_nodes_ids[2], **self.common_nodes[2])

        self.__graph_init()
        self.graph.remove_node(self.common_nodes_ids[1])
        self.graph.remove_node(self.common_nodes_ids[3])
        error = approx_error(self, self.image, self.graph, self.i_hyperedge_id)
        self.assertEqual(error, 0.0)
        self.graph.add_node(self.common_nodes_ids[1], **self.common_nodes[1])
        self.graph.add_node(self.common_nodes_ids[3], **self.common_nodes[3])

    def __graph_init(self):
        self.graph = nx.Graph()
        P1(self.graph, self.x_max_idx, self.y_max_idx, self.image)
        # plot(self.graph)
        self.i_hyperedge_id = self.__hyperedges_ids(HyperEdge.I)[0]
        self.common_nodes_ids = get_common_nodes(self.graph, self.i_hyperedge_id)
        self.common_nodes = [self.graph.node[node] for node in self.common_nodes_ids]


    def __hyperedges_ids(self, label):
        return [idd for idd, data in self.__hyperedges(label)]

    def __hyperedges(self, label):
        return [(idd, data) for idd, data in self.graph.nodes(data=True)
                if 'label' in data.keys() and data['label'] == label.name]
