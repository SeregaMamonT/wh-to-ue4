from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

def read_zones_template_list(file: BinaryIO):
    version = int2(file)  # version
    # assert int4(file) == 0, "ZONES_TEMPLATE_LIST has items"
    # print('Version: ', version)
    zones_amount = int4(file)
    # print('Amount: ', amount)
    for i in range(zones_amount):
        points = int4(file)
        # print('Points: ', points)
        points_list = []
        for j in range(points):
            t = (float4(file), float4(file))
            points_list.append(t)
        # print(points_list)

        # <entity_formation_template name=''> and <lines/>
        file.read(8)

        #transformation matrix
        transformation_matrix = []
        i = 16
        while i > 0:
            matrix_element = float4(file)
            transformation_matrix.append(matrix_element)
            i = i - 1
        # print(transformation_matrix)

