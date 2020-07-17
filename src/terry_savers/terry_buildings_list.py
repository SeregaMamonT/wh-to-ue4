import json
import sys
import random
from os import listdir, path
from xml.etree.ElementTree import Element, SubElement, tostring
from typing import Dict, List
from wh_binary_to_terry_convertor import convert_building
from terry_savers.xml_saver_utils import ectransform_to_xml, ecmeshrendersettings_to_xml
from terry_savers.xml_saver_utils import format_float

from wh_binary_objects import Building
from wh_terry_objects import TerryBuilding

def save_buildings_list(buildings: List[Building], entities: Element):
    for building in buildings:
        terry_building = convert_building(building)
        entity = SubElement(entities, "entity", {"id": hex(random.randrange(10 ** 17, 10 ** 18))[2:]})
        ECBuilding = SubElement(entity, "ECBuilding", {
            "key": terry_building.key,
            "damage": str(terry_building.damage),
            "indestructible": "false",
            "toggleable": "false",
            "capture_location": "",
            "export_as_prop": "false",
            "allow_in_outfield_as_prop": "false"
        })
        ecmeshrendersettings_to_xml(entity, terry_building.ecmeshrendersettings)
        ectransform_to_xml(entity, terry_building.ectransform)

        ECTerrainClamp = SubElement(entity, "ECTerrainClamp", {
            "active": "false",
            "clamp_to_sea_level": "false",
            "terrain_oriented": "false",
        })

    return entities
