from abc import abstractmethod
from math import floor, copysign
from Material import Material
from ObjectRegistry import ObjectRegistry
from Attribute import Attribute, ModificationType, Property
import pygame

from powers.Effects import Effect

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
        self.rect = self.create_rect(x, y, 64, 64)
        self.effects = [] #type: list[Effect]

    def create_rect(self, x: int, y: int, width: int, height: int):
        return pygame.Rect((x - width // 2, y - height // 2, width, height))

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

    def make_solid(self):
        self.solid = True
        self.object_registry.add_to_global_solid_registry(self)

    def solids_not_me(self):
        return list(filter(lambda obj: id(obj) != id(self), self.object_registry.solid_objects))

    def deal_damage(self, target, damage, attributes: list[Attribute]):
        target.hp -= damage
        if target.hp <= 0:
            self.destroy(target)

    def destroy(self, target):
        self.object_registry.remove_from_global_object_registry(target)
        self.object_registry.remove_from_global_solid_registry(target)

    def calculate_movespeed(self) -> float:
        base_movespeed = self.movespeed
        modifier = 1
        for effect in self.effects:
            if effect.property == Property.MOVESPEED:
                if effect.modification_type == ModificationType.FLAT:
                    base_movespeed += effect.modification_amount
                elif effect.modification_type == ModificationType.PERCENT:
                    modifier += effect.modification_amount / 100
        return base_movespeed * modifier
        


    def move(self, move_x, move_y):
        # might seem odd to have a function for this but I suspect it will come in handy later when we need to modify how everything moves
        self.rect.x += move_x
        self.rect.y += move_y

    def move_tangible(self, move_x: int, move_y: int):
        if self.solid == False:
            self.rect.x += move_x
            self.rect.y += move_y
        else:
            sign_move_x = int(copysign(1, move_x))
            sign_move_y = int(copysign(1, move_y))
            test_rect = pygame.Rect((self.rect.x + move_x, self.rect.y + move_y, self.rect.width, self.rect.height))
            solids_not_me = self.solids_not_me()
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