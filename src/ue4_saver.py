from wh_baninary_to_unreal_convertor import convert_building, convert_decal

from terry_savers.xml_saver_utils import s_float
from ue4_objects import UnrealStaticMesh, RelativeLocation, RelativeRotation, RelativeScale3D, UnrealDecal
from wh_binary_objects import Prefab


def save_relative_location(relative_location: RelativeLocation) -> str:
    x = relative_location.X
    y = relative_location.Y
    z = relative_location.Z
    content = '\tRelativeLocation=(X={0},Y={1},Z={2})\n'.format(s_float(x), s_float(y), s_float(z))

    return content


def save_relative_rotation(relative_rotation: RelativeRotation) -> str:
    pitch = relative_rotation.Pitch
    yaw = relative_rotation.Yaw
    roll = relative_rotation.Roll
    content = '\tRelativeRotation=(Pitch={0},Yaw={1},Roll={2})\n'.format(s_float(pitch), s_float(yaw), s_float(roll))

    return content


def save_relative_scale3d(relative_scale_3d: RelativeScale3D) -> str:
    scale_x = relative_scale_3d.X
    scale_y = relative_scale_3d.Y
    scale_z = relative_scale_3d.Z
    content = '\tRelativeScale3D = (X={0}, Y={1}, Z={2})\n'.format(s_float(scale_x), s_float(scale_y), s_float(scale_z))

    return content


def save_static_mesh(static_mesh: UnrealStaticMesh) -> str:
    content = 'Begin Object Class=/Script/Engine.StaticMeshComponent '
    content += 'Name="{0}"\n'.format(static_mesh.name)
    content += static_mesh.static_mesh
    content += '\tStaticMeshImportVersion=1\n'
    content += save_relative_location(static_mesh.relative_location)
    content += save_relative_rotation(static_mesh.relative_rotation)
    content += save_relative_scale3d(static_mesh.relative_scale_3d)
    content += 'End Object\n'

    return content


def save_decal(decal: UnrealDecal) -> str:
    content = 'Begin Object Class=/Script/Engine.ChildActorComponent '
    content += 'Name="{0}"\n'.format(decal.name)
    content += '    Begin Object Class=/Game/Environment/DEcals/wh_decal_bp.wh_decal_bp_C '
    content += 'Name="ChildActor_GEN_VARIABLE_wh_decal_bp_C_CAT"\n'
    content += '    End Object\n'
    content += '    Begin Object Name="ChildActor_GEN_VARIABLE_wh_decal_bp_C_CAT"\n'
    content += '        Decal_Material=MaterialInstanceConstant'"{0}"'\n'.format(decal.material)
    content += '        Tiling={0}\n'.format(s_float(decal.tiling))
    content += '        Parallax Scale={0}\n'.format(s_float(decal.parallax_scale))
    content += '    End Object\n'
    content += '    ChildActorClass=BlueprintGeneratedClass'"/Game/Environment/DEcals/wh_decal_bp.wh_decal_bp_C"'\n'
    content += save_relative_location(decal.relative_location)
    content += save_relative_rotation(decal.relative_rotation)
    content += save_relative_scale3d(decal.relative_scale_3d)
    content += 'End Object\n'

    return content



def save_ue4_prefab_data(filename, prefab: Prefab):
    dir = "/Game/Environment/meshes2"
    content = ""
    for building in prefab.buildings:
        index = prefab.buildings.index(building)
        content +=save_static_mesh(convert_building(building, index, dir))
    decal_dir = "/Game/Environment/Materials"
    for key, props in prefab.props.items():
        decals = filter(lambda prop: prop.decal, props)
        for decal in decals:
            content +=save_decal(convert_decal(decal, index,decal_dir))
    save_to_file(content, filename + ".ue4")


def save_to_file(content, name):
    output_file = open(name, "w")
    output_file.write(content)
    output_file.close()