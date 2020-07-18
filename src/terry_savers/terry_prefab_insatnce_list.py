from xml.etree.ElementTree import Element, SubElement, tostring
from typing import Dict, List
from terry_savers.xml_saver_utils import ectransform_to_xml, ecterrainclamp_to_xml, create_entity_node, \
    ecbattleproperties_to_xml, s_bool

from wh_terry_objects import TerryPrefabInstance


def save_prefab_instance_list(prefab_instances: List[TerryPrefabInstance], entities: Element):
    for prefab_instance in prefab_instances:
        entity = create_entity_node(entities)
        ECPrefab = SubElement(entity, "ECPrefab", {
            "key": str(prefab_instance.key),
        })
        ecterrainclamp_to_xml(entity, prefab_instance.ecterrainclamp)
        ectransform_to_xml(entity, prefab_instance.ectransform)

    return entities