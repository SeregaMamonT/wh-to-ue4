from xml.etree.ElementTree import Element, SubElement
from typing import List

from terry_savers.xml_saver_utils import ectransform_to_xml, create_entity_node, s_float

from wh_terry_objects import TerryBuildingProjectileEmitter


def save_building_projectile_emitter_list(building_projectile_emitters: List[TerryBuildingProjectileEmitter], entities: Element):
    for building_projectile_emitter in building_projectile_emitters:
        entity = create_entity_node(entities)
        ECBuildingProjectileEmitter = SubElement(entity, "ECBuildingProjectileEmitter", {
        })
        ectransform_to_xml(entity, building_projectile_emitter.ectransform)