from collections import defaultdict
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.GameObject import GameObject

class ObjectRegistry(object):
    # singleton code from https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ObjectRegistry, cls).__new__(cls)
            cls.instance.objects = []
            cls.instance.solid_objects = []
            cls.instance.objects_by_type = defaultdict(list)
        return cls.instance

    def add_to_global_object_registry(self, obj: "GameObject"):
        self.objects.append(obj)
        self.objects_by_type[str(type(obj))].append(obj)


    def remove_from_global_object_registry(self, obj: "GameObject"):
        self.objects.remove(obj)
        self.objects_by_type[str(type(obj))].remove(obj)

    def add_to_global_solid_registry(self, obj: "GameObject"):
        print('added ' + str(id(obj)) + ' to solids')
        self.solid_objects.append(obj)

    def remove_from_global_solid_registry(self, obj: "GameObject"):
        if obj in self.solid_objects:
            self.solid_objects.remove(obj)
        else:
            print("object to remove not in solid list! skipping")