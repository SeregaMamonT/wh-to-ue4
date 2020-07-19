from xml.etree.ElementTree import Element, SubElement
from typing import List

from terry_savers.xml_saver_utils import ectransform_to_xml, ecmeshrendersettings_to_xml, ecterrainclamp_to_xml, s_bool, \
    create_entity_node

from wh_terry_objects import TerryPlayableArea


def save_playable_area(playable_area: TerryPlayableArea, entities: Element):
    entity = create_entity_node(entities)
    ECPlayableArea = SubElement(entity, "ECPlayableArea", {
    })
    ECPlayerDeploymentLocations = SubElement(entity, "ECPlayerDeploymentLocations", {
        "deployment_locations": ",".join(map(str, playable_area.deployment_locations)),
    })
    ectransform_to_xml(entity, playable_area.ectransform)
    ECTransform2D = SubElement(entity, "ECTransform2D", {
    })
    ECRectangle = SubElement(entity, "ECRectangle", {
        "width": str(playable_area.width),
        "height": str(playable_area.height),
    })
