from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

from wh_binary_objects import SoundShape, Point3D, Cube


def read_sound_shape_v6(file):
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
    river_nodes_list = []
    for i in range(river_nodes_amount):
        river_node_version = int2(file)
        rive_nodes_points = (float4(file), float4(file), float4(file), float4(file), float4(file))
        river_nodes_list.append(rive_nodes_points)
    sound_shape.clamp_to_surface = bool1(file)
    sound_shape.height_mode = string(file)
    sound_shape.campaign_type_mask = int4(file)
    sound_shape.pdlc_mask = int4(file)
    #print(sound_shape.__dict__)

    return sound_shape


def read_sound_shape_v7(file):
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
    river_nodes_list = []
    for i in range(river_nodes_amount):
        river_node_version = int2(file)
        rive_nodes_points = (float4(file), float4(file), float4(file), float4(file), float4(file))
        river_nodes_list.append(rive_nodes_points)
    sound_shape.clamp_to_surface = bool1(file)
    sound_shape.height_mode = string(file)
    sound_shape.campaign_type_mask = int4(file)
    sound_shape.pdlc_mask = int8(file)

    return sound_shape


version_readers = {
    6: read_sound_shape_v6,
    7: read_sound_shape_v7,
}


def get_version_reader(version):
    if version in version_readers:
        return version_readers[version]
    else:
        raise Exception('Unsupported sound shape version: ' + str(version))


def read_sound_shape_list(file: BinaryIO):
    version = int2(file)  # version
    amount = int4(file)
    sound_shapes = []
    # print('Sound shapes: ', version, sound_shapes)
    for i in range(amount):
        sound_shape_version = int2(file)
        sound_shapes.append(get_version_reader(sound_shape_version)(file))

    return sound_shapes
