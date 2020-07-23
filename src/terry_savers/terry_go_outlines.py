from xml.etree.ElementTree import Element, SubElement
from typing import List

from terry_savers.xml_saver_utils import ectransform_to_xml, ecpolyline_to_xml, s_bool, \
    create_entity_node, s_float

from wh_terry_objects import TerryRegion


def save_go_outlines(go_outlines: List[TerryRegion], entities: Element):
    for go_outline in go_outlines:
        entity = create_entity_node(entities)
        ECGoRegion = SubElement(entity, "ECGoRegion", {
        })
        ectransform_to_xml(entity, go_outline.ectransform)
        ECTransform2D = SubElement(entity, "ECTransform2D", {
        })
        ecpolyline_to_xml(entity, go_outline.polyline)

