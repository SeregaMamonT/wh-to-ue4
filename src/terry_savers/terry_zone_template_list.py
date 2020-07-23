from xml.etree.ElementTree import Element, SubElement
from typing import List

from terry_savers.xml_saver_utils import ectransform_to_xml, ecpolyline_to_xml, s_bool, \
    create_entity_node, s_float

from wh_terry_objects import TerryZoneTemplate


def save_zone_template_list(zone_templates: List[TerryZoneTemplate], entities: Element):
    for zone_template in zone_templates:
        entity = create_entity_node(entities)
        ECBattlefieldZone = SubElement(entity, "ECBattlefieldZone", {
        })
        ECTerryBattlefieldZone = SubElement(entity, "ECTerryBattlefieldZone", {
            "locked": s_bool(zone_template.locked),
            "rank_distance": s_float(zone_template.rank_distance),
            "zone_skirt_distance": s_float(zone_template.zone_skirt_distance),
        })
        ectransform_to_xml(entity, zone_template.ectransform)
        ECTransform2D = SubElement(entity, "ECTransform2D", {
        })
        ecpolyline_to_xml(entity, zone_template.polyline)

