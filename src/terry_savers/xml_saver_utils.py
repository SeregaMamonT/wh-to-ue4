from xml.etree.ElementTree import Element, SubElement, tostring
from typing import Dict, List
from wh_terry_objects import ECTransform, ECMeshRenderSettings, ECBattleProperties, ECTerrainClamp


def s_float(x):
    return "{:.5f}".format(x).rstrip("0").strip(".")


def s_bool(bool_value):
    return str(bool_value).lower()


def create_entity_node(entities: Element):
    return SubElement(entities, "entity", {"id": hex(random.randrange(10 ** 17, 10 ** 18))[2:]})


def ectransform_to_xml(entity: Element, ectransform: ECTransform):
    ECTransform = SubElement(entity, "ECTransform", {
        "position": " ".join(map(s_float, ectransform.position)),
        "rotation": " ".join(map(s_float, ectransform.rotation)),
        "scale": " ".join(map(s_float, ectransform.scale)),
    })


def ecmeshrendersettings_to_xml(entity: Element, ecmeshrendersettings: ECMeshRenderSettings):
    ECMeshRenderSettings = SubElement(entity, "ECMeshRenderSettings", {
        "cast_shadow": str(ecmeshrendersettings.cast_shadow).lower()
    })


def ecterrainclamp_to_xml(entity: Element, ecterrainclamp: ECTerrainClamp):
    ECTerrainClamp = SubElement(entity, "ECTerrainClamp", {
        "active": "false",
        "clamp_to_sea_level": "false",
        "terrain_oriented": "false",
    })


def ecbattleproperties_to_xml(entity: Element, ecbattleproperties: ECBattleProperties):
    ECBattleProperties = SubElement(entity, "ECBattleProperties", {
        "allow_in_outfield": "false",
    })
