from xml.etree.ElementTree import Element, SubElement
from typing import List

from terry_savers.xml_saver_utils import ectransform_to_xml, ecmeshrendersettings_to_xml, ecterrainclamp_to_xml, s_bool, \
    create_entity_node, s_float

from wh_terry_objects import TerrySpotLight


def save_spot_light_list(spot_lights: List[TerrySpotLight], entities: Element):
    for spot_light in spot_lights:
        entity = create_entity_node(entities)
        ECSpotLight = SubElement(entity, "ECSpotLight", {
            "colour": str(spot_light.colour.red) + " " + str(spot_light.colour.green) + " " + str(
                spot_light.colour.blue) + " " + str(spot_light.colour.alpha),
            "intensity": s_float(spot_light.intensity),
            "length": s_float(spot_light.length),
            "inner_angle": s_float(spot_light.inner_angle),
            "outer_angle": s_float(spot_light.outer_angle),
            "falloff": s_float(spot_light.falloff),
            "volumetric": s_bool(spot_light.volumetric),
            "gobo": spot_light.gobo,
        })
        ectransform_to_xml(entity, spot_light.ectransform)
