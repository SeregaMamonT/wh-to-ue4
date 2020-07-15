from typing import BinaryIO, List, Any, Callable

from decorators import offset_error_logger
from wh_binary_objects import Particle, Prop
from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8

from wh_binary_objects import Prefab

from parsers.battlefield_building_list import read_building_list
from parsers.battlefield_building_list_far import read_building_list_far
from parsers.capture_location_set import read_capture_location_set
from parsers.ef_line_list import read_ef_line_list
from parsers.go_outlines import read_go_outlines
from parsers.non_terrain_outlines import read_non_terrain_outlines
from parsers.zones_template_list import read_zones_template_list
from parsers.prefab_instance_list import read_prefab_instance_list
from parsers.bmd_outline_list import read_bmd_outline_list
from parsers.terrain_outlines import read_terrain_outlines
from parsers.lite_building_outlines import read_lite_building_outlines
from parsers.camera_zones import read_camera_zones
from parsers.civilian_deployment_list import read_civilian_deployment_list
from parsers.civilian_shelter_list import read_civilian_shelter_list
from parsers.prop_list import read_prop_list
from parsers.particle_emitter_list import read_particle_list
from parsers.ai_hints import read_ai_hints


from parsers.light_probe_list import read_light_probe_list
from parsers.terrain_stencil_triangle_list import read_terrain_stencil_triangle_list
from parsers.point_light_list import read_point_light_list
from parsers.building_projectile_emitter_list import read_building_projectile_emitter_list
from parsers.playable_area import read_playable_area
from parsers.custom_material_mesh_list import read_custom_material_mesh_list
from parsers.terrain_stencil_blend_triangle_list import read_terrain_stencil_blend_triangle_list
from parsers.spot_light_list import read_spot_light_list
from parsers.sound_shape_list import read_sound_shape_list
from parsers.composite_scene_list import read_composite_scene_list
from parsers.deployment_list import read_deployment_list
from parsers.bmd_catchment_area_list import read_bmd_catchment_area_list
from parsers.prefab_vegetation import read_prefab_tree_list
from parsers.tree_list_reference_list import read_tree_list_reference_list
from parsers.grass_list_reference_list import read_grass_list_reference_list


@offset_error_logger
def parse_file(file: BinaryIO, global_context):
    global context
    context = global_context

    file.read(8)  # FASTBIN0
    root_version = int2(file)
    if root_version not in context:
        context.append(root_version)
    if root_version == 23 or root_version == 24:
        buildings = read_building_list(file)
        read_building_list_far(file)
        capture_location_set = read_capture_location_set(file)
        # for i in capture_location_set:
        #   for j in i:
        #        print(j.__dict__)
        read_ef_line_list(file)
        read_go_outlines(file)
        read_non_terrain_outlines(file)
        read_zones_template_list(file)
        prefab_instance_list = read_prefab_instance_list(file)
        # for i in prefab_instance_list:
        #  print(i.__dict__)
        read_bmd_outline_list(file)
        read_terrain_outlines(file)
        read_lite_building_outlines(file)
        read_camera_zones(file)
        read_civilian_deployment_list(file)
        read_civilian_shelter_list(file)
        props = read_prop_list(file)
        particles = read_particle_list(file)
        # for i in particles:
        #  print(i.__dict__)
        ai_hints = read_ai_hints(file)
        # print(ai_hints.__dict__)

        read_light_probe_list(file)
        read_terrain_stencil_triangle_list(file)
        point_light_list = read_point_light_list(file)
        # for i in point_light_list:
        #   print(i.__dict__)
        read_building_projectile_emitter_list(file)
        read_playable_area(file)
        # end of prefab!!!
        read_custom_material_mesh_list(file)
        read_terrain_stencil_blend_triangle_list(file)
        spot_light_list = read_spot_light_list(file)
        # for i in spot_light_list:
        #   print(i.__dict__)
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


@offset_error_logger
def read_prefab(file: BinaryIO, global_context):
    global context
    context = global_context

    file.read(8)  # FASTBIN0
    root_version = int2(file)
    if root_version not in context:
        context.append(root_version)
    if root_version == 23 or root_version == 24:
        prefab = Prefab()
        prefab.buildings = read_building_list(file)
        read_building_list_far(file)
        prefab.capture_locations = read_capture_location_set(file)
        read_ef_line_list(file)
        prefab.go_outlines = read_go_outlines(file)
        prefab.non_terrain_outlines = read_non_terrain_outlines(file)
        prefab.zones_templates = read_zones_template_list(file)
        prefab.prefab_instances = read_prefab_instance_list(file)
        read_bmd_outline_list(file)
        read_terrain_outlines(file)
        read_lite_building_outlines(file)
        read_camera_zones(file)
        read_civilian_deployment_list(file)
        read_civilian_shelter_list(file)
        prefab.props = read_prop_list(file)
        prefab.particles = read_particle_list(file)
        prefab.ai_hints = read_ai_hints(file)
        prefab.light_probes = read_light_probe_list(file)
        prefab.terrain_stencil_triangle = read_terrain_stencil_triangle_list(file)
        prefab.point_lights = read_point_light_list(file)
        prefab.building_projectile_emitters = read_building_projectile_emitter_list(file)
        prefab.playable_area = read_playable_area(file)
        # print(prefab.__dict__)
        return prefab.buildings

    else:
        raise Exception('Only versions 23, 24 of root are supported')


@offset_error_logger
def read_map(file: BinaryIO, global_context):
    global context
    context = global_context

    file.read(8)  # FASTBIN0
    root_version = int2(file)
    if root_version not in context:
        context.append(root_version)
    if root_version == 23 or root_version == 24:
        buildings = read_building_list(file)
        read_building_list_far(file)
        capture_location_set = read_capture_location_set(file)
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
        point_light_list = read_point_light_list(file)
        # for i in point_light_list:
        #   print(i.__dict__)
        emitters = read_building_projectile_emitter_list(file)
        area = read_playable_area(file)

        # end of prefab!!!
        read_custom_material_mesh_list(file)
        read_terrain_stencil_blend_triangle_list(file)
        spot_light_list = read_spot_light_list(file)
        # for i in spot_light_list:
        #   print(i.__dict__)
        read_sound_shape_list(file)
        read_composite_scene_list(file)
        read_deployment_list(file)
        read_bmd_catchment_area_list(file)
        print('Hooray it did not crash!')
        # only for version 24
        # read_tree_list_reference_list(file)
        # read_grass_list_reference_list(file)

        return buildings
    else:
        raise Exception('Only versions 2, 23, 24 of root are supported')


@offset_error_logger
def read_prefab_vegetation(file: BinaryIO):
    file.read(8)  # FASTBIN0
    assert_version('Vegetation', 2, int2(file))
    prefab_vegetation = read_prefab_tree_list(file)
    # for i in prefab_vegetation:
    #    print(i.__dict__)

@offset_error_logger
def read_tree_list(file: BinaryIO):
    file.read(8)  # FASTBIN0
    assert_version('Vegetation', 2, int2(file))
    # tree_list_version = int2(file)
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


@offset_error_logger
def read_vegetation(file: BinaryIO):
    file.read(8)  # FASTBIN0
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


