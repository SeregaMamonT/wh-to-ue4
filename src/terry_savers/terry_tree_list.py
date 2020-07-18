from xml.etree.ElementTree import Element, SubElement
from typing import List

from terry_savers.xml_saver_utils import ectransform_to_xml, ecmeshrendersettings_to_xml, ecterrainclamp_to_xml, s_bool, \
    create_entity_node

from wh_terry_objects import TerryTree


def save_tree_list(trees: List[TerryTree], entities: Element):
    for tree in trees:
        entity = create_entity_node(entities)
        ECVegetation = SubElement(entity, "ECVegetation", {
            "key": tree.key,
        })
        ectransform_to_xml(entity, tree.ectransform)
        ecterrainclamp_to_xml(entity, tree.ecterrainclamp)