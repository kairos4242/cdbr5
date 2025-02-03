import random

import pygame
from Circle import Circle
from events.DamageDealtEvent import DamageDealtEvent
from events.Event import Event
from events.EventListener import EventListener
from events.EventType import EventType
from game_objects import Objects, Projectiles
from game_objects.Projectiles import AtlasBullet, Bullet
from powers.PowerIcon import PowerIcon
from powers.Timeline import BodySlamTimeline, DashTimeline, EmbraceTimeline, FalconPunchTimeline, PlayfulTimeline, SniperRifleTimeline
from animations import Animations
from powers.Effects import Effect
from Attribute import ModificationType, Property
import math
import Constants
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.player import Player
from powers.PowerType import PowerType
import utils
import os

class Power(EventListener):

    def __init__(self):
        self.max_cooldown = 100
        self.cooldown = 100
        self.owner = None
        self.name = "Power"
        self.uses = None # intended here to mean infinite uses, not sure if this is the best way to do it

    def __init__(self, name: str, cooldown: int, max_cooldown: int, owner: "Player", type: "PowerType" = PowerType.SKILL):
        self.cooldown = cooldown
        self.max_cooldown = max_cooldown
        self.name = name
        self.owner = owner
        self.command_registry = self.owner.command_registry
        self.type = type
        self.animation = None
        self.icon = None # type: PowerIcon

    def step(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def on_acquire(self):
        pass

    def on_use(self):
        self.command_registry.add_power_used(self)
        if self.type == PowerType.TALENT:
            #remove power, don't trigger any sort of power exhausted or power removed event
            self.owner.powers.remove(self)
        if self.icon != None:
            self.icon.on_use()

    def on_remove(self):
        pass

class NullPower(Power):

    def __init__(self, owner: "Player"):
        super().__init__("No Power", 30, 30, owner)

class Sprint(Power):

    def __init__(self, owner: "Player"):
        super().__init__("Sprint", 30, 30, owner)

    def on_use(self):
        super().on_use()
        #get a movespeed aura for 1 second
        speed_aura = Effect("Sprint", 60, self.owner, Property.MOVESPEED, ModificationType.PERCENT, 50)
        self.owner.effects.append(speed_aura)

class Blink(Power):

    def __init__(self, owner: "Player"):
        super().__init__("Blink", 30, 30, owner)

    def on_use(self):
        super().on_use()
        # teleport
        teleport_dist = 256
        self.owner.move_tangible(teleport_dist * self.owner.move_xdir, teleport_dist * self.owner.move_ydir)

class Dash(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Dash", 30, 30, owner)

    def on_use(self):
        super().on_use()
        self.owner.timeline = DashTimeline(10, self.owner.move_xdir, self.owner.move_ydir, self, 25)

class AggressiveDash(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Aggressive Dash", 30, 30, owner)

    def on_use(self):
        super().on_use()
        x, y = self.owner.get_direction_to_opponent()
        self.owner.timeline = DashTimeline(10, -x, -y, self, 25)

class DefensiveDash(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Defensive Dash", 30, 30, owner)

    def on_use(self):
        super().on_use()
        x, y = self.owner.get_direction_to_opponent()
        self.owner.timeline = DashTimeline(10, x, y, self, 25)

class PlayfulTrickster(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Playful/Trickster", 30, 30, owner)

    def on_use(self):
        super().on_use()
        if isinstance(self.owner.timeline, PlayfulTimeline):
            self.owner.timeline = DashTimeline(10, self.owner.move_xdir, self.owner.move_ydir, self, 25)
        else:
            self.owner.timeline = PlayfulTimeline(self)

class ConveyorBelt(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Conveyor Belt", 30, 30, owner)

    def on_use(self):
        super().on_use()
        #create a conveyor belt in the direction of movement
        #namespace pollution issue here with conveyor belt power and conveyor belt object
        original_x = self.owner.rect.centerx + (64 * self.owner.move_xdir)
        snapped_x = utils.snap_to_grid(original_x)
        original_y = self.owner.rect.centery + (64 * self.owner.move_ydir)
        snapped_y = utils.snap_to_grid(original_y)
        Objects.ConveyorBelt(
            snapped_x,
            snapped_y,
            self,
            self.owner.move_xdir,
            self.owner.move_ydir
        )

class Swap(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Swap", 30, 30, owner)

    def on_use(self):
        super().on_use()
        # python syntax for swap in place
        self.owner.rect.x, self.owner.rect.y, self.owner.opponent.rect.x, self.owner.opponent.rect.y = self.owner.opponent.rect.x, self.owner.opponent.rect.y, self.owner.rect.x, self.owner.rect.y

class CrossCannon(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Cross Cannon", 30, 30, owner, PowerType.ATTACK)

    def on_use(self):
        super().on_use()
        #create four projectiles around owner, one going in each cardinal direction
        Bullet(self.owner.rect.centerx, self.owner.rect.centery - 50, 0, -8, self, self.owner.colour)
        Bullet(self.owner.rect.centerx, self.owner.rect.centery + 50, 0, 8, self, self.owner.colour)
        Bullet(self.owner.rect.centerx - 50, self.owner.rect.centery, -8, 0, self, self.owner.colour)
        Bullet(self.owner.rect.centerx + 50, self.owner.rect.centery, 8, 0, self, self.owner.colour)

class FalconPunch(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Falcon Punch", 30, 30, owner, PowerType.ATTACK)

    def on_use(self):
        super().on_use()
        self.owner.timeline = FalconPunchTimeline(self)

class BodySlam(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Body Slam", 30, 30, owner, PowerType.ATTACK)

    def on_use(self):
        super().on_use()
        self.owner.timeline = BodySlamTimeline(self)

class Bomb(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Bomb", 30, 30, owner, PowerType.ATTACK)

    def on_use(self):
        super().on_use()
        Projectiles.Bomb(self.owner.rect.centerx, self.owner.rect.centery, self, 60, 128)

class Sword(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Sword", 30, 30, owner, PowerType.ATTACK)

    def on_use(self):
        super().on_use()
        Projectiles.Sword(self.owner.rect.centerx, self.owner.rect.centery, self, 15, self.owner.move_xdir, self.owner.move_ydir)

class Turret(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Turret", 150, 150, owner, PowerType.ATTACK)

    def on_use(self):
        super().on_use()
        original_x = self.owner.rect.centerx + (64 * self.owner.move_xdir)
        snapped_x = utils.snap_to_grid(original_x)
        original_y = self.owner.rect.centery + (64 * self.owner.move_ydir)
        snapped_y = utils.snap_to_grid(original_y)
        Objects.Turret(snapped_x, snapped_y, self, self.owner.move_xdir, self.owner.move_ydir)

class Shotgun(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Shotgun", 30, 30, owner, PowerType.ATTACK)

    def on_use(self):
        super().on_use()
        move_angle = math.degrees(math.atan2(-self.owner.move_ydir, self.owner.move_xdir))
        bullet_point = (self.owner.rect.centerx + self.owner.move_xdir * 50, self.owner.rect.centery + self.owner.move_ydir * 50)
        spread = 10
        movespeed = 8
        for angle_degrees in [move_angle - spread, move_angle, move_angle + spread]:
            angle = math.radians(angle_degrees)
            angle_xspeed = utils.round_float_down_bidirectional(math.cos(angle) * movespeed)
            angle_yspeed = utils.round_float_down_bidirectional(-math.sin(angle) * movespeed)
            Bullet(bullet_point[0], bullet_point[1], angle_xspeed, angle_yspeed, self, self.owner.colour)

class SniperRifle(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Sniper Rifle", 30, 30, owner, PowerType.ATTACK)

    def on_use(self):
        super().on_use()
        self.owner.timeline = SniperRifleTimeline(self)

class ChipDamage(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Chip Damage", 30, 30, owner, PowerType.ATTACK)

    def on_use(self):
        super().on_use()
        self.owner.deal_damage(self, self.owner.opponent, 1)

class AtlasStone(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Atlas Stone", 30, 30, owner, PowerType.ATTACK)
        self.damage = 1

    def on_use(self):
        super().on_use()
        movespeed = 7
        bullet_point = (self.owner.rect.centerx + self.owner.move_xdir * Constants.PLAYER_SIZE_WITH_MARGIN, self.owner.rect.centery + self.owner.move_ydir * Constants.PLAYER_SIZE_WITH_MARGIN)
        AtlasBullet(bullet_point[0], bullet_point[1], self.owner.move_xdir * movespeed, self.owner.move_ydir * movespeed, self, self.owner.colour)

class Storm(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Storm", 30, 30, owner, PowerType.ATTACK)
        self.animation = self.owner.animation_manager.get_animation(Animations.StormAnimation)

    def on_use(self):
        super().on_use()
        storm_point = (self.owner.rect.centerx + self.owner.move_xdir * Constants.PLAYER_SIZE_WITH_MARGIN, self.owner.rect.centery + self.owner.move_ydir * Constants.PLAYER_SIZE_WITH_MARGIN)
        Objects.Storm(storm_point[0], storm_point[1], 1200, self, self.animation, self.owner.colour)

class HealthInvestment(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Health Investment", 30, 30, owner)
        self.heal_cooldown = 0
        self.max_heal_cooldown = 120
        self.heal_amount = 0
        self.active = False

    def on_use(self):
        super().on_use()
        self.active = True
        self.heal_cooldown = self.max_heal_cooldown
        damage_amount = math.floor(self.owner.hp / 2)
        self.heal_amount = damage_amount * 2
        self.owner.deal_damage(self, self.owner, damage_amount)

    def step(self):
        super().step()
        if self.heal_cooldown == 0 and self.active == True:
            self.active = False
            print("healing for", self.heal_amount)
            self.owner.heal(self, self.owner, self.heal_amount)
        if self.heal_cooldown > 0:
            self.heal_cooldown -= 1
        
class FastLife(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Fast Life", 30, 30, owner)

    def on_use(self):
        super().on_use()
        damage_amount = math.floor(self.owner.hp - 1)
        self.owner.max_hp = self.owner.max_hp * 2
        self.owner.deal_damage(self, self.owner, damage_amount)

class BloodKnight(Power):

    def __init__(self, owner: "Player"):
        super().__init__("Blood Knight", 30, 30, owner)
        self.command_registry.event_manager.subscribe(EventType.PROPERTY_MODIFICATION, "hp", self)

    def notify(self, event: Event):
        if event.target == self.owner:
            x_offset = random.randint(-256, 256)
            y_offset = random.randint(-256, 256)
            storm_point = (self.owner.rect.centerx + x_offset, self.owner.rect.centery + y_offset)
            Objects.Storm(storm_point[0], storm_point[1], 1200, self, self.owner.animation_manager.get_animation(Animations.StormAnimation), self.owner.colour)

class Normality(Power):

    def __init__(self, owner: "Player"):
        super().__init__("Normality", 30, 30, owner)
        self.command_registry.event_manager.subscribe(EventType.POWER_USAGE, None, self)

    def notify(self, event: Event):
        if event.target == self.owner.opponent:
            self.owner.deal_damage(self, self.owner.opponent, 1)

class Commonality(Power):

    def __init__(self, owner: "Player"):
        super().__init__("Commonality", 30, 30, owner)
        self.command_registry.event_manager.subscribe(EventType.POWER_USAGE, None, self)

    def notify(self, event: Event):
        self.owner.deal_damage(self, event.target, 1)

class Deference(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Deference", 30, 30, owner)

    def on_use(self):
        # this should probably be an animation in the same vein as the other teleports
        # so actual teleport doesn't happen the same frame you request it, way too snappy
        super().on_use()
        x_pos = self.owner.opponent.rect.centerx
        y_pos = self.owner.opponent.rect.centery + Constants.PLAYER_SIZE_WITH_MARGIN
        #check no collisions and if so move below
        hitbox = utils.create_rect(x_pos, y_pos, 64, 64)
        solids_not_me = self.owner.solids_not_me()
        collide = hitbox.collideobjectsall(solids_not_me, key=lambda o: o.rect)
        if collide == []:
            self.owner.rect.centerx = x_pos
            self.owner.rect.centery = y_pos
        else:
            print("collision, no move")

        #heal
        self.owner.heal(self, self.owner, 10)

class TeleportGun(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Teleport Gun", 30, 30, owner, PowerType.ATTACK)

    def on_use(self):
        super().on_use()
        movespeed = 7
        bullet_point = (self.owner.rect.centerx + self.owner.move_xdir * Constants.PLAYER_SIZE, self.owner.rect.centery + self.owner.move_ydir * Constants.PLAYER_SIZE)
        Projectiles.TeleportBullet(bullet_point[0], bullet_point[1], self.owner.move_xdir * movespeed, self.owner.move_ydir * movespeed, self, self.owner.colour)

class Embrace(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Embrace", 30, 30, owner)

    def on_use(self):
        super().on_use()
        self.owner.timeline = EmbraceTimeline(30, self.owner.move_xdir, self.owner.move_ydir, self, 25)

class Rest(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Rest", 30, 30, owner)

    def on_use(self):
        super().on_use()
        boundary = 400
        owner_rect = self.owner.rect
        opponent_rect = self.owner.opponent.rect
        dist = math.hypot(owner_rect.centerx - opponent_rect.centerx, owner_rect.centery - opponent_rect.centery)
        if dist > boundary:
            self.owner.heal(self, self.owner, 15)

class MaxHP(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Max HP", 30, 30, owner)

    def on_use(self):
        super().on_use()
        self.owner.gain_max_hp(self.owner, 5)

class Repeater(Power):

    def __init__(self, owner: "Player"):
        super().__init__("Repeater", 30, 30, owner, PowerType.ATTACK)
        self.command_registry.event_manager.subscribe(EventType.POWER_USAGE, None, self)

    def notify(self, event: Event):
        # using source here as for now source and target are equivalent
        # but if this were to change then source would more likely stay correct
        if event.source == self.owner:
            movespeed = 7
            bullet_point = (self.owner.rect.centerx + self.owner.move_xdir * Constants.PLAYER_SIZE, self.owner.rect.centery + self.owner.move_ydir * Constants.PLAYER_SIZE)
            Projectiles.Bullet(bullet_point[0], bullet_point[1], self.owner.move_xdir * movespeed, self.owner.move_ydir * movespeed, self, self.owner.colour, self)

class LivingStorm(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Living Storm", 30, 30, owner, PowerType.ATTACK)
        Objects.LivingStorm(owner.rect.centerx, owner.rect.centery, self, self.owner.colour)

class Rift(Power):

    def __init__(self, owner: "Player"):
        super().__init__("Rift", 30, 30, owner, PowerType.ATTACK)

    def on_use(self):
        super().on_use()
        # teleport
        teleport_dist = 128
        angle = math.atan2(-self.owner.move_ydir, self.owner.move_xdir)
        self.owner.move_tangible(math.cos(angle) * teleport_dist, -math.sin(angle) * teleport_dist)

        explosion_radius = 128
        damage = 10
        collision_circle = pygame.geometry.Circle(self.owner.rect.centerx, self.owner.rect.centery, explosion_radius)
        collide = Circle.collideobjectsall(collision_circle, self.owner.solids_not_me())
        for collision in collide:
            self.owner.deal_damage(self, collision, damage, [])
            self.owner.map.add_screen_shake(30)

class DanseMacabre(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Danse Macabre", 30, 1200, owner)
        self.command_registry.event_manager.subscribe(EventType.DAMAGE_DEALT, None, self)

    def notify(self, event: DamageDealtEvent):
        if event.source.owner == self.owner:
            self.cooldown = 0

    def on_use(self):
        super().on_use()
        self.owner.timeline = DashTimeline(10, self.owner.move_xdir, self.owner.move_ydir, self, 25)

class Blessing(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Blessing", 30, 30, owner)

    def on_use(self):
        super().on_use()
        self.owner.heal(self, self.owner, 10)
        self.owner.gain_shield(self, self.owner, 10)

class ShieldBoomerang(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Shield Boomerang", 30, 30, owner)

    def on_use(self):
        super().on_use()
        movespeed = 40
        bullet_point = (self.owner.rect.centerx + self.owner.move_xdir * Constants.PLAYER_SIZE, self.owner.rect.centery + self.owner.move_ydir * Constants.PLAYER_SIZE)
        angle = math.atan2(-self.owner.move_ydir, self.owner.move_xdir)
        print("angle", math.degrees(angle))
        print("xspeed", math.cos(angle) * movespeed)
        print("yspeed", -math.sin(angle) * movespeed)
        Projectiles.ShieldBoomerang(bullet_point[0], bullet_point[1], math.cos(angle) * movespeed, -math.sin(angle) * movespeed, self, self.owner.colour)

class TempShield(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Temp Shield", 30, 30, owner)
        self.shield_removal_timer = 60
        self.shield_removal_max_timer = 60
        self.active = False
        self.shield_amount = 30

    def step(self):
        super().step()
        if self.active:
            self.shield_removal_timer -= 1
            if self.shield_removal_timer <= 0:
                self.active = False
                self.owner.shield -= self.shield_amount #can get away with this because of custom setter that wont let it go below 0
                self.shield_removal_timer = self.shield_removal_max_timer

    def on_use(self):
        super().on_use()
        if not self.active:
            self.owner.gain_shield(self, self.owner, self.shield_amount)
        self.active = True

class ShieldMultiplier(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Shield Multiplier", 30, 30, owner)

    def on_use(self):
        super().on_use()
        self.owner.gain_shield(self, self.owner, self.owner.shield)

class Anchor(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Anchor", 30, 30, owner, PowerType.PASSIVE)
        self.used = False

    def step(self):
        if not self.used:
            # should this be coded as a trigger on a start of round event instead? 
            # for something like a trigger all your start of round effects in future?
            self.used = True
            self.owner.gain_shield(self, self.owner, 10)

class HornCleat(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Horn Cleat", 30, 30, owner, PowerType.PASSIVE)
        self.countdown = 600

    def step(self):
        self.countdown -= 1
        if self.countdown == 0:
            self.owner.gain_shield(self, self.owner, 15)

class CaptainsWheel(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Captain's Wheel", 30, 30, owner, PowerType.PASSIVE)
        self.countdown = 1200

    def step(self):
        self.countdown -= 1
        if self.countdown == 0:
            self.owner.gain_shield(self, self.owner, 25)

class Contract(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Contract", 30, 30, owner, PowerType.PASSIVE)
        self.used = False

    def step(self):
        if not self.used:
            # should this be coded as a trigger on a start of round event instead? 
            # for something like a trigger all your start of round effects in future?
            self.used = True
            self.owner.deal_damage(self, self.owner.opponent, 10)

class QuillPen(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Quill Pen", 30, 30, owner, PowerType.PASSIVE)
        self.countdown = 600

    def step(self):
        self.countdown -= 1
        if self.countdown == 0:
            self.owner.deal_damage(self, self.owner.opponent, 15)

class Signature(Power):
    def __init__(self, owner: "Player"):
        super().__init__("Signature", 30, 30, owner, PowerType.PASSIVE)
        self.countdown = 1200

    def step(self):
        self.countdown -= 1
        if self.countdown == 0:
            self.owner.deal_damage(self, self.owner.opponent, 25)