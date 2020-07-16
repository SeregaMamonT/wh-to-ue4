import json
import sys
import random
from os import listdir, path
from xml.etree.ElementTree import Element, SubElement, tostring
from typing import Dict, List
from wh_binary_to_terry_convertor import convert_building

from wh_terry_objects import TerryBuilding

def format_float(x):
    return "{:.5f}".format(x).rstrip("0").strip(".")

def save_buildings_list(buildings: List[TerryBuilding], entities: Element):
    for building in buildings:
        terry_building = convert_building(building)
        entity = SubElement(entities, "entity", {"id": hex(random.randrange(10 ** 17, 10 ** 18))[2:]})
        ECBuilding = SubElement(entity, "ECBuilding", {
            "key": 'terry_building.key',
            "damage": map(format_float, terry_building.damage),
            "indestructible": "false",
            "toggleable": "false",
            "capture_location": "",
            "export_as_prop": "false",
            "allow_in_outfield_as_prop": "false"
        })
        ECMeshRenderSettings = SubElement(entity, "ECMeshRenderSettings", {
            "cast_shadow": "true"
        })

        # ECTransform = SubElement(entity, "ECTransform", {
        #     "position": " ".join(map(format_float, model["position"])),
        #     "rotation": " ".join(map(format_float, model["rotation"])),
        #     "scale": " ".join(map(format_float, model["scale"])),
        # })

        ECTerrainClamp = SubElement(entity, "ECTerrainClamp", {
            "active": "false",
            "clamp_to_sea_level": "false",
            "terrain_oriented": "false",
        })

    return entities
