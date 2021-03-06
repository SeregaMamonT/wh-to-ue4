import struct

from typing import BinaryIO, List, Callable, Any


# BYTE FUNCTIONS
def bool1(file: BinaryIO):
    return struct.unpack('?', file.read(1))[0]

def int1(file: BinaryIO):
    return struct.unpack('b', file.read(1))[0]


def int2(file: BinaryIO):
    return struct.unpack('h', file.read(2))[0]


def int4(file: BinaryIO):
    return struct.unpack('i', file.read(4))[0]


def int8(file: BinaryIO):
    return struct.unpack('Q', file.read(8))[0]


def float4(file: BinaryIO):
    return struct.unpack('f', file.read(4))[0]


def string(file: BinaryIO):
    length = int2(file)
    return file.read(length).decode()


# OTHER FUNCTIONS
def assert_version(name, expected, actual):
    assert actual == expected, "{0} serializer version should be {1} but found {2}".format(name, expected, actual)


def read_list(file: BinaryIO, instance_reader: Callable[[BinaryIO], Any]):
    instance_count = int4(file)
    return list(map(lambda _: instance_reader(file), range(instance_count)))


def mod_vector(vector: List):
    return sum([x * x for x in vector]) ** 0.5


def read_transform_n_x_m(file: BinaryIO, rows: int, cols: int):
    transform = [[None] * cols for i in range(rows)]
    for i in range(rows):
        for j in range(cols):
            transform[i][j] = float4(file)

    return transform


def get_scale(coordinates):
    return list(map(mod_vector, coordinates))


def read_flags(file: BinaryIO):
    assert_version('PARTICLE_EMITTER->flags', 2, int2(file))
    return {
        'allow_in_outfield': bool1(file),
        'clamp_to_surface': bool1(file),
        'clamp_to_water_surface': bool1(file),
        'spring': bool1(file),
        'summer': bool1(file),
        'autumn': bool1(file),
        'winter': bool1(file)
    }