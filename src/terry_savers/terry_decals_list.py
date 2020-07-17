from xml.etree.ElementTree import Element, SubElement, tostring
from typing import Dict, List
from terry_savers.xml_saver_utils import ectransform_to_xml, ecterrainclamp_to_xml, create_entity_node, \
    ecbattleproperties_to_xml

from wh_terry_objects import TerryDecal


def save_decals_list(decals: List[TerryDecal], entities: Element):
    for terry_decal in decals:
        entity = create_entity_node(entities)
        ECDecal = SubElement(entity, "ECDecal", {
            "model_path": terry_decal.model_path,
            "parallax_scale": "1",
            "tiling": "2",
            "normal_mode": "DNM_BLEND",
            "apply_to_terrain": "true",
            "apply_to_objects": "true",
            "render_above_snow": "false",
        })
        ecterrainclamp_to_xml(entity, terry_decal.ectransform)
        ectransform_to_xml(entity, terry_decal.ectransform)
        ecbattleproperties_to_xml(entity, terry_decal.ecbattleproperties)

    return entities