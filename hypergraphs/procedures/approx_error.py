from PIL import Image

from utils import get_common_nodes

APPROX_R = None
APPROX_G = None
APPROX_B = None


def approx_error(self, image: Image, graph, i_hyperedge_id):
    common_nodes_ids = get_common_nodes(graph, i_hyperedge_id)
    x1, x2, y1, y2 = -1, -1, -1, -1
    r1, g1, b1, r2, g2, b2, r3, g3, b3, r4, g4, b4 = -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1

    if len(common_nodes_ids) < 2 or len(common_nodes_ids) > 4:
        raise ValueError('in ApproxError: Invalid graph representation! I hyperedge has connected only 1 common node!')
    else:
        x_arr = sorted(set(map(lambda node_id: graph.node[node_id]['x'], common_nodes_ids)))
        y_arr = sorted(set(map(lambda node_id: graph.node[node_id]['y'], common_nodes_ids)))

        if len(x_arr) != 2 or len(y_arr) != 2:
            raise ValueError('in ApproxError: Invalid graph representation! Nodes are not orthogonal to each other!')

        x1, x2 = x_arr
        y1, y2 = y_arr

    for node_id in common_nodes_ids:
        node = graph.node[node_id]
        if node['x'] == x1:
            if node['y'] == y1:
                r3, g3, b3 = node['r'], node['g'], node['b']
            else:
                r1, g1, b1 = node['r'], node['g'], node['b']
        else:
            if node['y'] == y1:
                r4, g4, b4 = node['r'], node['g'], node['b']
            else:
                r2, g2, b2 = node['r'], node['g'], node['b']

    if x1 == -1:
        if y1 == -1:
            r3, g3, b3 = APPROX_R[x1, y1], APPROX_G[x1, y1], APPROX_B[x1, y1]
        elif y2 == -1:
            r1, g1, b1 = APPROX_R[x1, y2], APPROX_G[x1, y2], APPROX_B[x1, y2]
    elif x2 == -1:
        if y1 == -1:
            r4, g4, b4 = APPROX_R[x2, y1], APPROX_G[x2, y1], APPROX_B[x2, y1]
        elif y2 == -1:
            r2, g2, b2 = APPROX_R[x2, y2], APPROX_G[x2, y2], APPROX_B[x2, y2]

    if [x1, y1, x2, y2, r1, g1, b1, r2, g2, b2, r3, g3, b3, r4, g4, b4].__contains__(-1):
        raise ValueError('in ApproxError: variables x1..y2, r1..b4 contain wrong values')

    diff_r, diff_g, diff_b = [], [], []

    init_tmp = []
    for _ in range(x1, x2 + 1):
        init_tmp.append(0.0)

    for _ in range(y1, y2 + 1):
        diff_r.append(init_tmp.copy())
        diff_g.append(init_tmp.copy())
        diff_b.append(init_tmp.copy())

    for px in range(x1, x2 + 1):
        for py in range(y1, y2 + 1):
            img = image.convert('RGB')
            bitmap_r, bitmap_g, bitmap_b = img.getpixel((px, py))

            diff_r[px][py] = bitmap_r
            diff_g[px][py] = bitmap_g
            diff_b[px][py] = bitmap_b

    for px in range(x1, x2 + 1):
        for py in range(y1, y2 + 1):
            div_x = (px - x1) / (x2 - x1)
            div_y = (py - y1) / (y2 - y1)
            mul_x = (1 - div_x)
            mul_y = (1 - div_y)
            mul_x_div_y = mul_x * div_y
            div_x_div_y = div_x * div_y
            mul_x_mul_y = mul_x * mul_y
            div_x_mul_y = div_x * mul_y

            diff_r[px][py] -= r1 * mul_x_div_y + r2 * div_x_div_y + r3 * mul_x_mul_y + r4 * div_x_mul_y
            diff_g[px][py] -= g1 * mul_x_div_y + g2 * div_x_div_y + g3 * mul_x_mul_y + g4 * div_x_mul_y
            diff_b[px][py] -= b1 * mul_x_div_y + b2 * div_x_div_y + b3 * mul_x_mul_y + b4 * div_x_mul_y

    self.error = 0

    for px in range(x1, x2 + 1):
        for py in range(y1, y2 + 1):
            self.error += 0.5 * (diff_r[px][py]) ** 2 \
                          + 0.3 * (diff_g[px][py]) ** 2 \
                          + 0.2 * (diff_b[px][py]) ** 2

    return round(self.error, 16)
