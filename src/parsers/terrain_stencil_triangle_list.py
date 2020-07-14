from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale


def read_terrain_stencil_triangle_list(file: BinaryIO):
    version = int2(file)  # version
    terrain_stencil_triangles = int4(file)
    for i in range(terrain_stencil_triangles):
        terrain_stencil_triangle_version = int2(file)
        position0 = (float4(file), float4(file), float4(file))
        position1 = (float4(file), float4(file), float4(file))
        position2 = (float4(file), float4(file), float4(file))
        height_mode = string(file)
        # print(terrain_stencil_triangle_version, position0, position1, position2, height_mode)

    # assert int4(file) == 0, "TERRAIN_STENCIL_TRIANGLE_LIST has items"