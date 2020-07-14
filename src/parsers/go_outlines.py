from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

def read_go_outlines(file: BinaryIO):
    regions_amount = int4(file)
    # print('Go outlines: ', regions_amount)
    for i in range(regions_amount):
        point_amount = int4(file)
        points_list = []
        for j in range(point_amount):
            t = (float4(file), float4(file))
            points_list.append(t)
        # print(points_list)

    # assert int4(file) == 0, "GO_OUTLINES has items"