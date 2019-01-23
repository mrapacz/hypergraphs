import uuid

import networkx as nx
from PIL.Image import Image

from hypergraphs.utils import get_node_id, Direction


# hyp_b - B labeled hyperedge id
# hyp_is - I labeled hyperedge_ids
# hyp_f - F labeled hyperedge_id

def P3AutoDetect(graph, hyp_b, image):
    hyp_b_data = graph.node[hyp_b]
    b_neighbour_ids = list(graph.neighbors(hyp_b))

    graph.remove_node(hyp_b)

    path = nx.shortest_path(graph, b_neighbour_ids[0], b_neighbour_ids[1])

    if len(path) != 5:
        raise ValueError(f"P3AutoDetect - wrong number of nodes in path {len(path)}")

    graph.add_node(hyp_b, **hyp_b_data)
    graph.add_edge(hyp_b, b_neighbour_ids[0])
    graph.add_edge(hyp_b, b_neighbour_ids[1])

    hyp_is = [x for x in path if 'label' in graph.node[x] and graph.node[x]['label'] == 'I']

    common_i_node = list(set(graph.neighbors(hyp_is[0])) & set(graph.neighbors(hyp_is[1])))[0]

    common_i_node_neighbours = list(graph.neighbors(common_i_node))

    hyp_fs = []
    for x in common_i_node_neighbours:
        data = graph.node[x]
        if 'label' in data and data['label'] in map(lambda x: x.name, list(Direction)):
            hyp_fs.append(x)

    done = False
    for hyp_f in hyp_fs:
        try:
            P3(graph, hyp_b, hyp_is, hyp_f, image)
            done = True
            break
        except ValueError:
            print("P3AutoDetect - ValueError handled!")

    if not done:
        raise ValueError('P3AutoDetect - ValueError not handled')



def P3(graph: nx.Graph, hyp_b, hyp_is, hyp_f, image: Image):
    __assert_hyper_edge(graph, [hyp_b], 'B')
    __assert_hyper_edge(graph, hyp_is, 'I')
    __assert_hyper_edge(graph, [hyp_f])

    hyp_f_data = graph.node[hyp_f]
    hyp_b_data = graph.node[hyp_b]

    hyp_f_neighbour_ids = list(graph.neighbors(hyp_f))

    if len(hyp_f_neighbour_ids) != 1:
        raise ValueError('F should have 1 neighbour')

    for hyp_i in hyp_is:
        if hyp_f_neighbour_ids[0] not in list(graph.neighbors(hyp_i)):
            raise ValueError('I is not connected with F1 via neighbour')

    hyp_f_neighbour_data = graph.node[hyp_f_neighbour_ids[0]]

    if hyp_f_data['label'] == Direction.N.name:
        if hyp_f_data['x'] != hyp_f_neighbour_data['x'] or hyp_f_data['y'] <= hyp_f_neighbour_data['y']:
            raise ValueError('F hyperedge has weird position')
        if hyp_f_data['x'] != hyp_b_data['x'] or hyp_f_data['y'] >= hyp_b_data['y']:
            raise ValueError('F hyperedge has weird position (B)')
    elif hyp_f_data['label'] == Direction.S.name:
        if hyp_f_data['x'] != hyp_f_neighbour_data['x'] or hyp_f_data['y'] >= hyp_f_neighbour_data['y']:
            raise ValueError('F hyperedge has weird position')
        if hyp_f_data['x'] != hyp_b_data['x'] or hyp_f_data['y'] <= hyp_b_data['y']:
            raise ValueError('F hyperedge has weird position (B)')
    elif hyp_f_data['label'] == Direction.E.name:
        if hyp_f_data['x'] <= hyp_f_neighbour_data['x'] or hyp_f_data['y'] != hyp_f_neighbour_data['y']:
            raise ValueError('F hyperedge has weird position')
        if hyp_f_data['x'] >= hyp_b_data['x'] or hyp_f_data['y'] != hyp_b_data['y']:
            raise ValueError('F hyperedge has weird position (B)')
    elif hyp_f_data['label'] == Direction.W.name:
        if hyp_f_data['x'] >= hyp_f_neighbour_data['x'] or hyp_f_data['y'] != hyp_f_neighbour_data['y']:
            raise ValueError('F hyperedge has weird position')
        if hyp_f_data['x'] <= hyp_b_data['x'] or hyp_f_data['y'] != hyp_b_data['y']:
            raise ValueError('F hyperedge has weird position (B)')
    else:
        raise ValueError('F hyperedge has weird label')


    new_node_position = (hyp_b_data['x'], hyp_b_data['y'])
    new_node_id = get_node_id(new_node_position)

    __add_new_node(graph, image, new_node_id, new_node_position) # add v
    __add_hyperedges_between_neighbour_nodes(graph, hyp_b, new_node_id, new_node_position) # add 1-b-v-b-2
    for hyp_i in hyp_is:
        __add_edges_between_nodes(graph, new_node_id, hyp_i) # add v-i and v-i
    __add_edges_between_nodes(graph, new_node_id, hyp_f) # add v-f1
    graph.remove_node(hyp_b)


def __assert_hyper_edge(graph, hyperedge_ids, label=None):
    for hyperedge_id in hyperedge_ids:
        if not hyperedge_id in graph.nodes:
            raise ValueError('Given node_id do not exists')

        if not graph.node[hyperedge_id]['is_hyperedge']:
            raise ValueError('Given node_id is not id of hyperedge')

        if label:
            if not graph.node[hyperedge_id]['label'] is label:
                raise ValueError(f"Given node_id is not hyperedge type '{label}'")


def __add_new_node(graph, image, new_node_id, new_node_position):
    new_node_rgb = image.getpixel(new_node_position)
    graph.add_node(
        new_node_id,
        x=new_node_position[0],
        y=new_node_position[1],
        is_hyperedge=False,
        r=new_node_rgb[0],
        g=new_node_rgb[1],
        b=new_node_rgb[2],
    )


def __add_hyperedges_between_neighbour_nodes(graph, hyperedge_id, new_node_id, new_node_position):
    hyperedge_neighbour_ids = graph.neighbors(hyperedge_id)
    for neighbour_id in hyperedge_neighbour_ids:
        neighbour = graph.node[neighbour_id]
        new_hyperedge_id = uuid.uuid4()
        graph.add_node(
            new_hyperedge_id,
            x=(neighbour['x'] + new_node_position[0]) // 2,
            y=(neighbour['y'] + new_node_position[1]) // 2,
            is_hyperedge=True,
            label='B',
        )
        graph.add_edge(new_hyperedge_id, neighbour_id)
        graph.add_edge(new_hyperedge_id, new_node_id)


def __add_edges_between_nodes(graph, node1, node2):
    graph.add_edge(node1, node2)
