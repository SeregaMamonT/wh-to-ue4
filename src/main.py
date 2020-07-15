import json
import sys
import random
from os import listdir, path
from xml.etree.ElementTree import Element, SubElement, tostring

from decorators import read_file_error_logger
from src.matrix import transpose, get_angles_deg_XZY, get_angles_XYZ, degrees_tuple
from src.wh_parser import read_map, read_prefab
from wh_parser import read_vegetation, parse_file


def format_float(x):
    return "{:.5f}".format(x).rstrip("0").strip(".")


def save_json(data, filename):
    content = json.dumps(data, indent=4, sort_keys=True)
    save_to_file(content, filename + ".json")


def save_xml(data, filename):
    entities = Element("entities")
    for model in data:
        entity = SubElement(entities, "entity", {"id": hex(random.randrange(10 ** 17, 10 ** 18))[2:]})
        ECBuilding = SubElement(entity, "ECBuilding", {
            "key": model["model_name"],
            "damage": "0",
            "indestructible": "false",
            "toggleable": "false",
            "capture_location": "",
            "export_as_prop": "false",
            "allow_in_outfield_as_prop": "false"
        })
        ECMeshRenderSettings = SubElement(entity, "ECMeshRenderSettings", {
            "cast_shadow": "true"
        })
        ECTransform = SubElement(entity, "ECTransform", {
            "position": " ".join(model["position"]),
            "rotation": " ".join(model["rotation"]),
            "scale": " ".join(model["scale"]),
        })
        ECTerrainClamp = SubElement(entity, "ECTerrainClamp", {
            "active": "false",
            "clamp_to_sea_level": "false",
            "terrain_oriented": "false",
        })

    content = tostring(entities, "utf-8").decode("utf-8")
    save_to_file(content, filename + ".xml")


def save_ue4(data, filename):
    dirname = "/Game/Environment/lzd_building_cave/meshes"
    content = ""
    for i, model in enumerate(data):
        content += save_ue4_model(model, i, dirname)

    save_to_file(content, filename + ".ue4")


def save_ue4_model(model, id, dirname):
    model_name = model["model_name"]
    content = 'Begin Object Class=/Script/Engine.StaticMeshComponent Name="{0}_{1}_GEN_VARIABLE"\n' \
        .format(model_name, id)
    content += 'StaticMesh=StaticMesh\'"{0}/{1}.{1}"\''.format(dirname, model_name)
    content += '\tStaticMeshImportVersion=1\n'

    x, z, y = map(lambda t: t * 100, map(float, model["position"]))
    content += '\tRelativeLocation=(X={0},Y={1},Z={2})\n'.format(x, y, z)

    roll, yaw, pitch = map(float, model["rotation"])
    content += '\tRelativeRotation=(Pitch={0},Yaw={1},Roll={2})\n'.format(pitch, -yaw, roll)

    scale_x, scale_z, scale_y = model["scale"]
    content += '\tRelativeScale3D = (X={0}, Y={1}, Z={2})\n'.format(scale_x, scale_y, scale_z)

    content += 'End Object\n'
    return content


def save_to_file(content, name):
    output_file = open(name, "w")
    output_file.write(content)
    output_file.close()


def get_total_war_structure(instance):
    return {
        "model_name": instance["model_name"],
        "object_relation1": instance["object_relation1"],
        "object_relation2": instance["object_relation2"],
        "position": list(map(format_float, instance.get("position"))),
        "scale": list(map(format_float, instance.get("scale"))),
        "rotation": list(map(format_float, degrees_tuple(get_angles_XYZ(transpose(instance.get("coordinates"))))))
    }


def get_unreal_engine_structure(instance):
    return {
        "model_name": instance["model_name"],
        "object_relation1": instance["object_relation1"],
        "object_relation2": instance["object_relation2"],
        "position": list(map(format_float, instance.get("position"))),
        "scale": list(map(format_float, instance.get("scale"))),
        "rotation": list(map(format_float, get_angles_deg_XZY(transpose(instance.get("coordinates")))))
    }


global_context = []


@read_file_error_logger
def read_prefab_file(prefab_name: str):
    with open(prefab_name, 'rb') as file:
        return read_prefab(file, global_context)


@read_file_error_logger
def read_map_file(map_file_name: str):
    with open(map_file_name, 'rb') as file:
        return read_map(file, global_context)


@read_file_error_logger
def read_vegetation_file(prefab_vegetation_file: str):
    with open(prefab_vegetation_file, 'rb') as file:
        return read_vegetation(file)


def parse_prefab(prefab_name: str):
    prefab_vegetation_name = prefab_name + '.vegetation'
    if path.exists(prefab_vegetation_name):
        return read_prefab_file(prefab_name), read_vegetation_file(prefab_vegetation_name)
    else:
        return read_prefab_file(prefab_name)


def process_file(filename, format):
    print(filename)

    def parse_and_save(input_file):
        data = parse_file(input_file, global_context)

        tw_structures = list(map(get_total_war_structure, data))
        ue_structures = list(map(get_unreal_engine_structure, data))

        if format == "json":
            save_json(tw_structures, filename)
        elif format == "xml":
            save_xml(tw_structures, filename)
        save_ue4(ue_structures, filename)

    try:
        with open(filename, 'rb') as file:
            parse_and_save(file)
    except Exception as e:
        print("Failed to read " + filename + ": " + str(e))


def parse_prefabs(prefab_names):
    for prefab_name in prefab_names:
        print("Prefab " + prefab_name)
        prefab_data = parse_prefab(prefab_name)
        if prefab_data is not None:
            print("Prefab + Vegetation found" if len(prefab_data) == 2 else "Only prefab found")


def parse_map():
    if path.exists('bmd_data.bin'):
        parsed_map = read_map_file('bmd_data.bin')
    else:
        raise Exception('bmd_data.bin not found')
    vegetations = list(map(read_vegetation_file, find_map_vegetations()))
    return parsed_map, vegetations


def process_directory(format):
    all_files = [f for f in listdir() if path.isfile(f) and (f.endswith(".bmd") or f.endswith(".vegetation"))]
    for file in all_files:
        process_file(file, format)
    print(global_context)


def dir_files():
    return [f for f in listdir() if path.isfile(f)]


def find_prefab_files():
    return [f for f in dir_files() if f.endswith(".bmd")]


def find_map_vegetations():
    return [f for f in dir_files() if f.endswith("tree_list.bin")]


def get_parsing_mode_param():
    for arg in sys.argv:
        if arg.startswith("mode="):
            return arg.split("=")[1]


def get_file_param():
    for arg in sys.argv:
        if arg.startswith("file="):
            return arg.split("=")[1]


if __name__ == '__main__':
    format = 'xml'

    mode = get_parsing_mode_param()
    assert mode is not None, "Parsing mode ('mode' parameter) is not defined. Possible values: 'prefab', 'map'"

    if mode == 'prefab':
        file_param = get_file_param()
        prefab_names = [file_param] if file_param is not None else find_prefab_files()
        parse_prefabs(prefab_names)
    elif mode == 'map':
        parse_map()
