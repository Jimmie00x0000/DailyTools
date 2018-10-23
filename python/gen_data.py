import math
import numpy as np


def _gen_noise(noise_range):
    r = np.random.randn()
    x = noise_range * r
    r = np.random.randn()
    y = noise_range * r
    return x, y


def _gen_impl(radian_start, radian_range, point_count=500, radius=1, z=0):
    result = []
    noise_range = radius * 0.03
    for point_index in range(point_count):
        noise = _gen_noise(noise_range)
        x = radius * math.cos(radian_start + radian_range * (point_index / point_count)) + noise[0]
        y = radius * math.sin(radian_start + radian_range * (point_index / point_count)) + noise[1]
        result.append((x, y, z))
        pass
    return result


def _write_txt(data, file_name):
    file_handler = open(file_name, 'w')
    for x_y_z in data:
        file_handler.write('%.5f %.5f %.5f\n' % (x_y_z[0], x_y_z[1], x_y_z[2]))
    file_handler.close()
    pass


if __name__ == '__main__':
    """
    指定一段 xoy 平面上的圆弧和 z 坐标，生成一小段测试点云。
    """
    points = _gen_impl(math.pi * 2 / 3, math.pi * 0.6)
    _write_txt(points, 'test_data.txt')
    pass
