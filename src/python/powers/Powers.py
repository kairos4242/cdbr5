import random
from Colours import Colours
from commands.Event import Event
from commands.EventListener import EventListener
from commands.EventType import EventType
from game_objects import Objects, Projectiles
from game_objects.Projectiles import AtlasBullet, Bullet
from game_objects.GameObject import GameObject
from powers.Animations import BodySlamAnimation, DashAnimation, FalconPunchAnimation, PlayfulAnimation, SniperRifleAnimation
from powers.Effects import Effect
from Attribute import ModificationType, Property
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.player import Player
import utils


class Power(EventListener):

    def __init__(self):
        self.max_cooldown = 100
        self.cooldown = 100
        self.owner = None
        self.uses = None # intended here to mean infinite uses, not sure if this is the best way to do it

    def __init__(self, cooldown: int, max_cooldown: int, owner: "Player", uses: int | None):
        self.cooldown = cooldown
        self.max_cooldown = max_cooldown
        self.owner = owner
        self.command_registry = self.owner.command_registry
        self.uses = uses

    def step(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def on_acquire(self):
        pass

    def on_use(self):
        pass

    def on_remove(self):
        pass

class Sprint(Power):

    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)

    def on_use(self):
        #get a movespeed aura for 1 second
        speed_aura = Effect("Sprint", 60, self.owner, Property.MOVESPEED, ModificationType.PERCENT, 50)
        self.owner.effects.append(speed_aura)

class Blink(Power):

    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)

    def on_use(self):
        # teleport
        teleport_dist = 256
        self.owner.move_tangible(teleport_dist * self.owner.move_xdir, teleport_dist * self.owner.move_ydir)

class Dash(Power):
    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)

    def on_use(self):
        self.owner.animation = DashAnimation(10, self.owner.move_xdir, self.owner.move_ydir, self.owner, 25)

class AggressiveDash(Power):
    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)

    def on_use(self):
        x, y = self.owner.get_direction_to_opponent()
        self.owner.animation = DashAnimation(10, -x, -y, self.owner, 25)


class DefensiveDash(Power):
    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)

    def on_use(self):
        x, y = self.owner.get_direction_to_opponent()
        self.owner.animation = DashAnimation(10, x, y, self.owner, 25)

class PlayfulTrickster(Power):
    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)

    def on_use(self):
        if isinstance(self.owner.animation, PlayfulAnimation):
            self.owner.animation = DashAnimation(10, self.owner.move_xdir, self.owner.move_ydir, self.owner, 25)
        else:
            self.owner.animation = PlayfulAnimation(self.owner)

class ConveyorBelt(Power):
    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)

    def on_use(self):
        #create a conveyor belt in the direction of movement
        #namespace pollution issue here with conveyor belt power and conveyor belt object
        original_x = self.owner.rect.centerx + (64 * self.owner.move_xdir)
        snapped_x = utils.snap_to_grid(original_x)
        original_y = utils.rect.centery + (64 * self.owner.move_ydir)
        snapped_y = utils.snap_to_grid(original_y)
        Objects.ConveyorBelt(
            snapped_x,
            snapped_y,
            self.owner,
            self.owner.move_xdir,
            self.owner.move_ydir
        )

class Swap(Power):
    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)

    def on_use(self):
        # python syntax for swap in place
        self.owner.rect.x, self.owner.rect.y, self.owner.opponent.rect.x, self.owner.opponent.rect.y = self.owner.opponent.rect.x, self.owner.opponent.rect.y, self.owner.rect.x, self.owner.rect.y

class CrossCannon(Power):
    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)

    def on_use(self):
        #create four projectiles around owner, one going in each cardinal direction
        Bullet(self.owner.rect.centerx, self.owner.rect.centery - 50, 0, -8, self.owner, self.owner.colour)
        Bullet(self.owner.rect.centerx, self.owner.rect.centery + 50, 0, 8, self.owner, self.owner.colour)
        Bullet(self.owner.rect.centerx - 50, self.owner.rect.centery, -8, 0, self.owner, self.owner.colour)
        Bullet(self.owner.rect.centerx + 50, self.owner.rect.centery, 8, 0, self.owner, self.owner.colour)

class FalconPunch(Power):
    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)

    def on_use(self):
        self.owner.animation = FalconPunchAnimation(self.owner)

class BodySlam(Power):
    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)

    def on_use(self):
        self.owner.animation = BodySlamAnimation(self.owner)

class Bomb(Power):
    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)

    def on_use(self):
        Projectiles.Bomb(self.owner.rect.centerx, self.owner.rect.centery, self.owner, 60, 128)

class Sword(Power):
    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)

    def on_use(self):
        Projectiles.Sword(self.owner.rect.centerx, self.owner.rect.centery, self.owner, 15, self.owner.move_xdir, self.owner.move_ydir)

class Turret(Power):
    def __init__(self, owner: "Player"):
        super().__init__(150, 150, owner, None)

    def on_use(self):
        original_x = self.owner.rect.centerx + (64 * self.owner.move_xdir)
        snapped_x = utils.snap_to_grid(original_x)
        original_y = self.owner.rect.centery + (64 * self.owner.move_ydir)
        snapped_y = utils.snap_to_grid(original_y)
        Objects.Turret(snapped_x, snapped_y, self.owner, self.owner.move_xdir, self.owner.move_ydir)

class Shotgun(Power):
    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)

    def on_use(self):
        move_angle = math.degrees(math.atan2(-self.owner.move_ydir, self.owner.move_xdir))
        bullet_point = (self.owner.rect.centerx + self.owner.move_xdir * 50, self.owner.rect.centery + self.owner.move_ydir * 50)
        spread = 10
        movespeed = 8
        for angle_degrees in [move_angle - spread, move_angle, move_angle + spread]:
            angle = math.radians(angle_degrees)
            angle_xspeed = utils.round_float_down_bidirectional(math.cos(angle) * movespeed)
            angle_yspeed = utils.round_float_down_bidirectional(-math.sin(angle) * movespeed)
            Bullet(bullet_point[0], bullet_point[1], angle_xspeed, angle_yspeed, self.owner, self.owner.colour)

class SniperRifle(Power):
    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)

    def on_use(self):
        self.owner.animation = SniperRifleAnimation(self.owner)

class ChipDamage(Power):
    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)

    def on_use(self):
        self.owner.deal_damage(self.owner.opponent, 1)

class AtlasStone(Power):
    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)
        self.damage = 1

    def on_use(self):
        movespeed = 7
        bullet_point = (self.owner.rect.centerx + self.owner.move_xdir * 96, self.owner.rect.centery + self.owner.move_ydir * 96)
        AtlasBullet(bullet_point[0], bullet_point[1], self.owner.move_xdir * movespeed, self.owner.move_ydir * movespeed, self.owner, self.owner.colour, self)

class Storm(Power):
    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)

    def on_use(self):
        storm_point = (self.owner.rect.centerx + self.owner.move_xdir * 96, self.owner.rect.centery + self.owner.move_ydir * 96)
        Objects.Storm(storm_point[0], storm_point[1], 1200, self.owner, self.owner.colour)

class HealthInvestment(Power):
    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)
        self.heal_cooldown = 0
        self.max_heal_cooldown = 120
        self.heal_amount = 0
        self.active = False

    def on_use(self):
        self.active = True
        self.heal_cooldown = self.max_heal_cooldown
        damage_amount = math.floor(self.owner.hp / 2)
        self.heal_amount = damage_amount * 2
        self.owner.deal_damage(self.owner, damage_amount)

    def step(self):
        super().step()
        if self.heal_cooldown == 0 and self.active == True:
            self.active = False
            print("healing for", self.heal_amount)
            self.owner.heal(self.owner, self.heal_amount)
        if self.heal_cooldown > 0:
            self.heal_cooldown -= 1
        
class FastLife(Power):
    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)

    def on_use(self):
        damage_amount = math.floor(self.owner.hp - 1)
        self.owner.max_hp = self.owner.max_hp * 2
        self.owner.deal_damage(self.owner, damage_amount)

class BloodKnight(Power):

    def __init__(self, owner: "Player"):
        super().__init__(30, 30, owner, None)
        self.command_registry.event_manager.subscribe(EventType.PROPERTY_CHANGE, "hp", self)

    def notify(self, event: Event):
        if event.target == self.owner:
            x_offset = random.randint(-256, 256)
            y_offset = random.randint(-256, 256)
            storm_point = (self.owner.rect.centerx + x_offset, self.owner.rect.centery + y_offset)
            Objects.Storm(storm_point[0], storm_point[1], 1200, self.owner, self.owner.colour)