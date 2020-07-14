from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale


def read_custom_material_mesh_list(file: BinaryIO):
    version = int2(file)  # version
    custom_material_mesh_list_amount = int4(file)
    # print('Version: ', version, custom_material_mesh_list_amount)
    for i in range(custom_material_mesh_list_amount):
        custom_material_mesh_version = int2(file)
        vertices_amount = int4(file)
        vertex_list = []
        for j in range(vertices_amount):
            t = (float4(file), float4(file), float4(file))
            vertex_list.append(t)
        # print(vertex_list)
        indices_amount = int4(file)
        indices_list = []
        for j in range(indices_amount):
            indices_list.append(int2(file))
        # print(indices_list)
        material = string(file)
        # print(material)
        height_mode = string(file)

    # assert int4(file) == 0, "CUSTOM_MATERIAL_MESH_LIST has items"