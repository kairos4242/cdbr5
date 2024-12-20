from collections import defaultdict
from typing import TYPE_CHECKING

import pygame
if TYPE_CHECKING:
    from game_objects.GameObject import GameObject

class ObjectRegistry(object):
    # singleton code from https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ObjectRegistry, cls).__new__(cls)
            cls.instance.objects_group = pygame.sprite.LayeredUpdates() # layered for drawing purposes
            cls.instance.solid_objects_group = pygame.sprite.Group()
            cls.instance.objects_by_type_group = {}
            cls.instance.particles = pygame.sprite.Group()

        return cls.instance

    def add_to_global_object_registry(self, obj: "GameObject"):
        object_type = str(type(obj))

        self.objects_group.add(obj)
        type_group = self.objects_by_type_group.get(object_type)
        if type_group == None:
            self.objects_by_type_group[object_type] = pygame.sprite.Group(obj)
        else:
            self.objects_by_type_group[object_type].add(obj)


    def remove_from_global_object_registry(self, obj: "GameObject"):

        object_type = str(type(obj))

        self.objects_group.remove(obj)
        self.objects_by_type_group.get(object_type).remove(obj)


    def add_to_global_solid_registry(self, obj: "GameObject"):
        print('added ' + str(id(obj)) + ' to solids')
        self.solid_objects_group.add(obj)

    def remove_from_global_solid_registry(self, obj: "GameObject"):
        if self.solid_objects_group.has(obj):
            self.solid_objects_group.remove(obj)
        else:
            print("object to remove not in solid list! skipping")