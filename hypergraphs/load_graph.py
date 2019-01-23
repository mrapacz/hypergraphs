from productions import P1, P2, P3AutoDetect, P4, P5
from utils import get_node_id
from typing import TextIO, Tuple
from types import SimpleNamespace
from unittest.mock import Mock

import networkx as nx


def load_graph(file: TextIO) -> nx.Graph:
    graph = nx.Graph()

    for prod_sign in __read_production(file):
        __execute_production(graph, prod_sign[0], *prod_sign[1])

    return graph


def __read_production(stream: TextIO) -> Tuple:
    while True:
        try:
            prod_num = int(stream.readline())
        except ValueError:
            return

        attributes = stream.readline().split(',')
        if not attributes:
            return

        if prod_num not in range(1, 6):
            raise ValueError('Invalid production number: {}'.format(prod_num))

        yield prod_num, map(lambda arg: int(arg), attributes)


def __execute_production(graph: nx.Graph, prod_num: int, *args):
    if prod_num == 1:
        x_max, y_max, r1, g1, b1, r2, g2, b2, r3, g3, b3, r4, g4, b4 = args

        def sample(pixel):
            if pixel == (0, y_max):
                return r1, g1, b1
            elif pixel == (x_max, y_max):
                return r2, g2, b2
            elif pixel == (0, 0):
                return r3, g3, b3
            elif pixel == (x_max, 0):
                return r4, g4, b4

        image = SimpleNamespace()
        image.getpixel = Mock(side_effect=sample)

        P1(graph, x_max, y_max, image)

    elif prod_num == 2:
        x1, y1, x2, y2, r, g, b = args

        image = SimpleNamespace()
        image.getpixel = Mock(return_value=(r, g, b))

        hyperedge = next(__get_common_hyperedges(graph, get_node_id((x1, y1)), get_node_id((x2, y2))))

        P2(graph, hyperedge, image)

    elif prod_num == 3:
        x1, y1, x2, y2, r, g, b = args

        image = SimpleNamespace()
        image.getpixel = Mock(return_value=(r, g, b))

        hyperedge = next(__get_common_hyperedges(graph, get_node_id((x1, y1)), get_node_id((x2, y2))))

        P3AutoDetect(graph, hyperedge, image)

    elif prod_num == 4:
        x1, y1, x2, y2, r, g, b = args

        image = SimpleNamespace()
        image.getpixel = Mock(return_value=(r, g, b))

        hyperedge = next(__get_common_hyperedges(graph, get_node_id((x1, y1)), get_node_id((x2, y2))))

        P4(graph, hyperedge, image)

    elif prod_num == 5:
        x1, y1, x2, y2 = args

        hyperedge = next(__get_common_hyperedges(graph, get_node_id((x1, y1)), get_node_id((x2, y2))))

        P5(graph, hyperedge, None)


def __get_common_hyperedges(graph, v1, v2):
    return (e for e in graph[v1] if e in graph[v2])
