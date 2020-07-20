from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

from wh_binary_objects import SoundShape, Point3D, Cube, RiverNode

from version_holder import VersionHolder


def read_river_node_v1(file):
    river_node = RiverNode()
    river_node.vertex = Point3D(float4(file), float4(file), float4(file))
    river_node.width = float4(file)
    river_node.flow_speed = float4(file)

    return river_node


river_node_versions = VersionHolder('River node', {
    1: read_river_node_v1,
})


def read_sound_shape_common(file):
    sound_shape = SoundShape()
    sound_shape.key = string(file)
    sound_shape.type = string(file)
    points = int4(file)
    sound_shape.points = []
    for j in range(points):
        point = Point3D(float4(file), float4(file), float4(file))
        sound_shape.points.append(point)
    sound_shape.inner_radius = float4(file)
    sound_shape.outer_radius = float4(file)
    sound_shape.inner_cube = Cube(float4(file), float4(file), float4(file), float4(file), float4(file), float4(file))
    sound_shape.outer_cube = Cube(float4(file), float4(file), float4(file), float4(file), float4(file), float4(file))
    river_nodes_amount = int4(file)
    sound_shape.river_nodes_list = []
    for i in range(river_nodes_amount):
        river_node_version = int2(file)
        sound_shape.river_nodes_list.append(river_node_versions.get_reader(river_node_version)(file))
    sound_shape.clamp_to_surface = bool1(file)
    sound_shape.height_mode = string(file)
    sound_shape.campaign_type_mask = int4(file)

    return sound_shape


def read_sound_shape_v6(file):
    sound_shape = read_sound_shape_common(file)
    sound_shape.pdlc_mask = int4(file)

    return sound_shape


def read_sound_shape_v7(file):
    sound_shape = read_sound_shape_common(file)
    sound_shape.pdlc_mask = int8(file)

    return sound_shape


sound_shape_versions = VersionHolder('Sound shape', {
    6: read_sound_shape_v6,
    7: read_sound_shape_v7,
})


def read_sound_shape(file):
    sound_shape_version = int2(file)
    return sound_shape_versions.get_reader(sound_shape_version)(file)


def read_sound_shape_list(file: BinaryIO):
    version = int2(file)  # version
    return read_list(file, read_sound_shape)
