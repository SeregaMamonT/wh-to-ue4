from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

from wh_binary_objects import AiHint, Polygone, PolyLine, PolyLineList, Point2D



def read_polyline(file):
    polyline = PolyLine
    version = int2(file)
    polyline.type = string(file)
    points_amount = int4(file)
    polyline.points = []
    for i in range(points_amount):
        point = Point2D(float4(file), float4(file))
        polyline.points.append(point)

    return polyline


def read_polygone(file):
    polygone = Polygone
    polygone.points_amount = int4(file)
    polygone.points = []
    for i in range(polygone.points_amount):
        point = Point2D(float4(file), float4(file))
        polygone.points.append(point)

    return polygone

def read_ai_hints(file: BinaryIO):
    version = int2(file)  # version
    # print('Version: ', version)
    ai_hints = AiHint()

    ai_hints.separators = []

    # separators
    separators_version = int2(file)
    separators_amount = int4(file)
    for i in range(separators_amount):
        ai_hints.separators.append(read_polyline(file))

    # directed_points
    directed_points_version = int2(file)
    directed_points_amount = int4(file)

    # polylines
    polylines_version = int2(file)
    polylines_amount = int4(file)

    polylines = []
    ai_hints.polylines = []
    for i in range(polylines_amount):
        ai_hints.polylines.append(read_polyline(file))


    # polylines list

    polylines_list_version = int2(file)
    polylines_list_amount = int4(file)

    ai_hints.polylines_list_list = []
    for i in range(polylines_list_amount):
        poly_lines_list = PolyLineList()

        hint_polylines_version = int2(file)
        poly_lines_list.type = string(file)
        polygons_amount = int4(file)
        poly_lines_list.polygons = []
        for j in range(polygons_amount):
            poly_lines_list.polygons.append(read_polygone(file))

    return ai_hints