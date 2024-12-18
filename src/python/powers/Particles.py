import math
import pygame


class Particle():

    def __init__(self, x, y, angle, speed, colour, scale=1):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.colour = colour
        self.scale = scale
        self.alive = True

    def step(self):
        pass

    def draw(self, surface):
        pass

class Spark(Particle):
    
    def __init__(self, x, y, angle, speed, speed_increment, colour, scale=1):
        super().__init__(x, y, angle, speed, colour, scale)
        self.speed_increment = speed_increment

    def step(self):

        # move
        x_move = math.cos(self.angle) * self.speed
        y_move = math.sin(self.angle) * self.speed

        self.x += x_move
        self.y += y_move

        self.speed -= self.speed_increment
        if self.speed <= 0:
            self.alive = False

    def draw(self, surface):
        if self.alive:
            points = [
                [self.x + math.cos(self.angle) * self.speed * self.scale, self.y + math.sin(self.angle) * self.speed * self.scale],
                [self.x + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3, self.y + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                [self.x - math.cos(self.angle) * self.speed * self.scale * 3.5, self.y - math.sin(self.angle) * self.speed * self.scale * 3.5],
                [self.x + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3, self.y - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                ]
            pygame.draw.polygon(surface, self.colour.value, points)

class GrowingSpark(Particle):
    
    def __init__(self, x, y, angle, start_speed, max_speed, speed_increment, colour, scale=1):
        super().__init__(x, y, angle, start_speed, colour, scale)
        self.max_speed = max_speed
        self.speed_increment = speed_increment

    def step(self):

        # move
        x_move = math.cos(self.angle) * self.speed
        y_move = math.sin(self.angle) * self.speed

        self.x += x_move
        self.y += y_move

        self.speed += self.speed_increment
        if self.speed > self.max_speed:
            self.alive = False

    def draw(self, surface):
        if self.alive:
            points = [
                [self.x + math.cos(self.angle) * self.speed * self.scale, self.y + math.sin(self.angle) * self.speed * self.scale],
                [self.x + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3, self.y + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                [self.x - math.cos(self.angle) * self.speed * self.scale * 3.5, self.y - math.sin(self.angle) * self.speed * self.scale * 3.5],
                [self.x + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3, self.y - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                ]
            pygame.draw.polygon(surface, self.colour.value, points)