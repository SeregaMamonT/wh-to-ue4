from typing import BinaryIO, List, Any, Callable

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8,  read_transform_n_x_m

from wh_binary_objects import Building, BuildingProperty

from version_holder import VersionHolder

def read_building_list(file: BinaryIO):
    assert_version('BATTLEFIELD_BUILDING_LIST', 1, int2(file))
    return read_list(file, read_building)


def read_building(file):
    building_version = int2(file)
    return buildings_versions.get_reader(building_version)(file)


def read_building_v8(file):
    building = Building()
    building.flags = {}
    building.building_id = string(file)
    building.parent_id = int2(file)
    building.building_key = string(file)
    building.position_type = string(file)
    building.transform = read_transform_n_x_m(file, 4, 3)

    property_version = int2(file)
    building.properties = building_property_versions.get_reader(property_version)(file)

    building.height_mode = string(file)

    #print(building.__dict__)
    return building

def read_building_v11(file):
    building = Building()
    building.flags = {}
    building.building_id = string(file)
    building.parent_id = int2(file)
    some_unknown_flag = int2(file)
    building.building_key = string(file)
    print(building.building_key)
    building.position_type = string(file)
    print(building.position_type)
    building.transform = read_transform_n_x_m(file, 4, 3)
    print(building.transform)
    property_version = int2(file)
    building.properties = building_property_versions.get_reader(property_version)(file)

    building.height_mode = string(file)
    print(building.height_mode)
    #print(building.__dict__)
    # extra 8 bytes in the end of building
    file.read(8)
    return building

buildings_versions = VersionHolder('Building', {
    8: read_building_v8,
    11: read_building_v11
})


def read_building_property_v4(file):
    building_property = BuildingProperty()
    # seems to be empty string building_id
    building_property.building_id = string(file)
    building_property.starting_damage_unary = float4(file)
    building_property.flags = {}
    # i am not sure about next 4 bytes, but probably they are on_fire, start_disabled, weak_point, ai_breachable
    building_property.flags["on_fire"] = bool1(file)
    building_property.flags["start_disabled"] = bool1(file)
    building_property.flags["weak_point"] = bool1(file)
    building_property.flags["ai_breachable"] = bool1(file)
    building_property.flags["indestructible"] = bool1(file)
    # next byte is probably dockable
    building_property.flags["dockable"] = bool1(file)
    building_property.flags["toggleable"] = bool1(file)
    # next 2 bytes are  probably lite and clamp_to_surface
    building_property.flags["lite"] = bool1(file)
    building_property.flags["clamp_to_surface"] = bool1(file)
    building_property.flags["cast_shadows"] = bool1(file)

    return building_property

def read_building_property_v11(file):
    building_property = BuildingProperty()
    # need to wait untill Assembly Kit release, have no idea about those flags. It has 5 extra byte compared to
    # version 4.
    file.read(21)

    return building_property

building_property_versions = VersionHolder('Building propery', {
    4: read_building_property_v4,
    11: read_building_property_v11
})
