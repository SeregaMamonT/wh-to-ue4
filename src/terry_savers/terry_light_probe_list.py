from xml.etree.ElementTree import Element, SubElement
from typing import List

from terry_savers.xml_saver_utils import ectransform_to_xml, ecmeshrendersettings_to_xml, ecterrainclamp_to_xml, s_bool, \
    create_entity_node

from wh_terry_objects import TerryLightProbe


def save_light_probe_list(light_probes: List[TerryLightProbe], entities: Element):
    for light_probe in light_probes:
        entity = create_entity_node(entities)
        ECLightProbe = SubElement(entity, "ECLightProbe", {
            "primary": s_bool(light_probe.is_primary),
        })
        ectransform_to_xml(entity, light_probe.ectransform)
        ECSphere = SubElement(entity, "ECSphere", {
            "radius": str(light_probe.radius),
        })
