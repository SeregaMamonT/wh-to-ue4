import json


class Quaternion:
    def __init__(self, x: float, y: float, z: float, w: float):
        self.X = x
        self.Y = y
        self.Z = z
        self.W = w


class RelativeLocation:
    def __init__(self, x: float, y: float, z: float):
        self.X = x
        self.Y = y
        self.Z = z


class RelativeRotation:
    def __init__(self, roll: float, pitch: float, yaw: float):
        self.X = roll
        self.Y = pitch
        self.Z = yaw


class RelativeScale3D:
    def __init__(self, x: float, y: float, z: float):
        self.X = x
        self.Y = y
        self.Z = z


class HasRelativeLocation:
    relative_location: RelativeLocation


class HasRelativeRotation:
    relative_rotation: RelativeRotation


class HasRelativeScale3D:
    relative_scale_3d: RelativeScale3D


class Transform:
    Translation: RelativeLocation
    Rotation: Quaternion
    Scale3D: RelativeScale3D


class HasTransform:
    transform: Transform


class UnrealStaticMeshCopy(HasRelativeLocation, HasRelativeRotation, HasRelativeScale3D):
    name: str
    static_mesh: str


class UnrealStaticMesh(HasTransform):
    name: str
    static_mesh: str


class UnrealDecalCopy(HasRelativeLocation, HasRelativeRotation, HasRelativeScale3D):
    name: str
    material: str
    decal: str
    tiling: float
    parallax_scale: float


class UnrealDecal(HasTransform):
    name: str
    material: str
    tiling: float
    parallax_scale: float


class UnrealParticle(HasTransform):
    name: str
    particle: str