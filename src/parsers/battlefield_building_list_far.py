from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8


def read_building_list_far(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "BATTLEFIELD_BUILDING_LIST_FAR has items"