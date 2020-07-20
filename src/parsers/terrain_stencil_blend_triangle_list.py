from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8


def read_terrain_stencil_blend_triangle_list(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "TERRAIN_STENCIL_BLEND_TRIANGLE_LIST has items"