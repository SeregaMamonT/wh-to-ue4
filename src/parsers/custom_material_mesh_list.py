from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8

from wh_binary_objects import CustomMaterialMesh, Point3D

from version_holder import VersionHolder


def read_custom_material_mesh_list(file: BinaryIO):
    assert_version('CUSTOM_MATERIAL_MESH_LIST', 1, int2(file))
    return read_list(file, read_custom_material_mesh)


def read_custom_material_mesh(file):
    custom_material_mesh_version = int2(file)
    return custom_material_mesh_versions.get_reader(custom_material_mesh_version)(file)


def read_custom_material_mesh_v2(file):
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
    custom_material_mesh.material = string(file)
    custom_material_mesh.height_mode = string(file)

    return custom_material_mesh


custom_material_mesh_versions = VersionHolder('Custom material mesh', {
    2: read_custom_material_mesh_v2,
})

