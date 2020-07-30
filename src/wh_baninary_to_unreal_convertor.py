from wh_binary_objects import Building

from ue4_objects import UnrealStaticMesh, RelativeLocation, RelativeRotation, RelativeScale3D

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
    print(static_mesh.name)
    static_mesh.static_mesh = 'StaticMesh=StaticMesh\'"{0}/{1}.{1}"\''.format(directory, building.building_key)
    transform = get_transforms(building.transform)
    static_mesh.relative_location = transform[0]
    static_mesh.relative_rotation = transform[1]
    static_mesh.relative_scale_3d = transform[2]

    return static_mesh
