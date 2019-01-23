import networkx as nx
from PIL.Image import Image

from hypergraphs.productions.p6 import P6
from hypergraphs.utils import HyperEdge


def P5(graph: nx.Graph, hyperedge_id, image: Image):
    __check_conditions(graph, hyperedge_id)
    if graph.node[hyperedge_id]['should_break'] is 0:
        graph.node[hyperedge_id]['should_break'] = 1
        P6(graph, hyperedge_id, image)


def __check_conditions(graph, hyperedge_id):
    if not graph.node[hyperedge_id]['is_hyperedge']:
        raise ValueError('Given node_id is not id of hyperedge')
    if graph.node[hyperedge_id]['label'] is not HyperEdge.I.name:
        raise ValueError('Given hyperedge label is not I')
