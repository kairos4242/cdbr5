from math import copysign
import pygame
from Colours import Colours
from game_objects.GameObject import GameObject


class Wall(GameObject):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill(Colours.AshGrey.value)
        self.make_solid()

    def draw(self, surface):
        pygame.draw.rect(surface, Colours.AshGrey.value, self.rect)

class ConveyorBelt(GameObject):

    def __init__(self, x, y, owner, x_dir, y_dir):
        super().__init__(x, y)
        self.owner = owner
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.speed = 10
        
        self.image.fill(Colours.AshGrey.value)
        pygame.draw.rect(self.image, Colours.Red.value, pygame.Rect(0, 0, 64, 64), 5)
        pygame.draw.rect(self.image, Colours.White.value, self.create_rect(32 + (self.x_dir * 16), 32 + (self.y_dir * 16), 16, 16))

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

    def step(self):
        solids_not_me = self.solids_not_me()
        collide = self.rect.collideobjectsall(solids_not_me, key=lambda o: o.rect)
        for collision in collide:
            if abs(collision.outside_force_x) < self.speed:
                collision.outside_force_x = self.speed * self.x_dir
            if abs(collision.outside_force_y) < self.speed:
                collision.outside_force_y = self.speed * self.y_dir

    def draw(self, surface):
        pygame.draw.rect(surface, Colours.AshGrey.value, self.rect)
        pygame.draw.rect(surface, Colours.Red.value, self.rect, 5)
        pygame.draw.rect(surface, Colours.White.value, self.create_rect(self.rect.centerx + (16 * self.x_dir), self.rect.centery + (16 * self.y_dir), 16, 16))