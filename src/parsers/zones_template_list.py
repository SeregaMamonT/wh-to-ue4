from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, get_scale, \
    read_transform_n_x_m

from wh_binary_objects import ZoneTemplate, Point2D, Outline

from app_typing import Matrix, Vector


def read_zones_template_list(file: BinaryIO):
    assert_version('ZONES_TEMPLATE_LIST', 1, int2(file))

    return read_list(file, read_zone_template)


def read_zone_template(file):
    zone_template = ZoneTemplate()
    points_amount = int4(file)
    zone_template.outline = Outline()
    zone_template.outline.points = Outline.points = []
    for i in range(points_amount):
        zone_template.outline.points.append(Point2D(float4(file), float4(file)))


    # <zone_name> <entity_formation_template name=''> and <lines/>
    file.read(8)
    # transformation matrix
    zone_template.transformation = read_transform_n_x_m(file, 4, 4)

    return zone_template


# def read_zones_template_list(file: BinaryIO):
#     version = int2(file)  # version
#     zones_amount = int4(file)
#     zones = []
#     for i in range(zones_amount):
#         # read_zone_template(file)
#         zones.append(read_zone_template(file))
#
#     return zones
