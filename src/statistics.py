from wh_binary_objects import Prefab, Vegetation


class PrefabStats:
    buildings: []
    prefabs: []
    particles: []
    decals: []
    props: []
    vegetation: []

    def __init__(self):
        self.buildings = []
        self.prefabs = []
        self.particles = []
        self.decals = []
        self.props = []
        self.vegetation = []

    def update_stats(self, data):
        prefab = data[0]
        vegetation = data[1]
        for building in prefab.buildings:
            if building.building_key not in self.buildings:
                self.buildings.append(building.building_key)
        for prefab_instance in prefab.prefab_instances:
            if prefab_instance.name not in self.prefabs:
                self.prefabs.append(prefab_instance.name)
        for particle in prefab.particles:
            if particle.model_name not in self.particles:
                self.particles.append(particle.model_name)
        for key, props in prefab.props.items():
            decals = filter(lambda prop: prop.decal, props)
            not_decals = filter(lambda prop: not prop.decal, props)
            for decal in decals:
                if decal.key not in self.decals:
                    self.decals.append(decal.key)
            for prop in not_decals:
                if prop.key not in self.props:
                    self.props.append(prop.key)
        for veg in vegetation:
            for tree in veg.trees:
                if tree.key not in self.vegetation:
                    self.vegetation.append(tree.key)

    def print_stats(self):
        print("Buildings: ", len(self.buildings))
        for building in self.buildings:
            print(building)
        print("Prefabs: ", len(self.prefabs))
        for prefab in self.prefabs:
            print(prefab)
        print("Particles: ", len(self.particles))
        for particle in self.particles:
            print(particle)
        print("Decals: ", len(self.decals))
        for decal in self.decals:
            print(decal)
        print("Props: ", len(self.props))
        for prop in self.props:
            print(prop)
        print("Vegetation: ", len(self.vegetation))
        for veg in self.vegetation:
            print(veg)



