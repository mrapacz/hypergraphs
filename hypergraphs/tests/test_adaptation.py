from unittest import TestCase

import networkx as nx
from PIL import Image

from plot import plot
from procedures import mark_hyperedges_for_adaptation
from productions import P2, P1, P5
from tests.test_p1 import IMAGE_PATH
from tests.test_p3 import B_DIRECTION_EDGE_LAMBDAS
from utils import get_node_id, Direction


class TestAdaptation(TestCase):

    def setUp(self):
        self.graph = nx.Graph()
        self.image = Image.open(IMAGE_PATH)
        self.hyperedge = self.prepare_graph_and_get_central_hyperedge()
        self.added_node_position = (self.hyperedge[1]['x'], self.hyperedge[1]['y'])
        self.added_node_id = get_node_id(self.added_node_position)
        # plot(self.graph)
        P2(self.graph, hyperedge_id=self.hyperedge[0], image=self.image)
        # self.sorted_nodes_with_data = sorted(self.graph.nodes(data=True), key=lambda x: (x[1]['x'], x[1]['y']))
        # plot(self.graph)

    def prepare_graph_and_get_central_hyperedge(self):
        width, height = self.image.size
        P1(self.graph, x_max_idx=width - 1, y_max_idx=height - 1, image=self.image)
        # hyperedges_to_remove = [x for x, y in self.graph.nodes(data=True) if 'label' in y.keys() and y['label'] == 'B']
        # for id in hyperedges_to_remove:
        #     self.graph.remove_node(id)
        hyperedge = [(x, y) for x, y in self.graph.nodes(data=True) if 'label' in y.keys() and y['label'] == 'I'][0]
        hyperedge[1]['should_break'] = 1
        self.graph.add_node(hyperedge[0], **hyperedge[1])
        return hyperedge

    def testAdaptation(self):
        mark_hyperedges_for_adaptation(self.graph, 0.1, self.image)
        plot(self.graph)
