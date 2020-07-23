from xml.etree.ElementTree import Element, SubElement
from typing import List

from terry_savers.xml_saver_utils import ectransform_to_xml, ecpolyline_to_xml, s_bool, \
    create_entity_node, s_float

from wh_terry_objects import TerryRegion


def save_non_terrain_outlines(non_terrain_outlines: List[TerryRegion], entities: Element):
    for non_terrain_outline in non_terrain_outlines:
        entity = create_entity_node(entities)
        ECNoGoRegion = SubElement(entity, "ECNoGoRegion", {
        })
        ectransform_to_xml(entity, non_terrain_outline.ectransform)
        ECTransform2D = SubElement(entity, "ECTransform2D", {
        })
        ecpolyline_to_xml(entity, non_terrain_outline.polyline)

