from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale


def read_deployment_list(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "DEPLOYMENT_LIST has items"