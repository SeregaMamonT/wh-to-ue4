import json
import sys
import random
from os import listdir
from os.path import isfile
from typing import BinaryIO
from xml.etree.ElementTree import Element, SubElement, tostring

from src.matrix import transpose, get_angles_deg_XZY, get_angles_XYZ, degrees_tuple
from src.wh_parser import parse_file


def format_float(x):
    return "{:.5f}".format(x).rstrip("0").strip(".")


def with_file(filename, func):
    file: BinaryIO = open(filename, 'rb')
    try:
        func(file)
    finally:
        file.close()


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


def process_file(filename, format):
    def parse_and_save(input_file):
        data = parse_file(input_file)

        tw_structures = list(map(get_total_war_structure, data))
        ue_structures = list(map(get_unreal_engine_structure, data))

        # for inst in data:
        #     inst["position"] = list(map(format_float, inst.get("position")))
        #     inst["scale"] = list(map(format_float, inst.get("scale")))
        #     solution = get_angles_deg(transpose(inst.get("coordinates")))
        #     inst["rotation"] = list(map(format_float, solution))
        #     del inst["coordinates"]

        if format == "json":
            save_json(tw_structures, filename)
        elif format == "xml":
            save_xml(tw_structures, filename)
        save_ue4(ue_structures, filename)

    try:
        with_file(filename, parse_and_save)
    except Exception as e:
        print("Failed to read " + filename + ": " + str(e))


def process_directory(format):
    all_files = [f for f in listdir() if isfile(f) and f.endswith(".bmd")]
    for file in all_files:
        process_file(file, format)


if __name__ == "__main__":
    format = "xml"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        process_file(filename, format)
    else:
        process_directory(format)
