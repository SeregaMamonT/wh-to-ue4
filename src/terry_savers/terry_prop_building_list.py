from xml.etree.ElementTree import Element, SubElement, tostring
from typing import Dict, List
from terry_savers.xml_saver_utils import ectransform_to_xml, ecterrainclamp_to_xml, create_entity_node, \
    ecbattleproperties_to_xml, s_bool

from wh_terry_objects import TerryPropBuilding


def save_prop_buildings_list(prop_buildings: List[TerryPropBuilding], entities: Element):
    for prop_building in prop_buildings:
        entity = create_entity_node(entities)
        ECPropMesh = SubElement(entity, "ECPropMesh")
        ECMesh = SubElement(entity, "ECMesh", {
            "model_path": prop_building.model_path,
            "animation_path": "",
            "opacity": "1",
        })
        ecterrainclamp_to_xml(entity, prop_building.ecterrainclamp)
        ectransform_to_xml(entity, prop_building.ectransform)
        ecbattleproperties_to_xml(entity, prop_building.ecbattleproperties)

    return entities