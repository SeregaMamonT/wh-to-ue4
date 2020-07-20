from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, get_scale

from wh_binary_objects import ZoneTemplate, Point2D

from app_typing import Matrix, Vector


def read_zone_template(file):
    zone_template = ZoneTemplate()
    points_amount = int4(file)
    zone_template.points = []
    for i in range(points_amount):
        point = Point2D(float4(file), float4(file))
        zone_template.points.append(point)

    # <zone_name> <entity_formation_template name=''> and <lines/>
    file.read(8)
    # transformation matrix
    zone_template.transformation = []
    for i in range(4):
        row = [float4(file), float4(file), float4(file), float4(file)]
        zone_template.transformation.append(row)
    return zone_template


def read_zones_template_list(file: BinaryIO):
    version = int2(file)  # version
    zones_amount = int4(file)
    zones = []
    for i in range(zones_amount):
        read_zone_template(file)
        #zones.append(read_zone_template(file))

    return zones
