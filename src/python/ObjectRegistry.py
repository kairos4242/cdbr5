from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_objects.GameObjects import GameObject
    from game_objects.GameObjects import GameActor

class ObjectRegistry(object):
    # singleton code from https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ObjectRegistry, cls).__new__(cls)
            cls.instance.objects = []
            cls.instance.solid_objects = []
            cls.instance.actors = []
            cls.instance.objects_by_type = defaultdict(list)
            cls.instance.objects_by_depth = defaultdict(list)
        return cls.instance

    def add_to_global_object_registry(self, obj: "GameObject", depth=0):
        self.objects.append(obj)
        self.objects_by_type[str(type(obj))].append(obj)
        self.objects_by_depth[depth].append(obj)

    def remove_from_global_object_registry(self, obj: "GameObject"):
        depth = obj.depth
        self.objects.remove(obj)
        self.objects_by_type[str(type(obj))].remove(obj)
        self.objects_by_depth[depth].remove(obj)

    def add_to_global_solid_registry(self, obj: "GameObject"):
        #print('added ' + str(id(obj)) + ' to solids')
        self.solid_objects.append(obj)

    def remove_from_global_solid_registry(self, obj: "GameObject"):
        if obj in self.solid_objects:
            self.solid_objects.remove(obj)
        else:
            #print("object to remove not in solid list! skipping")
            pass

    def add_to_global_actor_registry(self, obj: "GameActor"):
        self.actors.append(obj)

    def remove_from_global_actor_registry(self, obj: "GameActor"):
        self.actors.remove(obj)

    def get_objects(self):
        #returns objects sorted by depth in decreasing order, to ensure correct draw order
        result = []
        for depth in sorted(self.objects_by_depth.keys(), reverse=True):
            for obj in self.objects_by_depth[depth]:
                result.append(obj)
        return result
    
    def clear_object_registry(self):
        self.objects = []
        self.solid_objects = []
        self.actors = []
        self.objects_by_type = defaultdict(list)
        self.objects_by_depth = defaultdict(list)