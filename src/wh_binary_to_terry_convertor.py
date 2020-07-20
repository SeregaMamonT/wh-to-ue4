from wh_terry_objects import TerryBuilding, ECTransform, ECMeshRenderSettings, ECTerrainClamp, TerryParticle, \
    ECBattleProperties, TerryDecal, TerryPropBuilding, TerryPrefabInstance, TerryTree, TerryCustomMaterialMesh, \
    TerryTerrainHole, TerryLightProbe, TerryPointLight, TerryPlayableArea, TerrySpotLight, TerrySoundShape, \
    TerryCompositeSecne

from typing import BinaryIO, List

from wh_binary_objects import Building, Particle, Prop, PrefabInstance, Tree, CustomMaterialMesh, Point2D, \
    TerrainStencilTriangle, LightProbe, PointLight, ColourRGBA, PlayableArea, SpotLight, SoundShape, Point3D, \
    CompositeScene

from matrix import get_angles_deg, transpose, get_angles_deg_XYZ, get_angles_deg_XZY, get_angles_XYZ, get_angles_XZY, \
    degrees_tuple


def mod_vector(vector: List):
    return sum([x * x for x in vector]) ** 0.5


def convert_building(building: Building) -> TerryBuilding:
    terry_building = TerryBuilding()
    terry_building.ectransform = ECTransform()
    terry_building.ecmeshrendersettings = ECMeshRenderSettings(building.properties.flags["cast_shadows"])
    terry_building.ecterrainclamp = ECTerrainClamp()
    terry_building.flags = {}
    terry_building.key = building.building_key

    terry_building.damage = int(building.properties.starting_damage_unary * 100)
    terry_building.ectransform.position = []

    for i in range(3):
        terry_building.ectransform.position.append(building.transform[i])

    coordinates = building.coordinates
    terry_building.ectransform.scale = list(map(mod_vector, coordinates))
    for i in range(3):
        scale = terry_building.ectransform.scale[i]
        for j in range(3):
            coordinates[i][j] /= scale
    terry_building.ectransform.rotation = degrees_tuple(get_angles_XYZ(transpose(coordinates)))
    terry_building.flags["indestructible"] = building.properties.flags["indestructible"]
    terry_building.flags["toggleable"] = building.properties.flags["toggleable"]
    terry_building.flags["export_as_prop"] = False
    terry_building.flags["allow_in_outfield_as_prop"] = False

    return terry_building


def convert_particle(particle: Particle) -> TerryParticle:
    terry_particle = TerryParticle()
    terry_particle.ectransform = ECTransform()
    terry_particle.ecterrainclamp = ECTerrainClamp()
    terry_particle.ecbattleproperties = ECBattleProperties()
    terry_particle.vfx = particle.model_name

    terry_particle.ectransform.position = []

    for i in range(3):
        terry_particle.ectransform.position.append(particle.position[i])

    coordinates = particle.coordinates
    terry_particle.ectransform.scale = list(map(mod_vector, coordinates))
    for i in range(3):
        scale = terry_particle.ectransform.scale[i]
        for j in range(3):
            coordinates[i][j] /= scale
    terry_particle.ectransform.rotation = degrees_tuple(get_angles_XYZ(transpose(coordinates)))

    return terry_particle


def convert_decal(prop: Prop) -> TerryDecal:
    terry_decal = TerryDecal()
    terry_decal.ectransform = ECTransform()
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
    terry_decal.ectransform.position = []

    for i in range(3):
        terry_decal.ectransform.position.append(prop.translation[i])

    coordinates = prop.coordinates
    terry_decal.ectransform.scale = list(map(mod_vector, coordinates))
    for i in range(3):
        scale = terry_decal.ectransform.scale[i]
        for j in range(3):
            coordinates[i][j] /= scale
    terry_decal.ectransform.rotation = degrees_tuple(get_angles_XYZ(transpose(coordinates)))
    # print(prop.flags)
    terry_decal.ecterrainclamp.terrain_oriented = True

    return terry_decal


def convert_prop_building(prop: Prop) -> TerryPropBuilding:
    terry_prop_building = TerryPropBuilding()
    terry_prop_building.ectransform = ECTransform()
    terry_prop_building.ecterrainclamp = ECTerrainClamp()
    terry_prop_building.ecbattleproperties = ECBattleProperties()
    terry_prop_building.ecmeshrendersettings = ECMeshRenderSettings()
    terry_prop_building.model_path = prop.key
    terry_prop_building.ectransform.position = []

    for i in range(3):
        terry_prop_building.ectransform.position.append(prop.translation[i])

    coordinates = prop.coordinates
    terry_prop_building.ectransform.scale = list(map(mod_vector, coordinates))
    for i in range(3):
        scale = terry_prop_building.ectransform.scale[i]
        for j in range(3):
            coordinates[i][j] /= scale
    terry_prop_building.ectransform.rotation = degrees_tuple(get_angles_XYZ(transpose(coordinates)))

    terry_prop_building.ecmeshrendersettings.cast_shadow = True

    return terry_prop_building


def convert_prefab_instance(prefab: PrefabInstance) -> TerryPrefabInstance:
    terry_prefab_instance = TerryPrefabInstance()
    terry_prefab_instance.ectransform = ECTransform()
    terry_prefab_instance.ecterrainclamp = ECTerrainClamp()
    temp_string = prefab.name.replace('prefabs/', '')
    temp_string = temp_string.replace(".bmd", '')
    terry_prefab_instance.key = temp_string
    terry_prefab_instance.ectransform.position = []

    # transform
    translation = []
    for i in range(3):
        translation.append(prefab.transformation[3][i])

    temp_coordinates = [[None] * 3 for i in range(3)]
    for i in range(9):
        temp_coordinates[i // 3][i % 3] = prefab.transformation[i // 3][i % 3]

    for i in range(3):
        terry_prefab_instance.ectransform.position.append(translation[i])

    coordinates = temp_coordinates
    terry_prefab_instance.ectransform.scale = list(map(mod_vector, coordinates))
    for i in range(3):
        scale = terry_prefab_instance.ectransform.scale[i]
        for j in range(3):
            coordinates[i][j] /= scale
    temp_angles = degrees_tuple(get_angles_XYZ(coordinates))
    terry_prefab_instance.ectransform.rotation = []
    for i in temp_angles:
        terry_prefab_instance.ectransform.rotation.append(-i)

    return terry_prefab_instance


def convert_tree_instance(tree: Tree) -> List[TerryTree]:
    terry_tree_list = []
    for i in tree.props:
        terry_tree = TerryTree()
        temp_string = tree.key.replace('BattleTerrain/vegetation/', '')
        temp_string = temp_string.replace('.rigid_model_v2', '')
        terry_tree.key = temp_string
        terry_tree.ecterrainclamp = ECTerrainClamp()
        terry_tree.ectransform = ECTransform()
        terry_tree.ectransform.position = []
        terry_tree.ectransform.rotation = []
        terry_tree.ectransform.scale = []
        terry_tree.ectransform.position.append(i.position[0])
        terry_tree.ectransform.position.append(i.position[1])
        terry_tree.ectransform.position.append(i.position[2])
        for j in range(3):
            terry_tree.ectransform.rotation.append(0)
        for j in range(3):
            terry_tree.ectransform.scale.append(i.scale)
        terry_tree_list.append(terry_tree)

    return terry_tree_list


def convert_custom_material_mesh(custom_material_mesh: CustomMaterialMesh) -> TerryCustomMaterialMesh:
    terry_custom_material_mesh = TerryCustomMaterialMesh()
    terry_custom_material_mesh.ectransform = ECTransform()
    terry_custom_material_mesh.polyline = []
    terry_custom_material_mesh.material = custom_material_mesh.material
    # calculate tranform from first vertex
    position_x = custom_material_mesh.vertices[0].x
    position_y = custom_material_mesh.vertices[0].y
    position_z = custom_material_mesh.vertices[0].z
    terry_custom_material_mesh.ectransform.position = [position_x, position_y, position_z]
    terry_custom_material_mesh.ectransform.rotation = [0, 0, 0]
    terry_custom_material_mesh.ectransform.scale = [1, 1, 1]
    # subtract position from poluline points
    for i in custom_material_mesh.vertices:
        x = i.x - position_x
        y = i.z - position_z
        point = Point2D(x, y)
        # print(point.__dict__)
        terry_custom_material_mesh.polyline.append(point)

    return terry_custom_material_mesh


def convert_light_probe(light_probe: LightProbe) -> TerryLightProbe:
    terry_light_probe = TerryLightProbe()
    terry_light_probe.ectransform = ECTransform()
    terry_light_probe.radius = int(light_probe.radius)
    terry_light_probe.is_primary = light_probe.is_primary
    terry_light_probe.ectransform.position = light_probe.position
    terry_light_probe.ectransform.rotation = [0, 0, 0]
    terry_light_probe.ectransform.scale = [1, 1, 1]

    return terry_light_probe


animation_type = {
    0: "LAT_NONE",
    1: "LAT_RADIUS_SIN",
    2: "LAT_RADIUS_SIN_SIN",
}


def convert_point_light(point_light: PointLight) -> TerryPointLight:
    terry_point_light = TerryPointLight()
    terry_point_light.ectransform = ECTransform()
    terry_point_light.radius = point_light.radius
    terry_point_light.colour_scale = point_light.colour_scale
    terry_point_light.animation_type = animation_type[point_light.animation_type]
    terry_point_light.colour_min = point_light.colour_min
    terry_point_light.random_offset = point_light.random_offset
    terry_point_light.ectransform.position = point_light.position
    terry_point_light.falloff_type = point_light.falloff_type
    terry_point_light.for_light_probes_only = point_light.flags["light_probes_only"]
    terry_point_light.ectransform.position = point_light.position
    terry_point_light.animation_speed_scale = (int(point_light.params[0]), int(point_light.params[1]))
    terry_point_light.ectransform.rotation = [0, 0, 0]
    terry_point_light.ectransform.scale = [1, 1, 1]
    terry_point_light.colour = ColourRGBA(int(point_light.colour.red * 255), int(point_light.colour.green * 255),
                                          int(point_light.colour.blue * 255), 255)

    return terry_point_light


def convert_playable_area(playable_area: PlayableArea) -> TerryPlayableArea:
    terry_playable_area = TerryPlayableArea()
    terry_playable_area.ectransform = ECTransform()
    terry_playable_area.width = playable_area.max_x - playable_area.min_x
    terry_playable_area.height = playable_area.max_y - playable_area.min_y
    x = playable_area.min_x + (terry_playable_area.width / 2)
    z = playable_area.min_y + (terry_playable_area.height / 2)
    terry_playable_area.ectransform.position = [x, 0, z]
    terry_playable_area.ectransform.rotation = [0, 0, 0]
    terry_playable_area.ectransform.scale = [1, 1, 1]
    terry_playable_area.deployment_locations = []
    for key, value in playable_area.flags.items():
        if value:
            temp_string = key.replace('valid_', '').capitalize()
            terry_playable_area.deployment_locations.append(temp_string)

    return terry_playable_area


def convert_spot_light(spot_light: SpotLight) -> TerrySpotLight:
    terry_spot_light = TerrySpotLight()
    terry_spot_light.ectransform = ECTransform()
    terry_spot_light.ectransform.position = spot_light.position
    terry_spot_light.ectransform.rotation = [0, 0, 0]
    terry_spot_light.ectransform.scale = [1, 1, 1]
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
    terry_sound_shape.ectransform = ECTransform()
    terry_sound_shape.key = sound_shape.key
    terry_sound_shape.type = sound_shape.type
    if terry_sound_shape.type != "SST_RIVER":
        position_x = sound_shape.points[0].x
        position_y = sound_shape.points[0].y
        position_z = sound_shape.points[0].z
        terry_sound_shape.ectransform.position = [position_x, position_y, position_z]
        terry_sound_shape.ectransform.rotation = [0, 0, 0]
        terry_sound_shape.ectransform.scale = [1, 1, 1]
        # subtract position from poluline points
        if terry_sound_shape.type == "SST_MULTI_POINT":
            terry_sound_shape.points_cloud = []
            for i in sound_shape.points:
                x = i.x - position_x
                y = i.y - position_y
                z = i.z - position_z
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


def convert_composite_scene(composite_scene: CompositeScene) -> TerryCompositeSecne:
    terry_composite_scene = TerryCompositeSecne()
    terry_composite_scene.ectransform = ECTransform()
    terry_composite_scene.path = composite_scene.scene_file
    terry_composite_scene.ectransform.position = []
    for i in range(3):
        terry_composite_scene.ectransform.position.append(composite_scene.transform[i])

    coordinates = composite_scene.coordinates
    terry_composite_scene.ectransform.scale = list(map(mod_vector, coordinates))
    for i in range(3):
        scale = terry_composite_scene.ectransform.scale[i]
        for j in range(3):
            coordinates[i][j] /= scale
    terry_composite_scene.ectransform.rotation = degrees_tuple(get_angles_XYZ(transpose(coordinates)))
    terry_composite_scene.autoplay = composite_scene.flags["autoplay"]
    
    return terry_composite_scene


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
