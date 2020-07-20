from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8


def read_lite_building_outlines(file: BinaryIO):
    assert int4(file) == 0, "LITE_BUILDING_OUTLINES has items"