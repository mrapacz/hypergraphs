from unittest import TestCase

import networkx as nx
from PIL import Image

from hypergraphs.productions import P1, P2, P5, P3AutoDetect, P4
from hypergraphs.utils import HyperEdge, IMAGE_PATH, Direction, get_common_nodes, common_elements, get_b_nodes, get_all_f_nodes
import itertools
from hypergraphs.plot import plot


class TestP5(TestCase):
    def setUp(self):
        self.graph = nx.Graph()
        self.image = Image.open(IMAGE_PATH)

    def test_if_p5_breaks_hyperedge(self):
        hyperedge = self.__prepare_i_hyperedge()
        P5(self.graph, hyperedge[0], self.image)
        self.assertEqual(hyperedge[1]['should_break'], 1)

    def test_p5_should_not_brake_simple_node(self):
        self.__prepare_i_hyperedge()
        simple_nodes = [idd for idd, data in self.graph.nodes(data=True) if not data['is_hyperedge']]
        self.assertRaises(ValueError, P5, self.graph, simple_nodes[0], self.image)

    def test_p5_should_brake_only_i_hyperedge(self):
        self.__prepare_multi_hyperedge()
        b_hyperedges_ids = self.__hyperedges_ids(HyperEdge.B)
        f1_hyperedges_ids = self.__hyperedges_ids(Direction.N) + self.__hyperedges_ids(Direction.S)
        f2_hyperedges_ids = self.__hyperedges_ids(Direction.E) + self.__hyperedges_ids(Direction.W)

        self.assertRaises(ValueError, P5, self.graph, b_hyperedges_ids[0], self.image)
        self.assertRaises(ValueError, P5, self.graph, f1_hyperedges_ids[0], self.image)
        self.assertRaises(ValueError, P5, self.graph, f2_hyperedges_ids[0], self.image)

    # def test_p5_should_not_break_broken_hyperedge(self):
    #     hyperedge = self.__prepare_i_hyperedge()
    #     P5(self.graph, hyperedge[0], self.image)
    #     self.assertRaises(ValueError, P5, self.graph, hyperedge[0], self.image)

    # TODO when P3 will be committed
    def test_p6(self):
        width, height = self.image.size

        P1(self.graph, x_max_idx=width - 1, y_max_idx=height - 1, image=self.image)
        i_hyperedges_ids = self.__hyperedges_ids(HyperEdge.I)
        P5(self.graph, i_hyperedges_ids[0], self.image)
        new_i_hyperedges = P2(self.graph, i_hyperedges_ids[0], self.image)
        # Get B hyperedges
        # Find I common nodes
        i_common_nodes = [get_common_nodes(self.graph, i_hyperedge) for i_hyperedge in new_i_hyperedges]
        i_common_nodes = list(set(itertools.chain(*i_common_nodes)))
        # Test if between common nodes we have B hyperedges. Collect them.
        b_hyperedges = [common_elements(get_b_nodes(self.graph, common_node_a), get_b_nodes(self.graph, common_node_b))
            for common_node_a, common_node_b in itertools.combinations(i_common_nodes, 2)]
        b_hyperedges = list(set(itertools.chain(*b_hyperedges)))
        for b_hyperedge in b_hyperedges:
            print(self.graph.nodes[b_hyperedge]['label'])
            P3AutoDetect(self.graph, b_hyperedge, self.image)

        print("first P3 done")

        # Run P5 three times
        for i_hyperedge in new_i_hyperedges[1:]:
            P5(self.graph, i_hyperedge, self.image)

        # Run P2 three times
        new_i_hyperedges = [P2(self.graph, i_hyperedge, self.image) for i_hyperedge in new_i_hyperedges[1:]]
        new_i_hyperedges = list(set(itertools.chain(*new_i_hyperedges)))

        # Get B hyperedges
        # Find I common nodes
        i_common_nodes = [get_common_nodes(self.graph, i_hyperedge) for i_hyperedge in new_i_hyperedges]
        i_common_nodes = list(set(itertools.chain(*i_common_nodes)))
        # Test if between common nodes we have B hyperedges. Collect them.
        b_hyperedges = [common_elements(get_b_nodes(self.graph, common_node_a), get_b_nodes(self.graph, common_node_b))
            for common_node_a, common_node_b in itertools.combinations(i_common_nodes, 2)]
        b_hyperedges = list(set(itertools.chain(*b_hyperedges)))
        for b_hyperedge in b_hyperedges:
            print(self.graph.nodes[b_hyperedge]['label'])
            P3AutoDetect(self.graph, b_hyperedge, self.image)

        print("second P3 done")

        for f_hyperedge in get_all_f_nodes(self.graph):
            print(self.graph.nodes[f_hyperedge]['label'])
            try:
                P4(self.graph, f_hyperedge, self.image)
            except AssertionError:
                print("Bad one ;(")
                pass

        # Run
        # plot(self.graph)

    def __hyperedges_ids(self, label):
        return [idd for idd, data in self.__hyperedges(label)]

    def __hyperedges(self, label):
        return [(idd, data) for idd, data in self.graph.nodes(data=True)
                if 'label' in data.keys() and data['label'] == label.name]

    def __prepare_i_hyperedge(self):
        width, height = self.image.size
        P1(self.graph, x_max_idx=width - 1, y_max_idx=height - 1, image=self.image)

        hyperedges_to_remove = [x for x, y in self.graph.nodes(data=True)
                                if 'label' in y.keys() and y['label'] == HyperEdge.B.name]
        for id in hyperedges_to_remove:
            self.graph.remove_node(id)

        hyperedge = [(x, y) for x, y in self.graph.nodes(data=True)
                     if 'label' in y.keys() and y['label'] == HyperEdge.I.name][0]
        self.graph.add_node(hyperedge[0], **hyperedge[1])
        return hyperedge

    def __prepare_multi_hyperedge(self):
        width, height = self.image.size
        P1(self.graph, x_max_idx=width - 1, y_max_idx=height - 1, image=self.image)
        i_hyperedges_ids = self.__hyperedges_ids(HyperEdge.I)
        P5(self.graph, i_hyperedges_ids[0], self.image)
        P2(self.graph, i_hyperedges_ids[0], self.image)
