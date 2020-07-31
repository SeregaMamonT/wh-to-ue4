import json


class RelativeLocation:
    def __init__(self, x: float, y: float, z: float):
        self.X = x
        self.Y = y
        self.Z = z


class RelativeRotation:
    def __init__(self, pitch: float, yaw: float, roll: float):
        self.X = pitch
        self.Y = yaw
        self.Z = roll
        # self.Pitch = pitch
        # self.Yaw = yaw
        # self.Roll = roll


class RelativeScale3D:
    def __init__(self, x: float, y: float, z: float):
        self.X = x
        self.Y = y
        self.Z = z


class HasRelativeLocation:
    relative_location: RelativeLocation

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class HasRelativeRotation:
    relative_rotation: RelativeRotation

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class HasRelativeScale3D:
    relative_scale_3d: RelativeScale3D

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)



class HasRelativeLocationJson:
    location: RelativeLocation

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class HasRelativeRotationJson:
    rotation: RelativeRotation

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class HasRelativeScale3DJson:
    scale: RelativeScale3D

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class UnrealStaticMesh(HasRelativeLocation, HasRelativeRotation, HasRelativeScale3D):
    name: str
    static_mesh: str


class UnrealStaticMeshJson(HasRelativeLocationJson, HasRelativeRotationJson, HasRelativeScale3DJson):
    Name: str
    static_mesh: str

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class UnrealDecal(HasRelativeLocation, HasRelativeRotation, HasRelativeScale3D):
    name: str
    material: str
    decal: str
    tiling: float
    parallax_scale: float
