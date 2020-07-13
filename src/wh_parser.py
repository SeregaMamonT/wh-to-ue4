from typing import BinaryIO, List, Any, Callable

from wh_binary_objects import Particle, Prop
from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8


#
def mod_vector(vector: List):
    return sum([x * x for x in vector]) ** 0.5


def parse_file(file: BinaryIO, global_context):
    global context
    context = global_context

    file.read(8)  # FASTBIN0
    root_version = int2(file)
    if root_version == 23 or root_version == 24:
        buildings = read_building_list(file)
        read_building_list_far(file)
        read_capture_location_set(file)
        read_ef_line_list(file)
        read_go_outlines(file)
        read_non_terrain_outlines(file)
        read_zones_template_list(file)
        read_prefab_instance_list(file)
        read_bmd_outline_list(file)
        read_terrain_outlines(file)
        read_lite_building_outlines(file)
        read_camera_zones(file)
        read_civilian_deployment_list(file)
        read_civilian_shelter_list(file)
        props = read_prop_list(file)
        particles = read_particle_list(file)
        read_ai_hints(file)

        # rest of file
        read_light_probe_list(file)
        read_terrain_stencil_triangle_list(file)
        read_point_light_list(file)
        read_building_projectile_emitter_list(file)
        read_playable_area(file)
        read_custom_material_mesh_list(file)
        read_terrain_stencil_blend_triangle_list(file)
        read_spot_light_list(file)
        read_sound_shape_list(file)
        read_composite_scene_list(file)
        read_deployment_list(file)
        read_bmd_catchment_area_list(file)
        print('Hooray it did not crash!')
        # only for version 24
        # read_tree_list_reference_list(file)
        # read_grass_list_reference_list(file)

        return buildings

    elif root_version == 2:
        read_vegetation(file)
    else:
        raise Exception('Only versions 2, 23, 24 of root are supported')


def read_vegetation(file: BinaryIO):
    assert_version('Vegetation', 2, int2(file))
    tree_list = int4(file)
    # print('Amount: ', tree_list)
    for i in range(tree_list):
        key = string(file)
        # print('Name:', key)
        amount = int4(file)
        # print('Amount: ', amount)
        for j in range(amount):
            x = float4(file)
            y = float4(file)
            z = float4(file)
            scale = float4(file)
            is_freeform = bool1(file)
            # print(x, y, z, scale, is_freeform)
    vegetation = []


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
    # print('1')
    instance["object_relation1"] = string(file)

    coordinates = read_coordinates(file)
    translation = read_translation(file)

    scales = get_scale(coordinates)
    unscale(coordinates, scales)

    instance["position"] = translation
    instance["scale"] = scales
    instance["coordinates"] = coordinates
    # print('2')
    file.read(18)
    instance["object_relation2"] = string(file)

    return instance


def read_building_list_far(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "BATTLEFIELD_BUILDING_LIST_FAR has items"


def read_capture_location_set(file: BinaryIO):
    version = int2(file)  # version
    # print('Version: ', version)
    list_amount = int4(file)
    for i in range(list_amount):
        location_amount = int4(file)
        # print('Locations: ', location_amount)
        for j in range(location_amount):
            location = (float4(file), float4(file))
            # print(location)
            radius = float4(file)
            valid_for_min_num_players = int4(file)
            valid_for_max_num_players = int4(file)
            # print(radius, valid_for_min_num_players, valid_for_max_num_players)
            capture_point_type = string(file)
            # print(capture_point_type)
            location_points = int4(file)
            location_points_list = []
            for l in range(location_points):
                t = (float4(file), float4(file))
                location_points_list.append(t)
            # print(location_points_list)
            database_key = string(file)
            # print(database_key)
            flag_facing = (float4(file), float4(file))
            building_links = int4(file)
            # print(building_links)
            for l in range(building_links):
                file.read(10)
                building_link = string(file)
                # print(building_link)
    # assert int4(file) == 0, "CAPTURE_LOCATION_SET has items"


def read_ef_line_list(file: BinaryIO):
    assert int4(file) == 0, "EF_LINE_LIST has items"


def read_go_outlines(file: BinaryIO):
    regions_amount = int4(file)
    # print('Go outlines: ', regions_amount)
    for i in range(regions_amount):
        point_amount = int4(file)
        points_list = []
        for j in range(point_amount):
            t = (float4(file), float4(file))
            points_list.append(t)
        # print(points_list)

    # assert int4(file) == 0, "GO_OUTLINES has items"


def read_non_terrain_outlines(file: BinaryIO):
    regions_amount = int4(file)
    # print('Non terrain outlines: ', regions_amount)
    for i in range(regions_amount):
        point_amount = int4(file)
        points_list = []
        for j in range(point_amount):
            t = (float4(file), float4(file))
            points_list.append(t)
        # print(points_list)

    # assert int4(file) == 0, "NON_TERRAIN_OUTLINES has items"


def read_zones_template_list(file: BinaryIO):
    version = int2(file)  # version
    # assert int4(file) == 0, "ZONES_TEMPLATE_LIST has items"
    # print('Version: ', version)
    amount = int4(file)
    # print('Amount: ', amount)
    for i in range(amount):
        points = int4(file)
        print('Points: ', points)
        points_list = []
        for j in range(points):
            t = (float4(file), float4(file))
            points_list.append(t)
        print(points_list)
        file.read(72)


def read_prefab_instance_list(file: BinaryIO):
    version = int2(file)  # version
    # print('Serrializer Version: ', version)
    prefab_amount = int4(file)
    # print('Prefabs amount: ', prefab_amount)
    for i in range(prefab_amount):
        prefab_version = int2(file)
        # print('Prefab serrializer Version: ', prefab_version)
        name = string(file)
        # print('Prefab name: ', name)
        # file.read(75)
        transformation_matrix = []
        i = 16
        while i > 0:
            matrix_element = float4(file)
            transformation_matrix.append(matrix_element)
            i = i - 1
        # print(transformation_matrix)
        property_overrides = int4(file)
        # print('Property overrides: ', property_overrides)
        for j in range(property_overrides):
            file.read(2)
            property_value = string(file)
            # print(property_value)
            file.read(14)
        file.read(7)
        height_mode = string(file)
        # print('Height mode: ', height_mode)


def read_bmd_outline_list(file: BinaryIO):
    version = int2(file)  # version
    # print(version)
    assert int4(file) == 0, "BMD_OUTLINE_LIST has items"


def read_particle_list(file: BinaryIO):
    assert_version('PARTICLE_EMITTER_LIST', 1, int2(file))
    return read_list(file, read_particle_instance)


def read_terrain_outlines(file: BinaryIO):
    assert int4(file) == 0, "TERRAIN_OUTLINES has items"


def read_lite_building_outlines(file: BinaryIO):
    assert int4(file) == 0, "LITE_BUILDING_OUTLINES has items"


def read_camera_zones(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "CAMERA_ZONES has items"


def read_civilian_deployment_list(file: BinaryIO):
    assert int4(file) == 0, "CIVILIAN_DEPLOYMENT_LIST has items"


def read_civilian_shelter_list(file: BinaryIO):
    assert int4(file) == 0, "CIVILIAN_SHELTER_LIST has items"


def read_prop_list(file: BinaryIO):
    assert_version('PROP_LIST', 2, int2(file))
    keys = read_list(file, read_prop_key_instance)
    props = read_list(file, read_prop_prop_instance)
    result = {}
    for key in keys:
        result[key] = []
    for prop in props:
        key = keys[prop.key_index]
        result[key].append(prop)
    return result


def read_prop_key_instance(file: BinaryIO):
    return string(file)


def read_prop_prop_instance(file: BinaryIO):
    # assert_version('PROP', 15, int2(file))

    version = int2(file)
    # print('Prop version: ', version)

    prop = Prop()
    prop.key_index = int2(file)
    file.read(2)  # TODO

    prop.coordinates = read_coordinates(file)
    # print(prop.coordinates)
    prop.translation = read_translation(file)
    # print(prop.translation)
    prop.scale = get_scale(prop.coordinates)
    # print(prop.scale)
    unscale(prop.coordinates, prop.scale)

    prop.decal = bool1(file)
    # print('Decal: ', prop.decal)
    file.read(7)  # flags from logic_decal to animated
    prop.decal_parallax_scale = float4(file)
    # print('Decal parallax: ', prop.decal_parallax_scale)
    prop.decal_tiling = float4(file)
    # print('Decal tiling: ', prop.decal_tiling)
    bool1(file)

    prop.flags = read_flags(file)

    bool1(file)
    bool1(file)
    bool1(file)
    bool1(file)
    prop.height_mode = string(file)
    # print('Height mode: ', prop.height_mode)
    if version == 15:
        strange_number = int8(file)
        # print('Strange number: ', strange_number)
        bool1(file)
        bool1(file)
    elif version == 14:
        strange_number = int4(file)
        # print('Strange number: ', strange_number)
        bool1(file)
        bool1(file)
    # print(int8(file))

    return prop


def read_particle_instance(file: BinaryIO):
    particle = Particle()
    version = int2(file)
    # print('Version: ', version)
    # assert_version('PARTICLE_EMITTER', 5, version)
    particle.model_name = string(file)
    # print('Particle name: ', particle.model_name)

    particle.coordinates = read_coordinates(file)
    # print(particle.coordinates)
    particle.position = read_translation(file)
    # print(particle.position)
    file.read(6)  # to be translated

    particle.flags = read_flags(file)
    # print(particle.flags)
    particle.object_relation = string(file)
    # print(particle.object_relation)
    if (version == 5):
        file.read(4)
        particle.autoplay = bool1(file)
        # print('Autoplay: ', particle.autoplay)
        particle.visible_in_shroud = bool1(file)
    elif (version == 6):
        file.read(8)
        particle.autoplay = bool1(file)
        # print('Autoplay: ', particle.autoplay)
        particle.visible_in_shroud = bool1(file)
    return particle


def read_ai_hints(file: BinaryIO):
    version = int2(file)  # version
    # print('Version: ', version)

    # separators
    separators_version = int2(file)
    separators_amount = int4(file)
    # print('Separators: ', separators_version, separators_amount)

    # directed_points
    directed_points_version = int2(file)
    directed_points_amount = int4(file)
    # print('Directed points: ', directed_points_version, directed_points_amount)

    # polylines
    polylines_version = int2(file)
    polylines_amount = int4(file)
    # print('Polylines: ', polylines_version, polylines_amount)
    for i in range(polylines_amount):
        polyline_version = int2(file)
        polyline_type = string(file)
        # print(polyline_version, polyline_type)
        polyline_points_amount = int4(file)
        polyline_points_list = []
        for j in range(polyline_points_amount):
            t = (float4(file), float4(file))
            polyline_points_list.append(t)
        # print(polyline_points_list)
    polylines_list_version = int2(file)
    polylines_list_amount = int4(file)
    # print('Polylines list: ', polylines_list_version, polylines_list_amount)
    # assert int4(file) == 0, "AI_HINTS has items"


def read_light_probe_list(file: BinaryIO):
    version = int2(file)  # version
    amount = int4(file)
    # print('Lightprobe: ', version, amount)
    for i in range(amount):
        light_probe_version = int2(file)
        t = (float4(file), float4(file), float4(file))
        radius = float4(file)
        is_primary = bool1(file)
        height_mode = string(file)
        # print(t, radius, is_primary, height_mode)
    # assert int4(file) == 0, "LIGHT_PROBE_LIST has items"


def read_terrain_stencil_triangle_list(file: BinaryIO):
    version = int2(file)  # version
    terrain_stencil_triangles = int4(file)
    for i in range(terrain_stencil_triangles):
        terrain_stencil_triangle_version = int2(file)
        position0 = (float4(file), float4(file), float4(file))
        position1 = (float4(file), float4(file), float4(file))
        position2 = (float4(file), float4(file), float4(file))
        height_mode = string(file)
        # print(terrain_stencil_triangle_version, position0, position1, position2, height_mode)

    # assert int4(file) == 0, "TERRAIN_STENCIL_TRIANGLE_LIST has items"


def read_point_light_list(file: BinaryIO):
    version = int2(file)  # version
    point_lights = int4(file)
    # print("Point lights: ", version, point_lights)
    for i in range(point_lights):
        point_ligh_version = int2(file)
        position = (float4(file), float4(file), float4(file))
        radius = float4(file)
        colour = (float4(file), float4(file), float4(file))
        colour_scale = float4(file)
        # file.read(9)
        animation_type= int1(file)
        params = (float4(file), float4(file))
        # animation_type = float4(file)
        colour_min = float4(file)
        random_offset = float4(file)
        falloff_type = string(file)
        lf_relative = bool1(file)
        height_mode = string(file)
        light_probes_only = bool1(file)
        pdlc_mask = int8(file)
        # print(point_ligh_version, position, radius, colour, colour_scale, animation_type, params, colour_min, random_offset, falloff_type, height_mode, pdlc_mask)
    # assert int4(file) == 0, "POINT_LIGHT_LIST has items"


def read_building_projectile_emitter_list(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "BUILDING_PROJECTILE_EMITTER_LIST has items"


def read_playable_area(file: BinaryIO):
    version = int2(file)  # version
    # print('Version: ', version)
    min_x = float4(file)
    min_y = float4(file)
    max_x = float4(file)
    max_y = float4(file)
    # print(min_x, min_y, max_x, max_y)
    has_been_set = bool1(file)
    valid_location_flags_version = int2(file)
    valid_north = bool1(file)
    valid_south = bool1(file)
    valid_east = bool1(file)
    valid_west = bool1(file)
    # print(valid_location_flags_version, valid_north, valid_south, valid_east, valid_west)
    # assert int4(file) == 0, "PLAYABLE_AREA has items"


def read_custom_material_mesh_list(file: BinaryIO):
    version = int2(file)  # version
    custom_material_mesh_list_amount = int4(file)
    # print('Version: ', version, custom_material_mesh_list_amount)
    for i in range(custom_material_mesh_list_amount):
        custom_material_mesh_version = int2(file)
        vertices_amount = int4(file)
        vertex_list = []
        for j in range(vertices_amount):
            t = (float4(file), float4(file), float4(file))
            vertex_list.append(t)
        # print(vertex_list)
        indices_amount = int4(file)
        indices_list = []
        for j in range(indices_amount):
            indices_list.append(int2(file))
        # print(indices_list)
        material = string(file)
        # print(material)
        height_mode = string(file)

    # assert int4(file) == 0, "CUSTOM_MATERIAL_MESH_LIST has items"


def read_terrain_stencil_blend_triangle_list(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "TERRAIN_STENCIL_BLEND_TRIANGLE_LIST has items"


def read_spot_light_list(file: BinaryIO):
    version = int2(file)  # version
    spot_lights = int4(file)
    print("Spot lights: ", version, spot_lights)
    for i in range(spot_lights):
        spot_light_version = int2(file)
        position = (float4(file), float4(file), float4(file))
        end = (float4(file), float4(file), float4(file), float4(file))
        length = float4(file)
        inner_angle = float4(file)
        outer_angle = float4(file)
        colour = (float4(file), float4(file), float4(file))
        falloff = float4(file)
        file.read(3)
        # gobo = string(file)
        height_mode = string(file)
        pdlc_mask = int8(file)
        print(spot_light_version, position, end, length, inner_angle, outer_angle, colour, falloff, height_mode, pdlc_mask)

    # assert int4(file) == 0, "SPOT_LIGHT_LIST has items"


def read_sound_shape_list(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "SOUND_SHAPE_LIST has items"


def read_composite_scene_list(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "COMPOSITE_SCENE_LIST has items"


def read_deployment_list(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "DEPLOYMENT_LIST has items"


def read_bmd_catchment_area_list(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "BMD_CATCHMENT_AREA_LIST has items"


def read_tree_list_reference_list(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "TREE_LIST_REFERENCE_LIST has items"


def read_grass_list_reference_list(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "GRASS_LIST_REFERENCE_LIST has items"



def read_flags(file: BinaryIO):
    assert_version('PARTICLE_EMITTER->flags', 2, int2(file))
    return {
        'allow_in_outfield': bool1(file),
        'clamp_to_surface': bool1(file),
        'clamp_to_water_surface': bool1(file),
        'spring': bool1(file),
        'summer': bool1(file),
        'autumn': bool1(file),
        'winter': bool1(file)
    }


def read_coordinates(file: BinaryIO):
    coordinates = [[None] * 3 for i in range(3)]
    for i in range(9):
        coordinates[i // 3][i % 3] = float4(file)
    return coordinates


def read_translation(file: BinaryIO):
    translation = [None] * 3
    for i in range(3):
        translation[i] = float4(file)
    return translation


def get_scale(coordinates):
    return list(map(mod_vector, coordinates))


def unscale(coordinates, scales):
    for i in range(3):
        for j in range(3):
            coordinates[i][j] /= scales[i]
