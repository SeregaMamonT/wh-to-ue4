from wh_baninary_to_unreal_convertor import convert_building_copy, convert_decal_copy, convert_building, convert_decal, \
    convert_particle
from enum import Enum
from terry_savers.xml_saver_utils import s_float
from ue4_objects import UnrealStaticMeshCopy, RelativeLocation, RelativeRotation, RelativeScale3D, UnrealDecalCopy
from wh_binary_objects import Prefab, MapData

import json


class Ue4StructureType(Enum):
    PREFAB = 1
    MAP = 2


def ue4_saver(filename: str, object: tuple, type: Ue4StructureType):
    get_type_saver(type)(filename, object)


def get_type_saver(type):
    if type in ue4_savers:
        return ue4_savers[type]
    else:
        raise Exception('Unsupported save type: ' + str(type))


def save_json(content, filename):
    # content = json.dumps(data, indent=4, sort_keys=True)
    save_to_file(content, filename + ".json")


def save_relative_location(relative_location: RelativeLocation) -> str:
    x = relative_location.X
    y = relative_location.Y
    z = relative_location.Z
    content = '\tRelativeLocation=(X={0},Y={1},Z={2})\n'.format(s_float(x), s_float(y), s_float(z))

    return content


def save_relative_rotation(relative_rotation: RelativeRotation) -> str:
    pitch = relative_rotation.X
    yaw = relative_rotation.Y
    roll = relative_rotation.Z
    # pitch = relative_rotation.Pitch
    # yaw = relative_rotation.Yaw
    # roll = relative_rotation.Roll
    content = '\tRelativeRotation=(Pitch={0},Yaw={1},Roll={2})\n'.format(s_float(pitch), s_float(yaw), s_float(roll))

    return content


def save_relative_scale3d(relative_scale_3d: RelativeScale3D) -> str:
    scale_x = relative_scale_3d.X
    scale_y = relative_scale_3d.Y
    scale_z = relative_scale_3d.Z
    content = '\tRelativeScale3D = (X={0}, Y={1}, Z={2})\n'.format(s_float(scale_x), s_float(scale_y), s_float(scale_z))

    return content


def save_static_mesh(static_mesh: UnrealStaticMeshCopy) -> str:
    content = 'Begin Object Class=/Script/Engine.StaticMeshComponent '
    content += 'Name="{0}"\n'.format(static_mesh.name)
    content += static_mesh.static_mesh
    content += '\tStaticMeshImportVersion=1\n'
    content += save_relative_location(static_mesh.relative_location)
    content += save_relative_rotation(static_mesh.relative_rotation)
    content += save_relative_scale3d(static_mesh.relative_scale_3d)
    content += 'End Object\n'

    return content


def save_decal(decal: UnrealDecalCopy) -> str:
    content = 'Begin Object Class=/Script/Engine.ChildActorComponent '
    content += 'Name="{0}"\n'.format(decal.name)
    content += 'Begin Object Class=/Game/Environment/DEcals/wh_decal_bp.wh_decal_bp_C '
    content += 'Name="{0}_wh_decal_bp_C_CAT"\n'.format(decal.name)
    content += 'End Object\n'
    content += 'Begin Object Name="{0}_wh_decal_bp_C_CAT"\n'.format(decal.name)
    content += 'Decal_Material=MaterialInstanceConstant'"{0}"'\n'.format(decal.material)
    content += 'Tiling={0}\n'.format(s_float(decal.tiling))
    content += 'Parallax Scale={0}\n'.format(s_float(decal.parallax_scale))
    content += 'End Object\n'
    content += 'ChildActorClass=BlueprintGeneratedClass\'"/Game/Environment/DEcals/wh_decal_bp.wh_decal_bp_C"\'\n'
    content += save_relative_location(decal.relative_location)
    content += save_relative_rotation(decal.relative_rotation)
    content += save_relative_scale3d(decal.relative_scale_3d)
    content += 'End Object\n'

    return content


def save_ue4_prefab_data(filename, prefab_data: tuple):
    prefab = prefab_data[0]
    dir = "/Game/Environment/meshes2"
    decal_dir = "/Game/Environment/DEcals/Materials"
    particle_dir = "/Game/Environment/particles"
    content = ""
    buildings_data = []
    for index, building in enumerate(prefab.buildings):
        buildings_data.append(convert_building(building, index, dir))
    decal_data = []
    for key, props in prefab.props.items():
        decals = filter(lambda prop: prop.decal, props)
        for index, decal in enumerate(decals):
            decal_data.append(convert_decal(decal, index, decal_dir))
    particle_data = []
    for index, particle in enumerate(prefab.particles):
        particle_data.append(convert_particle(particle, index, particle_dir))
    prefab_dict = {'Name': 'prefab', 'buildings': buildings_data, 'decals': decal_data, 'particles': particle_data}
    json_string = json.dumps([prefab_dict], default=lambda o: o.__dict__, indent=4)
    save_json(json_string, filename)
    decal_list = []
    # for key, props in prefab.props.items():
    #     decals = filter(lambda prop: prop.decal, props)
    #     for decal in decals:
    #         if decal.key not in decal_list:
    #             decal_list.append(decal.key)
    #         content +=save_decal(convert_decal(decal, index,decal_dir))
    save_to_file(content, filename + ".ue4")


def save_ue4_map_data(filename, map_data: tuple):
    map = map_data[0]
    dir = "/Game/Environment/meshes2"
    decal_dir = "/Game/Environment/DEcals/Materials"
    content = ""
    buildings_data = []
    for index, building in enumerate(map.buildings):
        buildings_data.append(convert_building(building, index, dir))
    decal_data = []
    for key, props in map.props.items():
        decals = filter(lambda prop: prop.decal, props)
        for index, decal in enumerate(decals):
            decal_data.append(convert_decal(decal, index, decal_dir))
    prefab_dict = {'Name': 'prefab', 'buildings': buildings_data, 'decals': decal_data}
    json_string = json.dumps([prefab_dict], default=lambda o: o.__dict__, indent=4)
    save_json(json_string, filename)
    decal_list = []
    # for key, props in prefab.props.items():
    #     decals = filter(lambda prop: prop.decal, props)
    #     for decal in decals:
    #         if decal.key not in decal_list:
    #             decal_list.append(decal.key)
    #         content +=save_decal(convert_decal(decal, index,decal_dir))
    save_to_file(content, filename + ".ue4")


ue4_savers = {
    Ue4StructureType.PREFAB: save_ue4_prefab_data,
    Ue4StructureType.MAP: save_ue4_map_data,
}


def save_to_file(content, name):
    output_file = open(name, "w")
    output_file.write(content)
    output_file.close()
