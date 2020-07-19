from xml.etree.ElementTree import Element, SubElement
from typing import List

from terry_savers.xml_saver_utils import ectransform_to_xml, ecmeshrendersettings_to_xml, ecterrainclamp_to_xml, s_bool, \
    create_entity_node

from wh_terry_objects import TerryPointLight


def save_point_light_list(point_lights: List[TerryPointLight], entities: Element):
    for point_light in point_lights:
        entity = create_entity_node(entities)
        ECPointLight = SubElement(entity, "ECPointLight", {
            "colour": str(point_light.colour.red)+" "+str(point_light.colour.green)+" "+str(point_light.colour.blue)+" "+"255",
            "colour_scale": str(point_light.colour_scale),
            "radius": str(point_light.radius),
            "animation_type": point_light.animation_type,
            "animation_speed_scale": " ".join(map(str, point_light.animation_speed_scale)),
            "colour_min": str(point_light.colour_min),
            "random_offset": str(point_light.random_offset),
            "falloff_type": point_light.falloff_type,
            "for_light_probes_only": s_bool(point_light.for_light_probes_only),
        })
        ectransform_to_xml(entity, point_light.ectransform)

