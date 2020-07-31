from wh_binary_objects import Building, Prop

from ue4_objects import UnrealStaticMesh, RelativeLocation, RelativeRotation, RelativeScale3D, UnrealDecal, \
    UnrealStaticMeshJson

from app_typing import Matrix, Vector

from wh_binary_to_terry_convertor import mod_vector, unscale

from matrix import transpose, get_angles_XZY_new, degrees


def get_transforms(transform: Matrix):
    x, z, y = map(lambda t: t * 100, transform[3])
    position = RelativeLocation(-x, y, z)

    scale_temp = [*map(mod_vector, transform[0:3])]
    rotation_matrix = unscale(transform[0:3], scale_temp)
    scale = RelativeScale3D(scale_temp[0], scale_temp[2], scale_temp[1])
    temp_rotation = [*map(degrees, get_angles_XZY_new(transpose(rotation_matrix)))]
    rotation = RelativeRotation(temp_rotation[0], temp_rotation[2], temp_rotation[1])

    return position, rotation, scale


def convert_building(building: Building, index: int, directory: str) -> UnrealStaticMesh:
    static_mesh = UnrealStaticMesh()
    static_mesh.name = "{0}_{1}_GEN_VARIABLE".format(building.building_key, index)
    # print(static_mesh.name)
    static_mesh.static_mesh = 'StaticMesh=StaticMesh\'"{0}/{1}.{1}"\''.format(directory, building.building_key)
    transform = get_transforms(building.transform)
    static_mesh.relative_location = transform[0]
    static_mesh.relative_rotation = transform[1]
    static_mesh.relative_scale_3d = transform[2]

    return static_mesh


def convert_building_json(building: Building, index: int, directory: str) -> UnrealStaticMeshJson:
    static_mesh = UnrealStaticMeshJson()
    static_mesh.Name = "{0}_{1}".format(building.building_key, index)
    # print(static_mesh.name)
    static_mesh.static_mesh = 'StaticMesh\'{0}/{1}\''.format(directory, building.building_key)
    transform = get_transforms(building.transform)
    static_mesh.location = transform[0]
    static_mesh.rotation = transform[1]
    static_mesh.scale = transform[2]

    return static_mesh


def convert_decal(decal: Prop, index: int, directory: str) -> UnrealDecal:
    unreal_decal = UnrealDecal()
    temp_string = decal.key.replace('rigidmodels/decals/wood elf/', '')
    temp_string = temp_string.replace('.rigid_model_v2', '')
    s = decal.key[decal.key.rfind('/') + 1:].split('.')[0]
    unreal_decal.name = "{0}_{1}_GEN_VARIABLE".format(s, index)
    unreal_decal.material = '\'"{0}/{1}.{1}"\''.format(directory, s)
    unreal_decal.tiling = decal.decal_tiling + 1
    unreal_decal.parallax_scale = decal.decal_parallax_scale
    transform = get_transforms(decal.transform)
    unreal_decal.relative_location = transform[0]
    unreal_decal.relative_rotation = transform[1]
    unreal_decal.relative_scale_3d = transform[2]
    unreal_decal.relative_scale_3d.Z = unreal_decal.relative_scale_3d.X

    return unreal_decal
