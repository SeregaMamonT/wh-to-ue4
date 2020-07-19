from xml.etree.ElementTree import Element, SubElement
from typing import List

from terry_savers.xml_saver_utils import ectransform_to_xml, s_bool, create_entity_node, s_float

from wh_terry_objects import TerryCompositeSecne


def save_composite_scene_list(composite_scenes: List[TerryCompositeSecne], entities: Element):
    for composite_scene in composite_scenes:
        entity = create_entity_node(entities)
        ECCompositeScene = SubElement(entity, "ECCompositeScene", {
            "path": composite_scene.path,
            "autoplay": s_bool(composite_scene.autoplay),
        })
        ectransform_to_xml(entity, composite_scene.ectransform)
