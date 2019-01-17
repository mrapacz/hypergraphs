import networkx as nx
from PIL import Image

from plot import plot
from procedures.approx_error import approx_error
from productions import P2, P3, P5, P6, P4, P3AutoDetect
from utils import get_node_id, Direction


def calculate_aproximation_error():
    # THIS FUNCTION WILL BE PROVIDED BY TEAM MAKING TASK 14, MOCKED TO RETURN VALUE 0.1
    return 0.1


def mark_hyperedges_for_adaptation(graph: nx.Graph, epsilon: int, image: Image):
    for _ in range(3):
        hyperedges = [(id, node_data) for id, node_data in graph.nodes(data=True) if node_data['is_hyperedge']]
        I_hyperedges = [(id, node_data) for id, node_data in hyperedges if node_data['label'] == 'I']
        B_hyperedges = [(id, node_data) for id, node_data in hyperedges if node_data['label'] == 'B']
        F_hyperedges = [(id, node_data) for id, node_data in hyperedges if node_data['label'] in Direction]

        # Iterate I edges
        for edge_id, edge_data in I_hyperedges:
            # if approx_error(image, graph, edge_id) > epsilon:
            P5(graph, edge_id, image)
            # P6(graph, edge_id, image)

        # Iterate I edges
        for edge_id, edge_data in I_hyperedges:
            P2(graph, edge_id, image)

        # Iterate B edges
        for edge_id, edge_data in B_hyperedges:
            # B should have two neighbors
            P3AutoDetect(graph, edge_id, image)

        # Iterate F edges
        for edge_id, edge_data in F_hyperedges:
            P4(graph, edge_id, image)

        plot(graph)
