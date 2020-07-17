from xml.etree.ElementTree import Element, SubElement, tostring
from typing import Dict, List
from terry_savers.xml_saver_utils import ectransform_to_xml, ecterrainclamp_to_xml, create_entity_node, \
    ecbattleproperties_to_xml, s_bool

from wh_terry_objects import TerryDecal


def save_decals_list(decals: List[TerryDecal], entities: Element):
    for terry_decal in decals:
        entity = create_entity_node(entities)
        ECDecal = SubElement(entity, "ECDecal", {
            "model_path": terry_decal.model_path,
            "parallax_scale": str(terry_decal.parallax_scale),
            "tiling": str(terry_decal.tiling),
            "normal_mode": terry_decal.normal_mode,
            "apply_to_terrain": s_bool(terry_decal.flags["apply_to_terrain"]),
            "apply_to_objects": s_bool(terry_decal.flags["apply_to_objects"]),
            "render_above_snow": s_bool(terry_decal.flags["render_above_snow"]),
        })
        ecterrainclamp_to_xml(entity, terry_decal.ectransform)
        ectransform_to_xml(entity, terry_decal.ectransform)
        ecbattleproperties_to_xml(entity, terry_decal.ecbattleproperties)

    return entities