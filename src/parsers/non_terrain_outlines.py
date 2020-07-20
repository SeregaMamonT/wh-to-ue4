from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, get_scale, unscale

from wh_binary_objects import Outline, Point2D

def read_otline(file):
    point_amount = int4(file)
    outline = Outline()
    outline.points = []
    for i in range(point_amount):
        point = Point2D(float4(file), float4(file))
        outline.points.append(point)

    return outline


def read_non_terrain_outlines(file: BinaryIO):
    outlines_amount = int4(file)
    outlines = []
    capture_locations_set = []
    for i in range(outlines_amount):
        outlines.append(read_otline(file))

    return outlines