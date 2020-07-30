from wh_baninary_to_unreal_convertor import convert_building

from terry_savers.xml_saver_utils import s_float
from ue4_objects import UnrealStaticMesh
from wh_binary_objects import Prefab


def save_static_mesh(static_mesh: UnrealStaticMesh) -> str:
    content = 'Begin Object Class=/Script/Engine.StaticMeshComponent '
    #content += 'Name=' + '"static_mesh.name"' + '\n'
    content += 'Name="{0}"\n'.format(static_mesh.name)
    content += static_mesh.static_mesh
    content += '\tStaticMeshImportVersion=1\n'
    x = static_mesh.relative_location.X
    y = static_mesh.relative_location.Y
    z = static_mesh.relative_location.Z
    content += '\tRelativeLocation=(X={0},Y={1},Z={2})\n'.format(s_float(x), s_float(y), s_float(z))
    pitch = static_mesh.relative_rotation.Pitch
    yaw = static_mesh.relative_rotation.Yaw
    roll = static_mesh.relative_rotation.Roll
    content += '\tRelativeRotation=(Pitch={0},Yaw={1},Roll={2})\n'.format(s_float(pitch), s_float(yaw), s_float(roll))
    scale_x = static_mesh.relative_scale_3d.X
    scale_y = static_mesh.relative_scale_3d.Y
    scale_z = static_mesh.relative_scale_3d.Z
    content += '\tRelativeScale3D = (X={0}, Y={1}, Z={2})\n'.format(s_float(scale_x), s_float(scale_y), s_float(scale_z))
    content += 'End Object\n'

    return content


def save_ue4_prefab_data(filename, prefab: Prefab):
    dir = "/Game/Environment/meshes2"
    content = ""
    for building in prefab.buildings:
        index = prefab.buildings.index(building)
        content +=save_static_mesh(convert_building(building, index, dir))

    save_to_file(content, filename + ".ue4")


def save_to_file(content, name):
    output_file = open(name, "w")
    output_file.write(content)
    output_file.close()