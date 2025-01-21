from abc import abstractmethod
from math import floor, copysign
import math

from Material import Material
from ObjectRegistry import ObjectRegistry
from Attribute import Attribute, ModificationType, Property
import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from powers.Timeline import Timeline
    from commands.CommandRegistry import CommandRegistry
from powers.Effects import Effect
import utils

class GameObject():

    #gameobject: no health, not solid, can deal damage to stuff and modify it but nothing can modify it
    
    def __init__(self, x, y, command_registry: "CommandRegistry", height=64, width=64, depth=0):
        self.object_registry = ObjectRegistry()
        self.object_registry.add_to_global_object_registry(self, depth)
        self.depth = depth #should be no need to modify this after creation? if there is then might need to move object in the registry
        self._movespeed = 7
        self._outside_force_x = 0
        self._outside_force_y = 0
        self.rect = utils.create_rect(x, y, width, height)
        self.command_registry = command_registry
        self.command_registry.add_creation(self)

    def modify_property(self, property_name: str, value):
        #property_name should be the name with the underscore, the internal var
        curr_val = getattr(self, property_name)
        if curr_val != value:
            self.command_registry.add_modification(self, property_name.lstrip("_"), curr_val, value)
            setattr(self, property_name, value)

    @property
    def move_xdir(self):
        return self._move_xdir

    @move_xdir.setter
    def move_xdir(self, value):
        self.modify_property("_move_xdir", value)

    @property
    def move_ydir(self):
        return self._move_ydir

    @move_ydir.setter
    def move_ydir(self, value):
        self.modify_property("_move_ydir", value)

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def draw(self, surface):
        pass
    
    def objects_not_me(self):
        return list(filter(lambda obj: id(obj) != id(self), self.object_registry.objects))
    
    def objects_my_type_not_me(self):
        return list(filter(lambda obj: id(obj) != id(self), self.object_registry.objects_by_type[str(type(self))]))
    
    def solids_not_me(self):
        return list(filter(lambda obj: id(obj) != id(self), self.object_registry.solid_objects))
    
    def actors_not_me(self):
        return list(filter(lambda obj: id(obj) != id(self), self.object_registry.actors))

    def deal_damage(self, source, target: "GameActor", damage, attributes: list[Attribute] = list()):
        #general philosophy on source: should be a power and not a player, unless it's coming from something static like spikes
        #leave untyped? cause what could possibly be a common superclass of spikes and powers, zero fields or traits in common
        self.command_registry.add_damage_dealt(source, target, damage)
        if target.shield >= damage:
            target.shield -= damage
        else:
            damage -= target.shield
            target.shield = 0
            target.hp -= damage
            if target.hp <= 0:
                self.destroy(target)
        if target.timeline != None:
            #should animations still get interrupted if you have shield? interesting design question
            if target.timeline.interrupted_by_damage == True:
                target.timeline = None
        

    def heal(self, source, target: "GameActor", hp, attributes: list[Attribute] = list()):
        self.command_registry.add_healing(source, target, hp)
        print("health options", target.hp + hp, target.max_hp)
        target.hp = min(target.hp + hp, target.max_hp)

    def gain_max_hp(self, target: "GameActor", hp, attributes: list[Attribute] = list()):
        target.max_hp += hp

    def gain_shield(self, source, target: "GameActor", amount, attributes: list[Attribute] = list()):
        self.command_registry.add_shield(source, target, amount)
        target.shield += amount

    def destroy(self, target):
        self.object_registry.remove_from_global_object_registry(target)
        self.object_registry.remove_from_global_solid_registry(target)
        if isinstance(target, GameActor):
            self.object_registry.remove_from_global_actor_registry(target)
        self.command_registry.add_destruction(target)

    def move(self, move_x, move_y, outside_force_x, outside_force_y):
        # might seem odd to have a function for this but I suspect it will come in handy later when we need to modify how everything moves
        self.rect.x += move_x
        self.rect.x += outside_force_x
        self.rect.y += move_y
        self.rect.y += outside_force_y

class GameActor(GameObject):
    
    def __init__(self, x, y, command_registry: "CommandRegistry", height=64, width=64, depth=0):

        super().__init__(x, y, command_registry, height, width, depth)

        self.object_registry.add_to_global_actor_registry(self)
        self._hp = 100
        self._max_hp = 100
        self._shield = 0
        self._invulnerable = False
        self._divine_shield = False
        self._solid = False
        self._material = Material.NONE
        self.effects = [] #type: list[Effect]
        self._timeline = None #type: Timeline
        self._move_xdir = 0
        self._move_ydir = 0

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self.modify_property("_hp", value)

    @property
    def max_hp(self):
        return self._max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.modify_property("_max_hp", value)

    @property
    def shield(self):
        return self._shield

    @shield.setter
    def shield(self, value):
        if value < 0:
            value = 0
        self.modify_property("_shield", value)

    @property
    def invulnerable(self):
        return self._invulnerable

    @invulnerable.setter
    def invulnerable(self, value):
        self.modify_property("_invulnerable", value)

    @property
    def divine_shield(self):
        return self._divine_shield

    @divine_shield.setter
    def divine_shield(self, value):
        self.modify_property("_divine_shield", value)

    @property
    def solid(self):
        return self._solid

    @solid.setter
    def solid(self, value):
        self.modify_property("_solid", value)

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        self.modify_property("_material", value)

    @property
    def movespeed(self):
        return self._movespeed

    @movespeed.setter
    def movespeed(self, value):
        self.modify_property("_movespeed", value)

    @property
    def timeline(self):
        return self._timeline

    @timeline.setter
    def timeline(self, value):
        self.modify_property("_timeline", value)

    @property
    def move_xdir(self):
        return self._move_xdir

    @move_xdir.setter
    def move_xdir(self, value):
        self.modify_property("_move_xdir", value)

    @property
    def move_ydir(self):
        return self._move_ydir

    @move_ydir.setter
    def move_ydir(self, value):
        self.modify_property("_move_ydir", value)

    @property
    def outside_force_x(self):
        return self._outside_force_x

    @outside_force_x.setter
    def outside_force_x(self, value):
        self.modify_property("_outside_force_x", value)

    @property
    def outside_force_y(self):
        return self._outside_force_y

    @outside_force_y.setter
    def outside_force_y(self, value):
        self.modify_property("_outside_force_y", value)

    def make_solid(self):
        self.solid = True
        self.object_registry.add_to_global_solid_registry(self)

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
            temp_force = self.outside_force_x #copying it to minimize modifications for property modification recording
            temp_force -= sign_force_x * 0.75
            temp_force = utils.floor_int_bidirectional(temp_force)
            self.outside_force_x = temp_force
        if self.outside_force_y != 0:
            sign_force_y = int(copysign(1, self.outside_force_y))
            temp_force = self.outside_force_y
            temp_force -= sign_force_y * 0.75
            temp_force = utils.floor_int_bidirectional(temp_force)
            self.outside_force_y = temp_force

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