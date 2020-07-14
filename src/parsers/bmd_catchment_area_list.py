from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

# i have no xml, so i dont know exact structure, still have questions

def read_bmd_catchment_area_list(file: BinaryIO):
    version = int2(file)  # version
    amount = int4(file)
    for i in range(amount):
        bmd_catchment_area_version = int2(file)
        bmd_catchment_area_name = string(file)
        some_floats = (float4(file), float4(file), float4(file), float4(file))
        file.read(10)
        # print(bmd_catchment_area_version, bmd_catchment_area_name, some_floats)
    # assert int4(file) == 0, "BMD_CATCHMENT_AREA_LIST has items"