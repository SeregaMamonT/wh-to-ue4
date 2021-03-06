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
    outline = Outline()
    for i in range(points_amount):
        outline.points.append(Point2D(float4(file), float4(file)))
    zone_template.outline = outline
    # <zone_name> <entity_formation_template name=''> and <lines/>
    file.read(8)
    # transformation matrix
    zone_template.transformation = read_transform_n_x_m(file, 4, 4)

    return zone_template

