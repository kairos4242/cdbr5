from Colours import Colours
from game_objects import Projectiles
from game_objects.Projectiles import Bullet
from game_objects.GameObject import GameObject
from powers.Animations import BodySlamAnimation, DashAnimation, FalconPunchAnimation, PlayfulAnimation
from powers.Effects import Effect
from Attribute import ModificationType, Property
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.player import Player


class Power():

    def __init__(self):
        self.max_cooldown = 100
        self.cooldown = 100
        self.owner = None
        self.uses = None # intended here to mean infinite uses, not sure if this is the best way to do it

    def __init__(self, cooldown: int, max_cooldown: int, owner: "Player", uses: int | None):
        self.cooldown = cooldown
        self.max_cooldown = max_cooldown
        self.owner = owner
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
        pass

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