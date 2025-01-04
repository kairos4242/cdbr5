from abc import abstractmethod
from math import floor, copysign
import math
from Material import Material
from ObjectRegistry import ObjectRegistry
from Attribute import Attribute, ModificationType, Property
import pygame

from powers.Effects import Effect

class GameObject():
    
    def __init__(self, x, y, height=64, width=64, depth=0):
        self.object_registry = ObjectRegistry()
        self.object_registry.add_to_global_object_registry(self, depth)
        self.depth = depth #should be no need to modify this after creation? if there is then might need to move object in the registry
        self.hp = 100
        self.invulnerable = False
        self.divine_shield = False
        self.solid = False
        self.material = Material.NONE
        self.movespeed = 7
        self.rect = self.create_rect(x, y, width, height)
        self.effects = [] #type: list[Effect]
        self.animation = None
        self.move_xdir = 0
        self.move_ydir = 0
        self.outside_force_x = 0
        self.outside_force_y = 0

    def create_rect(self, x: int, y: int, width: int, height: int):
        return pygame.Rect((x - width // 2, y - height // 2, width, height))
    
    def rot_center(self, image, rect, angle):
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect
    
    def snap_to_grid(self, value):
        return 64 * round(value/64)

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
    
    def objects_not_me(self):
        return list(filter(lambda obj: id(obj) != id(self), self.object_registry.objects))
    
    def objects_my_type_not_me(self):
        return list(filter(lambda obj: id(obj) != id(self), self.object_registry.objects_by_type[str(type(self))]))
    
    def floor_int_bidirectional(self, value: float):
        # makes sure floats that tend towards zero don't overshoot zero and start going in the other direction
        if value < 1 and value > -1:
            return 0
        return value

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
        
    def apply_friction(self):
        sign_force_x = 0
        sign_force_y = 0
        if self.outside_force_x != 0:
            sign_force_x = int(copysign(1, self.outside_force_x))
        if self.outside_force_y != 0:
            sign_force_y = int(copysign(1, self.outside_force_y))
        self.outside_force_x -= sign_force_x * 0.75
        self.outside_force_y -= sign_force_y * 0.75
        self.outside_force_x = self.floor_int_bidirectional(self.outside_force_x)
        self.outside_force_y = self.floor_int_bidirectional(self.outside_force_y)


    def move(self, move_x, move_y, outside_force_x, outside_force_y):
        # might seem odd to have a function for this but I suspect it will come in handy later when we need to modify how everything moves
        self.rect.x += move_x
        self.rect.x += outside_force_x
        self.rect.y += move_y
        self.rect.y += outside_force_y

    def move_direction(self, dir_x: int, dir_y: int, distance: int, outside_force_x: float, outside_force_y: float, tangible: bool):
        dist = distance
        if dir_x == 0 or dir_y == 0:
            dist = math.sqrt((distance ** 2) * 2)

        x_dist = dist * dir_x + outside_force_x
        y_dist = dist * dir_y + outside_force_y
        if tangible:
            self.move_tangible(x_dist, y_dist)
        else:
            self.move(x_dist, y_dist)

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
                while floor(abs(move_x)) != 0 or floor(abs(move_y)) != 0:
                    if move_x != 0:
                        test_rect.x = self.rect.x + sign_move_x
                        test_rect.y = self.rect.y
                        if test_rect.collideobjects(solids_not_me, key=lambda o: o.rect) != None:
                            move_x = 0
                        else:
                            self.rect.x += sign_move_x
                            move_x -= sign_move_x
                            # is this a bandaid? is there a better way to do this? 
                            # implemented because of movement freezing on fractional movement, going past 0 and going infinite in the other direction
                            if move_x < 1 and move_x > -1: 
                                move_x = 0

                    if move_y != 0:
                        test_rect.x = self.rect.x
                        test_rect.y = self.rect.y + sign_move_y
                        if test_rect.collideobjects(solids_not_me, key=lambda o: o.rect) != None:
                            move_y = 0
                        else:
                            self.rect.y += sign_move_y
                            move_y -= sign_move_y
                            if move_y < 1 and move_y > -1:
                                move_y = 0