
import random
from xml.etree.ElementTree import Element, SubElement, tostring
from typing import Dict, List
from wh_binary_to_terry_convertor import convert_building
from terry_savers.xml_saver_utils import ectransform_to_xml, ecmeshrendersettings_to_xml, ecterrainclamp_to_xml


from wh_binary_objects import Building
from wh_terry_objects import TerryBuilding

def save_buildings_list(buildings: List[Building], entities: Element):
    for building in buildings:
        terry_building = convert_building(building)
        entity = SubElement(entities, "entity", {"id": hex(random.randrange(10 ** 17, 10 ** 18))[2:]})
        ECBuilding = SubElement(entity, "ECBuilding", {
            "key": terry_building.key,
            "damage": str(terry_building.damage),
            "indestructible": str(terry_building.flags["indestructible"]).lower(),
            "toggleable": str(terry_building.flags["toggleable"]).lower(),
            "capture_location": "",
            "export_as_prop": str(terry_building.flags["export_as_prop"]).lower(),
            "allow_in_outfield_as_prop": str(terry_building.flags["allow_in_outfield_as_prop"]).lower(),
        })
        ecmeshrendersettings_to_xml(entity, terry_building.ecmeshrendersettings)
        ectransform_to_xml(entity, terry_building.ectransform)
        ecterrainclamp_to_xml(entity, terry_building.ecterrainclamp)

    return entities
