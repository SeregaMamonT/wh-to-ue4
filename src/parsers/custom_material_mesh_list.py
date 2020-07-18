from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

from wh_binary_objects import CustomMaterialMesh, Point3D


def read_custom_material_mesh(file):
    custom_material_mesh = CustomMaterialMesh()
    vertices_amount = int4(file)
    custom_material_mesh.vertices = []
    for i in range(vertices_amount):
        vertex = Point3D(float4(file), float4(file), float4(file))
        custom_material_mesh.vertices.append(vertex)
    indices_amount = int4(file)
    custom_material_mesh.indices = []
    for i in range(indices_amount):
        custom_material_mesh.indices.append(int2(file))
    # for i in custom_material_mesh.vertices:
        # print(i.__dict__)
    custom_material_mesh.material = string(file)
    custom_material_mesh.height_mode = string(file)

    return custom_material_mesh


def read_custom_material_mesh_list(file: BinaryIO):
    version = int2(file)  # version
    custom_material_mesh_list_amount = int4(file)
    custom_material_mesh_list = []
    for i in range(custom_material_mesh_list_amount):
        custom_material_mesh_version = int2(file)
        custom_material_mesh_list.append(read_custom_material_mesh(file))

    return custom_material_mesh_list
