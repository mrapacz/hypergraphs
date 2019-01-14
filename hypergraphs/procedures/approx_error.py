from PIL import Image


def approx_error(self, image: Image, x1, x2, y1, y2, r1, g1, b1, r2, g2, b2, r3, g3, b3, r4, g4, b4):
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
