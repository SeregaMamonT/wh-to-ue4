from xml.etree.ElementTree import Element, SubElement
from typing import List

from wh_binary_to_terry_convertor import convert_building
from terry_savers.xml_saver_utils import ectransform_to_xml, ecmeshrendersettings_to_xml, ecterrainclamp_to_xml, s_bool, \
    create_entity_node

from wh_binary_objects import Building


def save_buildings_list(buildings: List[Building], entities: Element):
    for building in buildings:
        terry_building = convert_building(building)
        entity = create_entity_node(entities)
        ECBuilding = SubElement(entity, "ECBuilding", {
            "key": terry_building.key,
            "damage": str(terry_building.damage),
            "indestructible": s_bool(terry_building.flags["indestructible"]),
            "toggleable": s_bool(terry_building.flags["toggleable"]),
            "capture_location": "",
            "export_as_prop": s_bool(terry_building.flags["export_as_prop"]),
            "allow_in_outfield_as_prop": s_bool(terry_building.flags["allow_in_outfield_as_prop"]),
        })
        ecmeshrendersettings_to_xml(entity, terry_building.ecmeshrendersettings)
        ectransform_to_xml(entity, terry_building.ectransform)
        ecterrainclamp_to_xml(entity, terry_building.ecterrainclamp)
