import networkx as nx
from PIL import Image

from hypergraphs.productions import Direction, P2
from hypergraphs.utils import get_node_id


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
        # TODO We have to extract B node, two I nodes and one V node for given B node id, please refer to task docs,
        # TODO just take a look at the picture and you will know what to use in P3 production. The question is how
        # TODO to determine the proper nodes to pass in P3. There is possible error in P2.
        # B should have two neighbors
        b_neighbors = [graph.node[v] for v in graph.neighbors(edge_id)]
        v_neighbor_position = (b_neighbors[0]['x'] + b_neighbors[1]['x']) // 2, (
                b_neighbors[0]['y'] + b_neighbors[1]['y']) // 2
        v_id = get_node_id(v_neighbor_position)
        # P3(graph, ,edge_id, ,image)
        pass

    # Iterate F edges
    for edge_id, edge_data in F_hyperedges:
        P4()
