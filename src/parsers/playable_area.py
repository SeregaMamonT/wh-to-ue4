from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale


def read_playable_area(file: BinaryIO):
    version = int2(file)  # version
    # print('Version: ', version)
    min_x = float4(file)
    min_y = float4(file)
    max_x = float4(file)
    max_y = float4(file)
    # print(min_x, min_y, max_x, max_y)
    has_been_set = bool1(file)
    valid_location_flags_version = int2(file)
    valid_north = bool1(file)
    valid_south = bool1(file)
    valid_east = bool1(file)
    valid_west = bool1(file)
    # print(valid_location_flags_version, valid_north, valid_south, valid_east, valid_west)
    # assert int4(file) == 0, "PLAYABLE_AREA has items"