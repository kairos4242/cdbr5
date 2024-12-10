from abc import abstractmethod
from math import floor, copysign
from Material import Material
from ObjectRegistry import ObjectRegistry
import pygame

class GameObject():
    
    def __init__(self, x, y):
        self.object_registry = ObjectRegistry()
        self.object_registry.add_to_global_object_registry(self)
        self.hp = 100
        self.invulnerable = False
        self.divine_shield = False
        self.solid = False
        self.material = Material.NONE
        self.movespeed = 10
        self.rect = pygame.Rect((x, y, 64, 64))

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

    def make_solid(self):
        self.solid = True
        self.object_registry.add_to_global_solid_registry(self)

    def move_tangible(self, move_x, move_y):
        if self.solid == False:
            self.rect.x += move_x
            self.rect.y += move_y
        else:
            sign_move_x = int(copysign(1, move_x))
            sign_move_y = int(copysign(1, move_y))
            print(sign_move_x)
            print(sign_move_y)
            test_rect = pygame.Rect((self.rect.x + move_x, self.rect.y + move_y, self.rect.width, self.rect.height))
            solids_not_me = list(filter(lambda obj: id(obj) != id(self), self.object_registry.solid_objects))
            collide = test_rect.collideobjects(solids_not_me, key=lambda o: o.rect)
            if collide == None:
                self.rect.x += move_x
                self.rect.y += move_y
            else:
                while floor(move_x) != 0 or floor(move_y) != 0:
                    if move_x != 0:
                        test_rect.x = self.rect.x + sign_move_x
                        test_rect.y = self.rect.y
                        if test_rect.collideobjects(solids_not_me, key=lambda o: o.rect) != None:
                            move_x = 0
                        else:
                            self.rect.x += sign_move_x
                            move_x -= sign_move_x

                    if move_y != 0:
                        test_rect.x = self.rect.x
                        test_rect.y = self.rect.y + sign_move_y
                        if test_rect.collideobjects(solids_not_me, key=lambda o: o.rect) != None:
                            move_y = 0
                        else:
                            self.rect.y += sign_move_y
                            move_y -= sign_move_y

    def __del__(self):
        pass
        #self.object_registry.remove_from_global_object_registry(id(self))