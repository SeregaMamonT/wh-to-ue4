from wh_binary_objects import Prefab, MapData
from enum import Enum
from xml.etree.ElementTree import Element, SubElement, tostring
from wh_binary_to_terry_convertor import convert_building, convert_particle, convert_decal, convert_prop_building, \
    convert_prefab_instance, convert_tree_instance

from terry_savers.terry_buildings_list import save_buildings_list
from terry_savers.terry_particles_list import save_particles_list
from terry_savers.terry_decals_list import save_decals_list
from terry_savers.terry_prop_building_list import save_prop_buildings_list
from terry_savers.terry_prefab_insatnce_list import save_prefab_instance_list
from terry_savers.terry_tree_list import save_tree_list

class StructureType(Enum):
    PREFAB = 1
    MAP = 2


def terry_layer_saver(filename: str, object: tuple, type: StructureType):
    get_type_saver(type)(filename, object)


def prefab_saver(filename, prefab_data: tuple):
    print('Start saving')
    prefab = prefab_data[0]
    vegetation = prefab_data[1]
    # for i in prefab.buildings:
    #    convert_building(i)
    entities = Element("entities")
    save_buildings_list(list(map(convert_building, prefab.buildings)), entities)
    save_particles_list(list(map(convert_particle, prefab.particles)), entities)
    for key, props in prefab.props.items():
        decals = filter(lambda prop: prop.decal, props)
        not_decals = filter(lambda prop: not prop.decal, props)
        save_decals_list(list(map(convert_decal, decals)), entities)
        save_prop_buildings_list(list(map(convert_prop_building, not_decals)), entities)
    save_prefab_instance_list(list(map(convert_prefab_instance, prefab.prefab_instances)), entities)
    for i in vegetation:
        # print(i.trees)
        for j in i.trees:
            save_tree_list(convert_tree_instance(j), entities)
    #for i in vegetation:
        # print(i)
        #
    # props = filter(lambda prop: not prop.decal, prefab.props)
    content = tostring(entities, "utf-8").decode("utf-8")
    save_to_file(content, filename + ".xml")


def map_saver(filename, map_data_tuple: tuple):
    map_data = map_data_tuple[0]
    vegetation = map_data_tuple[1]
    entities = Element("entities")
    save_buildings_list(list(map(convert_building, map_data.buildings)), entities)
    save_particles_list(list(map(convert_particle, map_data.particles)), entities)
    for key, props in map_data.props.items():
        decals = filter(lambda prop: prop.decal, props)
        not_decals = filter(lambda prop: not prop.decal, props)
        save_decals_list(list(map(convert_decal, decals)), entities)
        save_prop_buildings_list(list(map(convert_prop_building, not_decals)), entities)
    save_prefab_instance_list(list(map(convert_prefab_instance, map_data.prefab_instances)), entities)
    for i in vegetation:
        for j in i:
            save_tree_list(convert_tree_instance(j), entities)

    content = tostring(entities, "utf-8").decode("utf-8")
    save_to_file(content, filename + ".xml")


def get_type_saver(type):
    if type in terry_savers:
        return terry_savers[type]
    else:
        raise Exception('Unsupported save type: ' + str(type))


terry_savers = {
    StructureType.PREFAB: prefab_saver,
    StructureType.MAP: map_saver,
}


def save_to_file(content, name):
    output_file = open(name, "w")
    output_file.write(content)
    output_file.close()
