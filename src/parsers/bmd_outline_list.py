from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, get_scale

def read_bmd_outline_list(file: BinaryIO):
    version = int2(file)  # version
    # print(version)
    assert int4(file) == 0, "BMD_OUTLINE_LIST has items"
