from math import copysign
import pygame
from game_objects import Projectiles
from game_objects.GameObject import GameObject
import os
import math
import utils


class Wall(GameObject):

    def __init__(self, x, y, command_registry):
        super().__init__(x, y, command_registry)
        self.make_solid()
        self.image = pygame.image.load(os.path.join('assets', 'testing', 'Wall.png')).convert_alpha()

    def draw(self, surface):
        # pygame.draw.rect(surface, Colours.AshGrey.value, self.rect)
        surface.blit(self.image, (self.rect.x, self.rect.y))

class ConveyorBelt(GameObject):

    def __init__(self, x, y, owner, x_dir, y_dir):
        super().__init__(x, y, owner.command_registry, depth = 100)
        self.owner = owner
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.speed = 10

        self.colour = self.owner.colour

        other_belts = self.objects_my_type_not_me()
        visited_belts = [] # to prevent infinite loops
        # this works cause belts should always be on a grid, if that changes for some reason things break down

        print("before move", self.rect.centerx, self.rect.centery)
        loop = True
        if len(other_belts) > 0:
            while loop:
                no_hits = True
                for other_belt in other_belts:
                    if other_belt.rect.x == self.rect.x and other_belt.rect.y == self.rect.y:
                        no_hits = False
                        print("other belt found!")
                        if other_belt not in visited_belts:
                            visited_belts.append(other_belt)
                        else:
                            # caught in a loop!
                            loop = False
                            self.destroy(self)
                            break

                        #not in a loop, so we have to chain another belt further
                        self.x_dir = other_belt.x_dir
                        self.y_dir = other_belt.y_dir
                        self.rect.centerx += 64 * self.x_dir
                        self.rect.centery += 64 * self.y_dir
                        print("after move", self.rect.centerx, self.rect.centery)
                        break
                # nobody else is in this square, we're good
                if no_hits:
                    loop = False
        print("final", self.rect.centerx, self.rect.centery)

        ANIMATION_LENGTH = 6

        self.images = []
        image_angle = math.degrees(math.atan2(-self.y_dir, self.x_dir))#y is negative because arctan assumes y increasing upward but y increases downward in pygame
        for i in range(ANIMATION_LENGTH):
            # TODO colours
            #TODO diagonals
            image = pygame.image.load(os.path.join('assets', 'testing', 'Conveyor Belt', f'Conveyor Belt - {"Red"} {i + 1}.png'))
            image_rot = pygame.transform.rotate(image, image_angle)
            self.images.append(image_rot.convert_alpha())
        self.images_len = len(self.images) #is this necessary? is it actually saving any compute time?
        self.image_index = 0

    def step(self):
        solids_not_me = self.solids_not_me()
        collide = self.rect.collideobjectsall(solids_not_me, key=lambda o: o.rect)
        for collision in collide:
            if abs(collision.outside_force_x) < self.speed:
                collision.outside_force_x = self.speed * self.x_dir
            if abs(collision.outside_force_y) < self.speed:
                collision.outside_force_y = self.speed * self.y_dir

    def draw(self, surface):
        #pygame.draw.rect(surface, Colours.AshGrey.value, self.rect)
        #pygame.draw.rect(surface, Colours.Red.value, self.rect, 5)
        #pygame.draw.rect(surface, Colours.White.value, utils.create_rect(self.rect.centerx + (16 * self.x_dir), self.rect.centery + (16 * self.y_dir), 16, 16))
        surface.blit(self.images[self.image_index], (self.rect.x, self.rect.y))
        self.image_index += 1
        if self.image_index >= self.images_len - 1:
            self.image_index = 0


class Turret(GameObject):

    def __init__(self, x, y, owner, x_dir, y_dir):
        super().__init__(x, y, owner.command_registry, depth = 100)
        self.owner = owner
        self.x_dir = x_dir
        self.y_dir = y_dir
        if self.x_dir == 0 and self.y_dir == 0:
            self.x_dir = 1
        self.spawn_cooldown = 60
        self.max_spawn_cooldown = 60
        self.lifespan = 1200
        self.colour = self.owner.colour

        image_angle = math.degrees(math.atan2(-self.y_dir, self.x_dir))#y is negative because arctan assumes y increasing upward but y increases downward in pygame
        image = pygame.image.load(os.path.join('assets', 'testing', 'Turret', f'Turret - {utils.get_colour_name(self.colour)} 1.png'))
        self.image, self.rect = utils.rot_center(image, self.rect, image_angle)

        other_turrets = self.objects_my_type_not_me()
        if len(other_turrets) > 0:
                for other_turret in other_turrets:
                    if other_turret.rect.x == self.rect.x and other_turret.rect.y == self.rect.y:
                        print("on top of another turret! not placing")
                        self.destroy(self)
                        #TODO dialogue box here or some feedback for user?

    def step(self):
        self.spawn_cooldown -= 1
        if self.spawn_cooldown <= 0:
            Projectiles.Bullet(self.rect.centerx, self.rect.centery, self.x_dir * 8, self.y_dir * 8, self.owner, self.colour)
            self.spawn_cooldown = self.max_spawn_cooldown
        self.lifespan -= 1
        if self.lifespan <= 0:
            self.destroy(self)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))