from typing import BinaryIO, List, Any, Callable

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

from wh_binary_objects import Building

def read_building_list(file: BinaryIO):
    assert_version('BATTLEFIELD_BUILDING_LIST', 1, int2(file))
    return read_list(file, read_building_instance)


def read_building_instance(file: BinaryIO):
    building = Building()
    building.flags = {}

    assert_version('BUILDING', 8, int2(file))
    # file.read(4)
    t = (int2(file), int2(file))
    building.building_key = string(file)
    building.position_type = string(file)

    building.coordinates = [[None] * 3 for i in range(3)]
    for i in range(9):
        building.coordinates[i // 3][i % 3] = float4(file)
    building.transform = [None] * 3
    for i in range(3):
        building.transform[i] = float4(file)


    # print('2')
    property_version = int2(file)

    # seems to be empty string building_id
    file.read(2)
    building.starting_damage_unary = float4(file)

    # i am not sure about next 4 bytes, but probably they are on_fire, start_disabled, weak_point, ai_breachable
    building.flags["on_fire"] = bool1(file)
    building.flags["start_disabled"] = bool1(file)
    building.flags["weak_point"] = bool1(file)
    building.flags["ai_breachable"] = bool1(file)
    building.flags["indestructible"] = bool1(file)

    # next byte is probably dockable
    dockable = bool1(file)

    building.flags["toggleable"] = bool1(file)

    # next 2 bytes are  probably lite and clamp_to_surface
    lite = bool1(file)
    clamp_to_surface = bool1(file)

    building.flags["cast_shadows"] = bool1(file)
    building.height_mode = string(file)

    # print(building.__dict__)
    return building
