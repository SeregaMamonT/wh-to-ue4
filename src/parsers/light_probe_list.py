from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale


def read_light_probe_list(file: BinaryIO):
    version = int2(file)  # version
    amount = int4(file)
    # print('Lightprobe: ', version, amount)
    for i in range(amount):
        light_probe_version = int2(file)
        t = (float4(file), float4(file), float4(file))
        radius = float4(file)
        is_primary = bool1(file)
        height_mode = string(file)
        # print(t, radius, is_primary, height_mode)
    # assert int4(file) == 0, "LIGHT_PROBE_LIST has items"