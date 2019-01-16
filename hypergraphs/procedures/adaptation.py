import networkx as nx
from PIL import Image

from productions import Direction, P2, P3
from utils import get_node_id


def calculate_aproximation_error():
    # THIS FUNCTION WILL BE PROVIDED BY TEAM MAKING TASK 14, MOCKED TO RETURN VALUE 0.1
    return 0.1


def P4():
    # THIS FUNCTION WILL BE PROVIDED BY OTHER TEAM
    pass


def P5():
    # THIS FUNCTION WILL BE PROVIDED BY OTHER TEAM
    pass


def P6():
    # THIS FUNCTION WILL BE PROVIDED BY OTHER TEAM
    pass


def mark_hyperedges_for_adaptation(graph: nx.Graph, epsilon: int, image: Image):
    hyperedges = [(id, node_data) for id, node_data in graph.nodes(data=True) if node_data['is_hyperedge']]
    I_hyperedges = [(id, node_data) for id, node_data in hyperedges if node_data['label'] == 'I']
    B_hyperedges = [(id, node_data) for id, node_data in hyperedges if node_data['label'] == 'B']
    F_hyperedges = [(id, node_data) for id, node_data in hyperedges if node_data['label'] in Direction]

    # Iterate I edges
    for edge_id, edge_data in I_hyperedges:
        if calculate_aproximation_error() > epsilon:
            P5()
            P6()

    # Iterate I edges
    for edge_id, edge_data in I_hyperedges:
        P2(graph, edge_id, image)

    # Iterate B edges
    for edge_id, edge_data in B_hyperedges:
        # B should have two neighbors
        v1, v2 = graph.neighbors(edge_id)
        I_neigh1 = [e for e in graph.neighbors(v1) if graph.nodes[e]['label'] == 'I']
        I_neigh2 = [e for e in graph.neighbors(v2) if graph.nodes[e]['label'] == 'I']
        I1 = None
        I2 = None
        F = None
        for i1 in I_neigh1:
            for i2 in I_neigh2:
                common_neighbors = [v for v in graph.neighbors(i1) if v in graph.neighbors(i2)]
                if len(common_neighbors) == 1:
                    v = common_neighbors[0]
                    I1 = i1
                    I2 = i2
                    F = next(e for e in graph.neighbors(v) if graph.nodes[e]['label'] in Direction)
                    break

        P3(graph, edge_id, [I1, I2], F, image)

    # Iterate F edges
    for edge_id, edge_data in F_hyperedges:
        P4()
