import random
from xml.etree.ElementTree import Element, SubElement, tostring
from typing import Dict, List
from wh_binary_to_terry_convertor import convert_particle
from terry_savers.xml_saver_utils import ectransform_to_xml, ecterrainclamp_to_xml, ecbattleproperties_to_xml


from wh_binary_objects import Particle
from wh_terry_objects import TerryParticle


def save_particles_list(particles: List[Particle], entities: Element):
    for particle in particles:
        terry_particle = convert_particle(particle)
        entity = SubElement(entities, "entity", {"id": hex(random.randrange(10 ** 17, 10 ** 18))[2:]})

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