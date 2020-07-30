class RelativeLocation:
    def __init__(self, x: float, y: float, z: float):
        self.X = x
        self.Y = y
        self.Z = z


class RelativeRotation:
    def __init__(self, pitch: float, yaw: float, roll: float):
        self.Pitch = pitch
        self.Yaw = yaw
        self.Roll = roll


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


class UnrealStaticMesh(HasRelativeLocation, HasRelativeRotation, HasRelativeScale3D):
    name: str
    static_mesh: str