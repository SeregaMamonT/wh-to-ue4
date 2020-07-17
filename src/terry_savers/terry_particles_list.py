
from xml.etree.ElementTree import Element, SubElement, tostring
from typing import Dict, List
from wh_binary_to_terry_convertor import convert_particle
from terry_savers.xml_saver_utils import ectransform_to_xml, ecterrainclamp_to_xml, create_entity_node


from wh_binary_objects import Particle
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
        ecterrainclamp_to_xml(entity, terry_particle.ectransform)
        ectransform_to_xml(entity, terry_particle.ectransform)
        ecterrainclamp_to_xml(entity, terry_particle.ecterrainclamp)

    return entities