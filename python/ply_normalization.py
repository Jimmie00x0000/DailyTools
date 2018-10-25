from plyfile import PlyData, PlyElement
import math
import numpy as np


def _bounding_box(data):
    x_min, y_min, z_min = math.inf, math.inf, math.inf
    x_max, y_max, z_max = - math.inf, - math.inf, - math.inf
    xs = data['x']
    ys = data['y']
    zs = data['z']
    for x in xs:
        x_min = min((x_min, x))
        x_max = max((x_max, x))
    for y in ys:
        y_min = min((y_min, y))
        y_max = max((y_max, y))
    for z in zs:
        z_min = min((z_min, z))
        z_max = max((z_max, z))
    return x_min, x_max, y_min, y_max, z_min, z_max


def _normalize_impl(bbox, vertex_data):
    largest_length = max((bbox[1] - bbox[0], bbox[3] - bbox[2], bbox[5] - bbox[4]))
    ratio = largest_length / 1.0
    vertex_data = vertex_data.tolist()
    for i in range(len(vertex_data)):
        xyz = vertex_data[i]
        new_xyz = (xyz[0] / ratio, xyz[1] / ratio, xyz[2] / ratio)
        vertex_data[i] = new_xyz
        pass
    return np.array(vertex_data, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])


def normalize(file_name):
    ply_data = PlyData.read(file_name)
    for element in ply_data.elements:
        if element.name == 'vertex' or element.name == 'vertices':
            vertex_data = element.data
            bbox = _bounding_box(vertex_data)
            new_vertex_data = _normalize_impl(bbox, vertex_data)
            _write_ply(file_name[:-4] + '.n.ply', new_vertex_data)
            pass
        pass
    pass


def _write_ply(file_name, vertex_data):
    vertex_ele = PlyElement.describe(vertex_data, 'vertex')
    PlyData([vertex_ele], text=True).write(file_name)
    pass


if __name__ == '__main__':
    # normalize('simple.ply')
    pass
