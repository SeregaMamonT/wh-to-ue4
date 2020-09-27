from wh_binary_objects import Building, Prop, Particle, Tree

from ue4_objects import UnrealStaticMeshCopy, RelativeLocation, RelativeRotation, RelativeScale3D, UnrealDecalCopy, \
    UnrealStaticMesh, Quaternion, Transform, UnrealDecal, UnrealParticle

from app_typing import Matrix, Vector

from wh_binary_to_terry_convertor import mod_vector, unscale

from matrix import transpose, get_angles_XZY_new, degrees
from typing import List
from math import cos, sin, radians


def to_quaternion(pitch: float, yaw: float, roll: float) -> Quaternion:
    # yaw (Z), pitch (Y), roll (X)

    # Abbreviations for the various angular functions
    cy = cos(radians(yaw * 0.5))
    sy = sin(radians(yaw * 0.5))
    cp = cos(radians(pitch * 0.5))
    sp = sin(radians(pitch * 0.5))
    cr = cos(radians(roll * 0.5))
    sr = sin(radians(roll * 0.5))

    x = cr * sp * sy - sr * cp * cy
    y = -cr * sp * cy - sr * cp * sy
    z = cr * cp * sy - sr * sp * cy
    w = cr * cp * cy + sr * sp * sy

    q = Quaternion(x, y, z, w)

    return q


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
    if building.properties.starting_damage_unary < 1:
        static_mesh.name = "{0}_{1}".format(building.building_key, index)
        static_mesh.static_mesh = 'StaticMesh\'{0}/{1}\''.format(directory, building.building_key)
    else:
        static_mesh.name = "{0}_broken_{1}".format(building.building_key, index)
        static_mesh.static_mesh = 'StaticMesh\'{0}/{1}_broken\''.format(directory, building.building_key)
    transform = get_transforms(building.transform)
    static_mesh.transform = Transform()
    static_mesh.transform.Translation = transform[0]
    static_mesh.transform.Rotation = to_quaternion(transform[1].X, transform[1].Y, transform[1].Z)
    static_mesh.transform.Scale3D = transform[2]
    # print(static_mesh.__dict__)

    return static_mesh


def convert_decal(decal: Prop, index: int, directory: str) -> UnrealDecal:
    unreal_decal = UnrealDecal()
    s = decal.key[decal.key.rfind('/') + 1:].split('.')[0]
    unreal_decal.name = "{0}_{1}_GEN_VARIABLE".format(s, index)

    unreal_decal.material = "Material\'{0}/{1}.{1}\'".format(directory, s)
    unreal_decal.tiling = decal.decal_tiling + 1
    unreal_decal.parallax_scale = decal.decal_parallax_scale
    transform = get_transforms(decal.transform)
    unreal_decal.transform = Transform()
    unreal_decal.transform.Translation = transform[0]
    unreal_decal.transform.Rotation = to_quaternion(transform[1].X, transform[1].Y, transform[1].Z)
    unreal_decal.transform.Scale3D = transform[2]
    unreal_decal.transform.Scale3D.Z = unreal_decal.transform.Scale3D.X

    return unreal_decal


def convert_particle(particle: Particle, index: int, directory: str) -> UnrealParticle:
    unreal_particle = UnrealParticle()
    unreal_particle.name = "{0}_{1}".format(particle.model_name, index)
    unreal_particle.particle = "ParticleSystem\'{0}/{1}.{1}\'".format(directory, particle.model_name)
    transform = get_transforms(particle.transform)
    unreal_particle.transform = Transform()
    unreal_particle.transform.Translation = transform[0]
    unreal_particle.transform.Rotation = to_quaternion(transform[1].X, transform[1].Y, transform[1].Z)
    unreal_particle.transform.Scale3D = transform[2]

    return unreal_particle


def convert_tree(tree: Tree, directory: str) -> List[UnrealStaticMesh]:
    unreal_tree_list = []
    for tree_prop in tree.props:
        unreal_tree = UnrealStaticMesh()
        temp_string = tree.key.replace('BattleTerrain/vegetation/', '')
        temp_string = temp_string.replace('.rigid_model_v2', '')
        # unreal_tree.name = temp_string
        unreal_tree.name = temp_string
        unreal_tree.static_mesh = 'StaticMesh\'{0}/{1}\''.format(directory, temp_string)
        unreal_tree.transform = Transform()
        unreal_tree.transform.Rotation = Quaternion(0, 0, 0, 1)
        unreal_tree.transform.Scale3D = RelativeScale3D(tree_prop.scale, tree_prop.scale, tree_prop.scale)
        unreal_tree.transform.Translation = RelativeLocation(-tree_prop.position.x * 100, tree_prop.position.z * 100,
                                                             tree_prop.position.y * 100)
        unreal_tree_list.append(unreal_tree)

    return unreal_tree_list


# convertor for copy-paste into unreal method
def convert_building_copy(building: Building, index: int, directory: str) -> UnrealStaticMeshCopy:
    static_mesh = UnrealStaticMeshCopy()
    static_mesh.name = "{0}_{1}_GEN_VARIABLE".format(building.building_key, index)
    # print(static_mesh.name)
    static_mesh.static_mesh = 'StaticMesh=StaticMesh\'"{0}/{1}.{1}"\''.format(directory, building.building_key)
    transform = get_transforms(building.transform)
    static_mesh.relative_location = transform[0]
    static_mesh.relative_rotation = transform[1]
    static_mesh.relative_scale_3d = transform[2]

    return static_mesh


def convert_decal_copy(decal: Prop, index: int, directory: str) -> UnrealDecalCopy:
    unreal_decal = UnrealDecalCopy()
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
