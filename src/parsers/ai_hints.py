from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale


def read_ai_hints(file: BinaryIO):
    version = int2(file)  # version
    # print('Version: ', version)

    # separators
    separators_version = int2(file)
    separators_amount = int4(file)
    # print('Separators: ', separators_version, separators_amount)

    # directed_points
    directed_points_version = int2(file)
    directed_points_amount = int4(file)
    # print('Directed points: ', directed_points_version, directed_points_amount)

    # polylines
    polylines_version = int2(file)
    polylines_amount = int4(file)
    # print('Polylines: ', polylines_version, polylines_amount)
    for i in range(polylines_amount):
        polyline_version = int2(file)
        polyline_type = string(file)
        # print(polyline_version, polyline_type)
        polyline_points_amount = int4(file)
        polyline_points_list = []
        for j in range(polyline_points_amount):
            t = (float4(file), float4(file))
            polyline_points_list.append(t)
        # print(polyline_points_list)
    polylines_list_version = int2(file)
    polylines_list_amount = int4(file)
    # print('Polylines list: ', polylines_list_version, polylines_list_amount)
    # assert int4(file) == 0, "AI_HINTS has items"