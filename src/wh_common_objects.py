from app_typing import Matrix, Vector


class Rotation3D:

    def __init__(self, x: float, y: float, z: float):
        self.rotation_x = x
        self.rotation_y = y
        self.rotation_z = z

    def as_vector(self) -> Vector:
        return [self.rotation_x, self.rotation_y, self.rotation_z]


class Scale3D:

    def __init__(self, x: float, y: float, z: float):
        self.scale_x = x
        self.scale_y = y
        self.scale_z = z

    def as_vector(self) -> Vector:
        return [self.scale_x, self.scale_y, self.scale_z]


class Point3D:

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def as_vector(self) -> Vector:
        return [self.x, self.y, self.z]


class Point2D:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def as_vector(self) -> Vector:
        return [self.x, self.y]


class ColourRGB:

    def __init__(self, r: float, g: float, b: float):
        self.red = r
        self.green = g
        self.blue = b


class ColourRGBA:

    def __init__(self, r: float, g: float, b: float, a: float):
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a


class Cube:

    def __init__(self, min_x: float, min_y: float, min_z: float, max_x: float, max_y: float, max_z: float):
        self.min_x = min_x
        self.min_y = min_y
        self.min_z = min_z
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z