from typing import BinaryIO, List, Any, Callable

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale


def read_building_list(file: BinaryIO):
    assert_version('BATTLEFIELD_BUILDING_LIST', 1, int2(file))
    return read_list(file, read_building_instance)


def read_building_instance(file: BinaryIO):
    instance = {}
    assert_version('BUILDING', 8, int2(file))
    # file.read(4)
    t = (int2(file), int2(file))
    # if t not in context:
    #    context.append(t)
    instance["model_name"] = string(file)

    instance["object_relation1"] = string(file)

    coordinates = read_coordinates(file)
    translation = read_translation(file)

    scales = get_scale(coordinates)
    unscale(coordinates, scales)

    instance["position"] = translation
    instance["scale"] = scales
    instance["coordinates"] = coordinates
    # print('2')
    property_version = int2(file)

    # seems to be empty string building_id
    file.read(2)
    starting_damage_unary = float4(file)

    # i am not sure about next 4 bytes, but probably they are on_fire, start_disabled, weak_point, ai_breachable
    on_fire = bool1(file)
    start_disabled = bool1(file)
    weak_point = bool1(file)
    ai_breachable = bool1(file)

    indestructible = bool1(file)

    # next byte is probably dockable
    dockable = bool1(file)

    toggleable = bool1(file)

    # next 2 bytes are  probably lite and clamp_to_surface
    lite = bool1(file)
    clamp_to_surface = bool1(file)

    cast_shadows = bool1(file)
    instance["object_relation2"] = string(file)
    # print(instance["model_name"], 'version: ', property_version, 'damage: ', starting_damage_unary, 'indestructable: ',
    #      indestructible, 'toggleable: ', toggleable, 'cast shadows: ', cast_shadows)

    return instance
