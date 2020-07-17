from xml.etree.ElementTree import Element, SubElement
from typing import List

from terry_savers.xml_saver_utils import ectransform_to_xml, ecmeshrendersettings_to_xml, ecterrainclamp_to_xml, s_bool, \
    create_entity_node

from wh_terry_objects import TerryBuilding


def save_buildings_list(buildings: List[TerryBuilding], entities: Element):
    for building in buildings:
        entity = create_entity_node(entities)
        ECBuilding = SubElement(entity, "ECBuilding", {
            "key": building.key,
            "damage": str(building.damage),
            "indestructible": s_bool(building.flags["indestructible"]),
            "toggleable": s_bool(building.flags["toggleable"]),
            "capture_location": "",
            "export_as_prop": s_bool(building.flags["export_as_prop"]),
            "allow_in_outfield_as_prop": s_bool(building.flags["allow_in_outfield_as_prop"]),
        })
        ecmeshrendersettings_to_xml(entity, building.ecmeshrendersettings)
        ectransform_to_xml(entity, building.ectransform)
        ecterrainclamp_to_xml(entity, building.ecterrainclamp)
