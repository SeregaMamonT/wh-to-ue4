from wh_terry_objects import TerryBuilding, ECTransform, ECMeshRenderSettings, ECTerrainClamp, TerryParticle, \
    ECBattleProperties, TerryDecal, TerryPropBuilding
from typing import BinaryIO, List
from wh_binary_objects import Building, Particle, Prop

from matrix import get_angles_deg, transpose, get_angles_deg_XYZ, get_angles_deg_XZY, get_angles_XYZ, get_angles_XZY, \
    degrees_tuple


def mod_vector(vector: List):
    return sum([x * x for x in vector]) ** 0.5


def convert_building(building: Building) -> TerryBuilding:
    terry_building = TerryBuilding()
    terry_building.ectransform = ECTransform()
    terry_building.ecmeshrendersettings = ECMeshRenderSettings()
    terry_building.ecterrainclamp = ECTerrainClamp()
    terry_building.flags = {}
    terry_building.key = building.building_key

    terry_building.damage = int(building.starting_damage_unary * 100)
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
    terry_building.ecmeshrendersettings.cast_shadow = building.flags["cast_shadows"]
    terry_building.flags["indestructible"] = building.flags["indestructible"]
    terry_building.flags["toggleable"] = building.flags["toggleable"]
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
