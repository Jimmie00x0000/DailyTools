import math
import numpy as np
from plyfile import PlyData, PlyElement
from random import *


def _gen_noise(noise_range):
    r = np.random.randn()
    x = noise_range * r
    r = np.random.randn()
    y = noise_range * r
    r = np.random.randn()
    z = noise_range * r
    return x, y, z


def read_ply(file_name):
    """
    读取 Ply
    :param file_name: 文件名
    :return: 返回顶点数据和面数据
    """
    ply_data = PlyData.read(file_name)
    vertex_data_ = None
    face_data_ = None
    for element in ply_data.elements:
        if element.name == 'vertex' or element.name == 'vertices':
            vertex_data_ = element.data
        elif element.name == 'face' or element.name == 'faces':
            face_data_ = element.data
            pass
        pass
    if vertex_data_ is None or face_data_ is None:
        print('no face data, exit')
        exit(-1)
    return vertex_data_, face_data_


def _gen_noisy_data(vertex_data, face_data):
    point_cloud = []
    for face in face_data:
        face = face[0]
        point_cloud += _gen_noisy_face(vertex_data, face)
    return point_cloud


# 采样分辨率，越小，点云越密
_RESOLUTION = 0.0005
# _RESOLUTION = 0.005


def length_of_vector(triple):
    return math.sqrt(triple[0] * triple[0] + triple[1] * triple[1] + triple[2] * triple[2])


# 计算向量叉积
def cross(v1, v2):
    return (
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0])


def _gen_noisy_face(vertex_data, face_vert_indices):
    if len(face_vert_indices) < 3:
        return []
    if len(face_vert_indices) > 3:
        vert_indices_res = list(face_vert_indices[0:1]) + list(face_vert_indices[2:])
        return _gen_noisy_face(vertex_data, face_vert_indices[:3]) \
               + _gen_noisy_face(vertex_data, vert_indices_res)
    points = []
    a = vertex_data[face_vert_indices[0]]
    b = vertex_data[face_vert_indices[1]]
    c = vertex_data[face_vert_indices[2]]
    ab = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    ac = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
    # 三角形参数方程：p = OA + u·AB + v·AC, u + v <= 1
    num = int(length_of_vector(cross(ab, ac)) * 0.5 / _RESOLUTION)
    r = Random()
    count = 0
    while count < num:
        u = r.random()
        v = r.random()
        if u + v > 1:
            continue
        pass
        noise = _gen_noise(_RESOLUTION * 0.25)
        point = (
            a[0] + ab[0] * u + ac[0] * v + noise[0],
            a[1] + ab[1] * u + ac[1] * v + noise[1],
            a[2] + ab[2] * u + ac[2] * v + noise[2]
        )
        points.append(point)
        count += 1
        pass
    return points


def _write_ply(point_cloud, file_name):
    pc_np_array = np.array(point_cloud, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    vertex_ele = PlyElement.describe(pc_np_array, 'vertex')
    PlyData([vertex_ele], text=True).write(file_name)
    pass



if __name__ == '__main__':
    """
    读取一个 Ply 文件，生成带有噪声的点云
    """
    file_name = './cube.ply'
    vertex_data, face_data = read_ply(file_name)
    pc = _gen_noisy_data(vertex_data, face_data)
    _write_ply(pc, file_name[:-3] + "pc.ply")
    pass
