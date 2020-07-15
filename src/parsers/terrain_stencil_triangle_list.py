from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

from wh_binary_objects import TerrainStencilTriangle


def read_terrain_stencil_triangle(file):
    terrain_stencil_triangle = TerrainStencilTriangle()
    terrain_stencil_triangle.position1 = (float4(file), float4(file), float4(file))
    terrain_stencil_triangle.position2 = (float4(file), float4(file), float4(file))
    terrain_stencil_triangle.position3 = (float4(file), float4(file), float4(file))
    terrain_stencil_triangle.height_mode = string(file)

    return terrain_stencil_triangle


def read_terrain_stencil_triangle_list(file: BinaryIO):
    version = int2(file)  # version
    amount = int4(file)
    terrain_stencil_triangle_list = []
    for i in range(amount):
        terrain_stencil_triangle_version = int2(file)
        terrain_stencil_triangle_list.append(read_terrain_stencil_triangle(file))

    return terrain_stencil_triangle_list