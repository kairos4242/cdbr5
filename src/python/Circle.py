import pygame.geometry

from game_objects.GameObjects import GameObject

class Circle:

    #temp solution cause pygame circle doesn't have collideobjectsall support yet, can be deleted when they support it

    @staticmethod
    def collideobjectsall(circle: pygame.geometry.Circle, objects: list[GameObject]) -> list[GameObject]:
        output = []
        rects = [x.rect for x in objects]
        collision_list = circle.collidelistall(rects)
        for index in collision_list:
            output.append(objects[index])
        return output