from typing import TYPE_CHECKING
from pygame import Rect
if TYPE_CHECKING:
    from GameObject import GameObject

class ObjectRegistry(object):
    # singleton code from https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ObjectRegistry, cls).__new__(cls)
            cls.instance.objects = []
            cls.instance.solid_objects = []
        return cls.instance

    def add_to_global_object_registry(self, obj: "GameObject"):
        print('added ' + str(id(obj)))
        self.objects.append(obj)

    def remove_from_global_object_registry(self, obj: "GameObject"):
        self.objects.remove(obj)

    def add_to_global_solid_registry(self, obj: "GameObject"):
        print('added ' + str(id(obj)) + ' to solids')
        self.solid_objects.append(obj)

    def remove_from_global_solid_registry(self, obj: "GameObject"):
        self.solid_objects.remove(obj)