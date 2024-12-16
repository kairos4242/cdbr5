from game_objects.Bullet import Bullet
from game_objects.GameObject import GameObject
from powers.Effects import Effect
from Attribute import ModificationType, Property


class Power():

    def __init__(self):
        self.max_cooldown = 100
        self.cooldown = 100
        self.owner = None
        self.uses = None # intended here to mean infinite uses, not sure if this is the best way to do it

    def step(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def on_acquire(self):
        pass

    def on_use(self):
        pass

    def on_remove(self):
        pass

class CrossCannon(Power):

    def __init__(self, owner: GameObject):
        super().__init__()
        self.max_cooldown = 30
        self.cooldown = 30
        self.owner = owner

    def on_use(self):
        #create four projectiles around owner, one going in each cardinal direction
        Bullet(self.owner.rect.centerx, self.owner.rect.centery - 50, 0, -8, self.owner)
        Bullet(self.owner.rect.centerx, self.owner.rect.centery + 50, 0, 8, self.owner)
        Bullet(self.owner.rect.centerx - 50, self.owner.rect.centery, -8, 0, self.owner)
        Bullet(self.owner.rect.centerx + 50, self.owner.rect.centery, 8, 0, self.owner)

class Sprint(Power):

    def __init__(self, owner: GameObject):
        super().__init__()
        self.max_cooldown = 60
        self.cooldown = 0
        self.owner = owner

    def on_use(self):
        #get a movespeed aura for 1 second
        speed_aura = Effect("Sprint", 60, self.owner, Property.MOVESPEED, ModificationType.PERCENT, 50)
        self.owner.effects.append(speed_aura)