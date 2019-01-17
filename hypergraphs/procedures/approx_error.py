import utils
from PIL import Image

from utils import get_common_nodes


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
                r1, g1, b1 = node['r'], node['g'], node['b']
            else:
                r2, g2, b2 = node['r'], node['g'], node['b']
        else:
            if node['y'] == y1:
                r4, g4, b4 = node['r'], node['g'], node['b']
            else:
                r3, g3, b3 = node['r'], node['g'], node['b']

    if r1 == -1:
        r1, g1, b1 = utils.APPROX_R[y1][x1], utils.APPROX_G[y1][x1], utils.APPROX_B[y1][x1]
    if r2 == -1:
        r2, g2, b2 = utils.APPROX_R[y2][x1], utils.APPROX_G[y2][x1], utils.APPROX_B[y2][x1]
    if r3 == -1:
        r3, g3, b3 = utils.APPROX_R[y2][x2], utils.APPROX_G[y2][x2], utils.APPROX_B[y2][x2]
    if r4 == -1:
        r4, g4, b4 = utils.APPROX_R[y1][x2], utils.APPROX_G[y1][x2], utils.APPROX_B[y1][x2]

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

            diff_r[py][px] = bitmap_r
            diff_g[py][px] = bitmap_g
            diff_b[py][px] = bitmap_b

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

            diff_r[py][px] -= r1 * mul_x_div_y + r2 * div_x_div_y + r3 * mul_x_mul_y + r4 * div_x_mul_y
            diff_g[py][px] -= g1 * mul_x_div_y + g2 * div_x_div_y + g3 * mul_x_mul_y + g4 * div_x_mul_y
            diff_b[py][px] -= b1 * mul_x_div_y + b2 * div_x_div_y + b3 * mul_x_mul_y + b4 * div_x_mul_y

    self.error = 0

    for px in range(x1, x2 + 1):
        for py in range(y1, y2 + 1):
            self.error += 0.5 * (diff_r[py][px]) ** 2 \
                          + 0.3 * (diff_g[py][px]) ** 2 \
                          + 0.2 * (diff_b[py][px]) ** 2

    return round(self.error, 16)
