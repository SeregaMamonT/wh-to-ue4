from wh_terry_objects import TerryBuilding, ECTransform, ECMeshRenderSettings, ECTerrainClamp, TerryParticle, \
    ECBattleProperties, TerryDecal, TerryPropBuilding, TerryPrefabInstance, TerryTree, TerryCustomMaterialMesh, \
    TerryTerrainHole, TerryLightProbe, TerryPointLight, TerryPlayableArea, TerrySpotLight, TerrySoundShape, \
    TerryCompositeScene, Scale3D, Rotation3D, TerryBuildingProjectileEmitter, TerryZoneTemplate, ECPolyline, \
    TerryRegion, TerryRiver, TerrySplinePoint

from typing import BinaryIO, List
from app_typing import Matrix, Vector

from wh_binary_objects import Building, Particle, Prop, PrefabInstance, Tree, CustomMaterialMesh, Point2D, \
    TerrainStencilTriangle, LightProbe, PointLight, ColourRGBA, PlayableArea, SpotLight, SoundShape, Point3D, \
    CompositeScene, BuildingProjectileEmitter, ZoneTemplate, Outline

from matrix import transpose, get_angles_XYZ, get_angles_from_direction, get_angles

from math import cos, sin, radians, pi, asin, degrees, atan2, sqrt


def mod_vector(vector: List):
    return sum([x * x for x in vector]) ** 0.5


def unscale(transform: Matrix, scale: Vector):
    unscaled_transform = copy_matrix(transform)
    for i in range(3):
        for j in range(3):
            unscaled_transform[i][j] /= scale[i]

    return unscaled_transform


def copy_matrix(matrix: Matrix) -> Matrix:
    return list(map(lambda row: row.copy(), matrix))


def get_transforms(transform: Matrix):
    position = Point3D(*transform[3])
    scale = Scale3D(*map(mod_vector, transform[0:3]))
    rotation_matrix = unscale(transform[0:3], scale.as_vector())
    rotation = Rotation3D(*map(degrees, get_angles(transpose(rotation_matrix))))

    return position, rotation, scale


def get_transforms_4_4(transformation: Matrix):
    position = Point3D(*transformation[3][:3])
    coordinates = transformation[:3]
    scale = Scale3D(*map(mod_vector, coordinates))
    coordinates = unscale(coordinates, scale.as_vector())
    rotation = Rotation3D(*map(lambda angle: -degrees(angle), get_angles_XYZ(coordinates)))

    return position, rotation, scale


def convert_building(building: Building) -> TerryBuilding:
    terry_building = TerryBuilding()
    terry_building.ecmeshrendersettings = ECMeshRenderSettings(building.properties.flags["cast_shadows"])
    terry_building.ecterrainclamp = ECTerrainClamp()
    terry_building.flags = {}
    terry_building.key = building.building_key
    terry_building.damage = int(building.properties.starting_damage_unary * 100)
    terry_building.ectransform = ECTransform(*get_transforms(building.transform))
    terry_building.flags["indestructible"] = building.properties.flags["indestructible"]
    terry_building.flags["toggleable"] = building.properties.flags["toggleable"]
    terry_building.flags["export_as_prop"] = False
    terry_building.flags["allow_in_outfield_as_prop"] = False

    return terry_building


def convert_particle(particle: Particle) -> TerryParticle:
    terry_particle = TerryParticle()
    terry_particle.ecterrainclamp = ECTerrainClamp()
    terry_particle.ecbattleproperties = ECBattleProperties()
    terry_particle.vfx = particle.model_name
    terry_particle.ectransform = ECTransform(*get_transforms(particle.transform))

    return terry_particle


def convert_decal(prop: Prop) -> TerryDecal:
    terry_decal = TerryDecal()
    terry_decal.ecterrainclamp = ECTerrainClamp()
    terry_decal.ecbattleproperties = ECBattleProperties()
    if prop.flags["decal_override_gbuffer_normal"] == True:
        terry_decal.normal_mode = "DNM_DECAL_OVERRIDE"
    else:
        terry_decal.normal_mode = "DNM_BLEND"
    terry_decal.flags = {}
    terry_decal.flags["apply_to_terrain"] = prop.flags["decal_apply_to_terrain"]
    terry_decal.flags["apply_to_objects"] = prop.flags["decal_apply_to_gbuffer_objects"]
    terry_decal.flags["render_above_snow"] = prop.flags["decal_render_above_snow"]
    terry_decal.model_path = prop.key
    terry_decal.parallax_scale = prop.decal_parallax_scale
    terry_decal.tiling = int(prop.decal_tiling)
    terry_decal.ectransform = ECTransform(*get_transforms(prop.transform))
    # print(prop.flags)
    terry_decal.ecterrainclamp.terrain_oriented = True

    return terry_decal


def convert_prop_building(prop: Prop) -> TerryPropBuilding:
    terry_prop_building = TerryPropBuilding()
    terry_prop_building.ecterrainclamp = ECTerrainClamp()
    terry_prop_building.ecbattleproperties = ECBattleProperties()
    terry_prop_building.ecmeshrendersettings = ECMeshRenderSettings(True)
    terry_prop_building.model_path = prop.key
    terry_prop_building.ectransform = ECTransform(*get_transforms(prop.transform))

    terry_prop_building.ecmeshrendersettings.cast_shadow = True

    return terry_prop_building


def convert_prefab_instance(prefab: PrefabInstance) -> TerryPrefabInstance:
    terry_prefab_instance = TerryPrefabInstance()

    terry_prefab_instance.ecterrainclamp = ECTerrainClamp()
    terry_prefab_instance.key = prefab.name.replace('prefabs/', '').replace(".bmd", '')

    # transform
    position = Point3D(*prefab.transformation[3][:3])
    coordinates = prefab.transformation[:3]
    scale = Scale3D(*map(mod_vector, coordinates))
    coordinates = unscale(coordinates, scale.as_vector())
    rotation = Rotation3D(*map(lambda angle: -degrees(angle), get_angles_XYZ(coordinates)))

    terry_prefab_instance.ectransform = ECTransform(position, rotation, scale)

    return terry_prefab_instance


def convert_tree_instance(tree: Tree) -> List[TerryTree]:
    terry_tree_list = []
    for tree_prop in tree.props:
        terry_tree = TerryTree()
        temp_string = tree.key.replace('BattleTerrain/vegetation/', '')
        temp_string = temp_string.replace('.rigid_model_v2', '')
        terry_tree.key = temp_string
        terry_tree.ecterrainclamp = ECTerrainClamp()
        terry_tree.ectransform = ECTransform(tree_prop.position, Rotation3D(0, 0, 0),
                                             Scale3D(tree_prop.scale, tree_prop.scale, tree_prop.scale))

        terry_tree_list.append(terry_tree)

    return terry_tree_list


def convert_custom_material_mesh(custom_material_mesh: CustomMaterialMesh) -> TerryCustomMaterialMesh:
    terry_custom_material_mesh = TerryCustomMaterialMesh()
    terry_custom_material_mesh.polyline = []
    terry_custom_material_mesh.material = custom_material_mesh.material
    # calculate tranform from first vertex
    terry_custom_material_mesh.ectransform = ECTransform(custom_material_mesh.vertices[0], Rotation3D(0, 0, 0),
                                                         Scale3D(1, 1, 1))
    # subtract position from poluline points
    for i in custom_material_mesh.vertices:
        x = i.x - custom_material_mesh.vertices[0].x
        y = i.z - custom_material_mesh.vertices[0].z
        point = Point2D(x, y)
        # print(point.__dict__)
        terry_custom_material_mesh.polyline.append(point)

    return terry_custom_material_mesh


def convert_light_probe(light_probe: LightProbe) -> TerryLightProbe:
    terry_light_probe = TerryLightProbe()
    terry_light_probe.radius = int(light_probe.radius)
    terry_light_probe.is_primary = light_probe.is_primary
    terry_light_probe.ectransform = ECTransform(light_probe.position, Rotation3D(0, 0, 0), Scale3D(1, 1, 1))

    return terry_light_probe


animation_type = {
    0: "LAT_NONE",
    1: "LAT_RADIUS_SIN",
    2: "LAT_RADIUS_SIN_SIN",
}


def convert_point_light(point_light: PointLight) -> TerryPointLight:
    terry_point_light = TerryPointLight()
    terry_point_light.radius = point_light.radius
    terry_point_light.colour_scale = point_light.colour_scale
    terry_point_light.animation_type = animation_type[point_light.animation_type]
    terry_point_light.colour_min = point_light.colour_min
    terry_point_light.random_offset = point_light.random_offset
    terry_point_light.falloff_type = point_light.falloff_type
    terry_point_light.for_light_probes_only = point_light.flags["light_probes_only"]
    terry_point_light.ectransform = ECTransform(point_light.position, Rotation3D(0, 0, 0), Scale3D(1, 1, 1))
    terry_point_light.animation_speed_scale = (int(point_light.params[0]), int(point_light.params[1]))
    terry_point_light.colour = ColourRGBA(int(point_light.colour.red * 255), int(point_light.colour.green * 255),
                                          int(point_light.colour.blue * 255), 255)

    return terry_point_light


def convert_playable_area(playable_area: PlayableArea) -> TerryPlayableArea:
    terry_playable_area = TerryPlayableArea()

    terry_playable_area.width = playable_area.max_x - playable_area.min_x
    terry_playable_area.height = playable_area.max_y - playable_area.min_y
    x = playable_area.min_x + (terry_playable_area.width / 2)
    z = playable_area.min_y + (terry_playable_area.height / 2)
    terry_playable_area.ectransform = ECTransform(Point3D(x, 0, z), Rotation3D(0, 0, 0), Scale3D(1, 1, 1))
    terry_playable_area.deployment_locations = []
    for key, value in playable_area.flags.items():
        if value:
            temp_string = key.replace('valid_', '').capitalize()
            terry_playable_area.deployment_locations.append(temp_string)

    return terry_playable_area


def convert_spot_light(spot_light: SpotLight) -> TerrySpotLight:
    terry_spot_light = TerrySpotLight()
    terry_spot_light.ectransform = ECTransform(spot_light.position, Rotation3D(0, 0, 0), Scale3D(1, 1, 1))
    # colours
    max_color = max(spot_light.colour.red, spot_light.colour.green, spot_light.colour.blue)
    terry_spot_light.intensity = max_color
    terry_spot_light.colour = ColourRGBA(int(spot_light.colour.red / max_color * 255),
                                         int(spot_light.colour.green / max_color * 255),
                                         int(spot_light.colour.blue / max_color * 255), 255)
    terry_spot_light.length = spot_light.length
    weird_constant = 57.2957549
    terry_spot_light.inner_angle = spot_light.inner_angle * weird_constant
    terry_spot_light.outer_angle = spot_light.outer_angle * weird_constant
    terry_spot_light.falloff = spot_light.falloff
    terry_spot_light.volumetric = spot_light.flags["volumetric"]
    terry_spot_light.gobo = spot_light.gobo

    return terry_spot_light


def convert_sound_shape(sound_shape: SoundShape) -> TerrySoundShape:
    terry_sound_shape = TerrySoundShape()
    terry_sound_shape.key = sound_shape.key
    terry_sound_shape.type = sound_shape.type
    if terry_sound_shape.type != "SST_RIVER":
        terry_sound_shape.ectransform = ECTransform(sound_shape.points[0], Rotation3D(0, 0, 0), Scale3D(1, 1, 1))
        position_x = sound_shape.points[0].x
        position_y = sound_shape.points[0].y
        position_z = sound_shape.points[0].z
        # subtract position from poluline points
        if terry_sound_shape.type == "SST_MULTI_POINT":
            terry_sound_shape.points_cloud = []
            for i in sound_shape.points:
                x = i.x - sound_shape.points[0].x
                y = i.y - sound_shape.points[0].y
                z = i.z - sound_shape.points[0].z
                point = Point3D(x, y, z)
                terry_sound_shape.points_cloud.append(point)
        else:
            terry_sound_shape.points = []
            for i in sound_shape.points:
                x = i.x - position_x
                y = i.z - position_z
                point = Point2D(x, y)
                terry_sound_shape.points.append(point)

    terry_sound_shape.radius = sound_shape.outer_radius

    return terry_sound_shape


def convert_river(sound_shape: SoundShape) -> TerryRiver:
    terry_river = TerryRiver()
    # setting default values for now
    terry_river.spline_closed = False
    terry_river.spline_step_size = 15
    terry_river.terrain_relative = True
    terry_river.reverse_direction = False
    position_x = sound_shape.river_nodes[0].vertex.x
    position_y = sound_shape.river_nodes[0].vertex.y
    position_z = sound_shape.river_nodes[0].vertex.z
    terry_river.ectransform = ECTransform(
        Point3D(position_x, position_y, position_z), Rotation3D(0, 0, 0), Scale3D(1, 1, 1))
    for river_node in sound_shape.river_nodes:
        width = river_node.width
        flow_speed = river_node.flow_speed
        position = Point3D(river_node.vertex.x - position_x, river_node.vertex.y - position_y,
                           river_node.vertex.z - position_z)
        # need to find a way how to calculate those values
        tangent_in = [0, 0, 0]
        tangent_out = [0, 0, 0]
        terrain_offset = 0
        alpha_fade = 1
        foam_amount = 0.1
        spline_point = TerrySplinePoint(position, tangent_in, tangent_out, width, terrain_offset, alpha_fade,
                                        flow_speed, foam_amount)
        terry_river.spline.append(spline_point)

    return terry_river


def convert_composite_scene(composite_scene: CompositeScene) -> TerryCompositeScene:
    terry_composite_scene = TerryCompositeScene()
    terry_composite_scene.path = composite_scene.scene_file
    terry_composite_scene.ectransform = ECTransform(*get_transforms(composite_scene.transform))
    terry_composite_scene.autoplay = composite_scene.flags["autoplay"]

    return terry_composite_scene


def convert_building_projectile_emitter(
        building_projectile_emitter: BuildingProjectileEmitter) -> TerryBuildingProjectileEmitter:
    terry_building_projectile_emitter = TerryBuildingProjectileEmitter()
    terry_building_projectile_emitter.building_index = building_projectile_emitter.building_index
    terry_building_projectile_emitter.ectransform = ECTransform(building_projectile_emitter.position,
                                                                Rotation3D(*map(degrees, get_angles_from_direction(
                                                                    building_projectile_emitter.direction))),
                                                                Scale3D(1, 1, 1))
    return terry_building_projectile_emitter


def convert_outline_to_polyline(outline: Outline):
    position_x = outline.points[0].x
    position_z = outline.points[0].y
    polyline = ECPolyline()
    polyline.closed = True
    polyline.polyline = []
    for point in outline.points:
        polyline.polyline.append(Point2D((point.x - position_x), (point.y - position_z)))
    position = Point3D(position_x, 0, position_z)

    return polyline, position


def convert_zone_template(zone_template: ZoneTemplate) -> TerryZoneTemplate:
    terry_zone_template = TerryZoneTemplate()
    terry_zone_template.ectransform = ECTransform(*get_transforms_4_4(zone_template.transformation))
    polyline_data = convert_outline_to_polyline(zone_template.outline)
    terry_zone_template.polyline = polyline_data[0]
    terry_zone_template.ectransform.position = polyline_data[1]
    terry_zone_template.locked = True
    # dont know what this mean, but it is standard for terry
    terry_zone_template.rank_distance = 3
    terry_zone_template.zone_skirt_distance = 3

    return terry_zone_template


def convert_region(outline: Outline) -> TerryRegion:
    terry_region = TerryRegion()
    region_data = convert_outline_to_polyline(outline)
    terry_region.polyline = region_data[0]
    terry_region.ectransform = ECTransform(region_data[1], Rotation3D(0, 0, 0), Scale3D(1, 1, 1))

    return terry_region


def convert_terrain_stencil_triangle(triangles: List[TerrainStencilTriangle]) -> TerryTerrainHole:
    # NEED WORK!!!!!
    terry_terrain_hole = TerryTerrainHole()
    terry_terrain_hole.ectransform = ECTransform()
    temp_triangles = triangles
    for trianlge in temp_triangles:
        temp_triangles.remove(trianlge)
        temp2_triangles = [trianlge]
        i = triangles[0]
        # for i in temp_triangles:
        if (trianlge.position1 == i.position1) or (trianlge.position2 == i.position2) or (
                trianlge.position3 == i.position3):
            temp2_triangles.append(i)
            temp_triangles.remove(i)
    print(temp2_triangles, )

    # terrain_stencil_triangle.

    return terry_terrain_hole
