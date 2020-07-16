import json
import sys
import random
from os import listdir, path
from xml.etree.ElementTree import Element, SubElement, tostring

def format_float(x):
    return "{:.5f}".format(x).rstrip("0").strip(".")

def save_buildings_list(buildings, entities: Element):
    for model in buildings:
        entity = SubElement(entities, "entity", {"id": hex(random.randrange(10 ** 17, 10 ** 18))[2:]})
        ECBuilding = SubElement(entity, "ECBuilding", {
            "key": model["model_name"],
            "damage": "0",
            "indestructible": "false",
            "toggleable": "false",
            "capture_location": "",
            "export_as_prop": "false",
            "allow_in_outfield_as_prop": "false"
        })
        ECMeshRenderSettings = SubElement(entity, "ECMeshRenderSettings", {
            "cast_shadow": "true"
        })
        print(model["position"])
        print(model["coordinates"])
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
