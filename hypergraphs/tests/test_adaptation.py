from unittest import TestCase

import networkx as nx
from PIL import Image

from procedures import mark_hyperedges_for_adaptation
from productions import P2, P1, Direction
from tests.test_p1 import IMAGE_PATH
from tests.test_p3 import B_DIRECTION_EDGE_LAMBDAS
from utils import get_node_id


class TestDrawing(TestCase):
    def testAdaptation(self):
        # Example data stolen from test_p3
        self.graph = nx.Graph()
        self.image = Image.open(IMAGE_PATH)
        width, height = self.image.size
        P1(self.graph, x_max_idx=width - 1, y_max_idx=height - 1, image=self.image)
        hyperedge = [(x, y) for x, y in self.graph.nodes(data=True) if 'label' in y.keys() and y['label'] == 'I'][0]
        hyperedge[1]['should_break'] = 1
        self.graph.add_node(hyperedge[0], **hyperedge[1])
        P2(self.graph, hyperedge_id=hyperedge[0], image=self.image)

        # plot(self.graph)

        self.hyp_fs = [(x, y) for x, y in self.graph.nodes(data=True) if
                       'label' in y.keys() and y['label'] in Direction]
        self.hyp_bs = [(x, y) for x, y in self.graph.nodes(data=True) if 'label' in y.keys() and y['label'] == 'B']
        self.hyp_is = [(x, y) for x, y in self.graph.nodes(data=True) if 'label' in y.keys() and y['label'] == 'I']
        self.hyperedges = {
            Direction.N: {},
            Direction.S: {},
            Direction.E: {},
            Direction.W: {},
        }
        for direction, edges in self.hyperedges.items():
            edges['f'] = [x for x in self.hyp_fs if x[1]['label'] == direction][0]
            edges['b'] = [(x, y) for x, y in self.hyp_bs if B_DIRECTION_EDGE_LAMBDAS[direction](y, edges['f'][1])][0]

            f_neighbour = list(self.graph.neighbors(edges['f'][0]))[0]
            b_neighbours = list(self.graph.neighbors(edges['b'][0]))
            edges['is'] = []
            for x, y in self.graph.nodes(data=True):
                if 'label' in y and y['label'] == 'I':
                    i_neighbours = list(self.graph.neighbors(x))

                    if f_neighbour in i_neighbours and (
                            b_neighbours[0] in i_neighbours or b_neighbours[1] in i_neighbours):
                        edges['is'].append((x, y))

        mark_hyperedges_for_adaptation(self.graph, 0.1, self.image)

    def prepare_graph_and_get_central_hyperedge(self):
        # Stolen from test_p2 for testing purposes, to be removed
        width, height = self.image.size
        P1(self.graph, x_max_idx=width - 1, y_max_idx=height - 1, image=self.image)
        hyperedges_to_remove = [x for x, y in self.graph.nodes(data=True) if 'label' in y.keys() and y['label'] == 'B']
        for id in hyperedges_to_remove:
            self.graph.remove_node(id)
        hyperedge = [(x, y) for x, y in self.graph.nodes(data=True) if 'label' in y.keys() and y['label'] == 'I'][0]
        hyperedge[1]['should_break'] = 1
        self.graph.add_node(hyperedge[0], **hyperedge[1])
        return hyperedge
