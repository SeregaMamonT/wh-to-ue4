from typing import BinaryIO, List, Any, Callable

from wh_binary_objects import Particle, Prop
from reader import bool1, string, int2, int4, float4, read_list, assert_version, int8
#
def mod_vector(vector: List):
    return sum([x * x for x in vector]) ** 0.5

def parse_file_v2(file: BinaryIO):
    return 0