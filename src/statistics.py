from wh_binary_objects import Prefab, Vegetation


class PrefabStats:
    buildings: []
    prefabs: []
    particles: []
    decals: []
    props: []
    vegetation: []

    def __init__(self):
        self.buildings = set()
        self.prefabs = set()
        self.particles = set()
        self.decals = set()
        self.props = set()
        self.vegetation = set()

    def update_stats(self, data):
        prefab = data[0]
        vegetation = data[1]
        for building in prefab.buildings:
            self.buildings.add(building.building_key)
        for prefab_instance in prefab.prefab_instances:
            self.prefabs.add(prefab_instance.name)
        for particle in prefab.particles:
            self.particles.add(particle.model_name)
        for key, props in prefab.props.items():
            decals = filter(lambda prop: prop.decal, props)
            not_decals = filter(lambda prop: not prop.decal, props)
            for decal in decals:
                self.decals.add(decal.key)
            for prop in not_decals:
                self.props.add(prop.key)
        for veg in vegetation:
            for tree in veg.trees:
                self.vegetation.add(tree.key)

    def print_stats(self):
        print("Buildings: ", len(self.buildings))
        print(*sorted(self.buildings), sep='\n')
        print("Prefabs: ", len(self.prefabs))
        print(*sorted(self.prefabs), sep='\n')
        print("Particles: ", len(self.particles))
        print(*sorted(self.particles), sep='\n')
        print("Decals: ", len(self.decals))
        print(*sorted(self.decals), sep='\n')
        print("Props: ", len(self.props))
        print(*sorted(self.props), sep='\n')
        print("Vegetation: ", len(self.vegetation))
        print(*sorted(self.vegetation), sep='\n')



