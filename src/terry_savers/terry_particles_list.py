from xml.etree.ElementTree import Element, SubElement, tostring
from typing import Dict, List
from terry_savers.xml_saver_utils import ectransform_to_xml, ecterrainclamp_to_xml, create_entity_node, \
    ecbattleproperties_to_xml

from wh_terry_objects import TerryParticle


def save_particles_list(particles: List[TerryParticle], entities: Element):
    for terry_particle in particles:
        # terry_particle = convert_particle(particle)
        entity = create_entity_node(entities)

        ECVFX = SubElement(entity, "ECVFX", {
            "vfx": terry_particle.vfx,
            "autoplay": "true",
            "scale": "1",
            "instance_name": "",
        })
        ecterrainclamp_to_xml(entity, terry_particle.ecterrainclamp)
        ectransform_to_xml(entity, terry_particle.ectransform)
        ecbattleproperties_to_xml(entity, terry_particle.ecbattleproperties)

    return entities
