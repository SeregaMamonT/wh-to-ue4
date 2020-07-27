from xml.etree.ElementTree import Element, SubElement
from typing import List

from terry_savers.xml_saver_utils import ectransform_to_xml, ecmeshrendersettings_to_xml, ecterrainclamp_to_xml, s_bool, \
    create_entity_node, s_float

from wh_terry_objects import TerryRiver, TerrySplinePoint


def save_river_list(terry_rivers: List[TerryRiver], entities: Element):
    for terry_river in terry_rivers:
        entity = create_entity_node(entities)
        ECRiver = SubElement(entity, "ECRiver", {
        })
        ectransform_to_xml(entity, terry_river.ectransform)
        save_spline(entity, terry_river)


def save_spline(entity: Element, terry_river: TerryRiver):
    ECRiverSpline = SubElement(entity, "ECRiverSpline", {
        "spline_step_size": s_float(terry_river.spline_step_size),
        "terrain_relative": s_bool(terry_river.terrain_relative),
        "reverse_direction": s_bool(terry_river.reverse_direction)
    })
    spline = SubElement(ECRiverSpline, "spline", {
        "closed": s_bool(terry_river.spline_closed)
    })
    for point in terry_river.spline:
        point = SubElement(spline, "point", {
            "position": "{0} {1} {2}".format(s_float(point.position.x), s_float(point.position.y),
                                             s_float(point.position.z)),
            "tangent_in": "{0} {1} {2}".format(s_float(point.tangent_in[0]), s_float(point.tangent_in[1]),
                                             s_float(point.tangent_in[2])),
            "tangent_out": "{0} {1} {2}".format(s_float(point.tangent_out[0]), s_float(point.tangent_out[1]),
                                               s_float(point.tangent_out[2])),
            "width": s_float(point.width),
            "terrain_offset": s_float(point.terrain_offset),
            "alpha_fade": s_float(point.alpha_fade),
            "flow_speed": s_float(point.flow_speed),
            "foam_amount": s_float(point.foam_amount),
        })
