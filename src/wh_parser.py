from typing import BinaryIO, List, Any, Callable

from decorators import offset_error_logger
from wh_binary_objects import Particle, Prop
from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8

from wh_binary_objects import Prefab, MapData, Vegetation

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
from parsers.vegetation import read_prefab_vegetation_list, read_map_vegetation_list


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
        #print(print_prefab_stats(prefab))

        return prefab
    if root_version == 26:
        print(root_version, 'in progress')
        prefab = Prefab()
        prefab.buildings = read_building_list(file)

        #print(print_prefab_stats(prefab))


    else:
        raise Exception('Only versions 23, 24 of root are supported')


def print_map_stats(map: MapData):
    buildings = []
    for i in map.buildings:
        if i.building_key not in buildings:
            buildings.append(i.building_key)
    print("Buildings: ", len(map.buildings), "Unique: ", len(buildings))
    for i in buildings:
        print(i)
    print("Capture locations: ", len(map.capture_locations))
    print("Go outline: ", len(map.go_outlines))
    print("Non terrain outlines: ", len(map.non_terrain_outlines))
    print("Zones templates: ", len(map.zones_templates))
    prefabs = []
    for i in map.prefab_instances:
        if i.name not in prefabs:
            prefabs.append(i.name)
    prefabs.sort()
    print("Prefabs: ", len(map.prefab_instances), "Unique: ", len(prefabs))
    for i in prefabs:
        print(i)
    props_amount = 0
    for i in map.props.items():
        props_amount = props_amount + len(i)
    props = []
    for i in map.props.keys():
        if i not in props:
            props.append(i)
    print("Props: ", props_amount, "Unique: ", len(props))
    for i in props:
        print(i)
    particles = []
    for i in map.particles:
        if i.model_name not in particles:
            particles.append(i.model_name)
    print("Particles: ", len(map.particles), "Unique: ", len(particles))
    for i in particles:
        print(i)
    print("Ai hints: ", "Separators: ", len(map.ai_hints.separators), "Polylines: ",
          len(map.ai_hints.polylines))
    print("Light probes: ", len(map.light_probes))
    print("Terrain stencil triangles: ", len(map.terrain_stencil_triangle))
    print("Point lights: ", len(map.point_lights))
    print("Building projectile emitters: ", len(map.building_projectile_emitters))
    print("Spot lights: ", len(map.spot_lights))
    print("Sound shapes: ", len(map.sound_shapes))


def print_prefab_stats(prefab: Prefab):
    buildings = []
    for i in prefab.buildings:
        if i.building_key not in buildings:
            buildings.append(i.building_key)
    print("Buildings: ", len(prefab.buildings), "Unique: ", len(buildings))
    for i in buildings:
        print(i)
    prefabs = []
    for i in prefab.prefab_instances:
        if i.name not in prefabs:
            prefabs.append(i.name)
    print("Prefabs: ", len(prefab.prefab_instances), "Unique: ", len(prefabs))
    for i in prefabs:
        print(i)
    props_amount = 0
    for i in prefab.props.items():
        props_amount = props_amount + len(i)
    props = []
    for i in prefab.props.keys():
        if i not in props:
            props.append(i)
    print("Props: ", props_amount, "Unique: ", len(props))
    for i in props:
        print(i)
    particles = []
    for i in prefab.particles:
        if i.model_name not in particles:
            particles.append(i.model_name)
    print("Particles: ", len(prefab.particles), "Unique: ", len(particles))
    for i in particles:
        print(i)



@offset_error_logger
def read_map(file: BinaryIO, global_context):
    global context
    context = global_context

    file.read(8)  # FASTBIN0
    root_version = int2(file)
    if root_version not in context:
        context.append(root_version)
    if root_version == 23 or root_version == 24:
        map = MapData()
        map.buildings = read_building_list(file)
        read_building_list_far(file)
        map.capture_locations = read_capture_location_set(file)
        read_ef_line_list(file)
        map.go_outlines = read_go_outlines(file)
        map.non_terrain_outlines = read_non_terrain_outlines(file)
        map.zones_templates = read_zones_template_list(file)
        map.prefab_instances = read_prefab_instance_list(file)
        read_bmd_outline_list(file)
        read_terrain_outlines(file)
        read_lite_building_outlines(file)
        read_camera_zones(file)
        read_civilian_deployment_list(file)
        read_civilian_shelter_list(file)
        map.props = read_prop_list(file)
        map.particles = read_particle_list(file)
        map.ai_hints = read_ai_hints(file)
        map.light_probes = read_light_probe_list(file)
        map.terrain_stencil_triangle = read_terrain_stencil_triangle_list(file)
        map.point_lights = read_point_light_list(file)
        map.building_projectile_emitters = read_building_projectile_emitter_list(file)
        map.playable_area = read_playable_area(file)

        # only for map
        map.custom_material_meshes = read_custom_material_mesh_list(file)
        read_terrain_stencil_blend_triangle_list(file)
        map.spot_lights = read_spot_light_list(file)
        map.sound_shapes = read_sound_shape_list(file)
        map.composite_scenes = read_composite_scene_list(file)
        map.deployment = read_deployment_list(file)
        read_bmd_catchment_area_list(file)
        # print('Hooray it did not crash!')

        print_map_stats(map)

        return map
    else:
        raise Exception('Only versions 2, 23, 24 of root are supported')


@offset_error_logger
def read_prefab_vegetation(file: BinaryIO):
    file.read(8)  # FASTBIN0
    vegetation = Vegetation()
    vegetation.trees = read_prefab_vegetation_list(file)

    return vegetation


@offset_error_logger
def read_map_vegetation(file: BinaryIO):
    file.read(8)  # FASTBIN0
    map_vegetation = read_map_vegetation_list(file)

    return map_vegetation
    # for i in map_vegetation:
    #    print(i.__dict__)
