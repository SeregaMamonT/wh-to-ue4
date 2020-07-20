from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, get_scale, unscale

def read_ef_line_list(file: BinaryIO):
    assert int4(file) == 0, "EF_LINE_LIST has items"