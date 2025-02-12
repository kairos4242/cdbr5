import math
import pygame
import pygame_gui
import copy

from typing import TYPE_CHECKING

from Colours import Colours


if TYPE_CHECKING:
    from powers.Powers import Power
    from game_objects.player import PlayerPrototype

class PowerIcon():

    #essentially a wrapper for a pygame_gui ui image with a step() and simple functions for on use, etc

    def __init__(self, relative_rect: pygame.Rect, image_surface: pygame.Surface, manager: pygame_gui.UIManager, anchors: dict[str, str], power: "Power"):

        self.original_width = image_surface.get_width()
        self.original_height = image_surface.get_height()
        
        self.icon = pygame_gui.elements.UIImage(relative_rect=relative_rect,
                                        image_surface=image_surface, manager=manager,
                                        anchors=anchors)
        
        self.overlay_surface = pygame.surface.Surface((self.original_width, self.original_height)).convert_alpha()
        
        self.overlay = pygame_gui.elements.UIImage(relative_rect=relative_rect,
                                        image_surface=image_surface, manager=manager,
                                        anchors=anchors, visible = False)
        self.overlay.hide()
        self.scale = 1
        self.relative_rect = relative_rect
        self.anchors = anchors
        self.manager = manager
        self.power = power
        self.tooltip = None
        self.hover_time_max = 20
        self.hover_time = self.hover_time_max

        self.ARIAL_12PT = pygame.freetype.SysFont("Arial", 12)

    def on_possible_press(self, prototype: "PlayerPrototype", mouse_coords: tuple[int, int]) -> bool:
        if self.overlay.hovered or self.icon.hovered:
            if prototype.money >= self.power.cost:
                prototype.money -= self.power.cost
                prototype.powers.append(copy.deepcopy(self.power))
                return True
            else:
                print(f"Player {prototype.name} has insufficient funds to buy {self.power.name}")
        return False
        
    def on_use(self):
        self.scale = 1.25
        self.icon.set_dimensions((self.original_width * self.scale, self.original_height * self.scale))

    def kill(self):
        self.icon.kill()
        self.overlay.kill()

    def calculatePointOnSquare(self, r, angle):
        p = [0, 0]

        if (angle >= 0 and angle < math.pi / 4):
            p[0] = r
            p[1] = r * math.tan(angle)
        elif (angle >= math.pi / 4 and angle < math.pi / 2):
            p[0] = r * math.tan(math.pi/2 - angle)
            p[1] = r
        elif (angle >= math.pi / 2 and angle < 3 * math.pi / 4):
            p[0] = -1 * r * math.tan(angle % (math.pi/4))
            p[1] = r
        elif (angle >= 3*math.pi/4 and angle < math.pi):
            p[0] = -1 * r
            p[1] = r * math.tan(math.pi - angle)
        elif (angle >= math.pi and angle < 5*math.pi/4):
            p[0] = -1 * r
            p[1] = -1 * r * math.tan(angle % (math.pi/4))
        elif (angle >= 5*math.pi/4 and angle < 3*math.pi/2):
            p[0] = -1 * r * math.tan(3*math.pi/2 - angle)
            p[1] = -1 * r
        elif (angle >= 3*math.pi/2 and angle < 7*math.pi/4):
            p[0] = r * math.tan(angle % (math.pi/4))
            p[1] = -1 * r
        else:
            p[0] = r
            p[1] = -1 * r * math.tan(2 * math.pi - angle)

        return (p[0], p[1])

    def step(self):

        #scale juice
        if self.scale > 1:
            self.scale = max(self.scale - 0.05, 1)
            self.icon.set_dimensions((self.original_width * self.scale, self.original_height * self.scale))

        #check tooltip
        if self.overlay.hovered or self.icon.hovered:
            if self.hover_time > 0:
                self.hover_time -= 1
            else:
                #show a tooltip if we haven't already
                if self.tooltip == None:
                    rect = self.relative_rect.copy()
                    rect.top -= 60
                    rect.width = -1
                    rect.height = -1
                    self.tooltip = pygame_gui.elements.UITextBox(self.power.name, rect, self.manager, anchors=self.anchors)
        else:
            if self.tooltip != None:
                self.tooltip.kill()
                self.tooltip = None
                self.hover_time = self.hover_time_max

        #if on cooldown, handle overlay
        if self.power.cooldown > 0:
            self.overlay.show()
            cooldown_ratio = self.power.cooldown / self.power.max_cooldown
            cooldown_angle_degrees = (cooldown_ratio * 360) - 90
            points = []
            
            start_point = (self.original_width / 2, self.original_height / 2)
            cooldown_angle_radians = (cooldown_angle_degrees % 360) * math.pi / 180
            end_point_test = self.calculatePointOnSquare(27, cooldown_angle_radians)
            end_point = (end_point_test[0] + 27, end_point_test[1] + 27)

            if cooldown_angle_degrees > 225:
                points.append((0, 0))
            if cooldown_angle_degrees > 135:
                points.append((0, 55))
            if cooldown_angle_degrees > 45:
                points.append((55, 55))
            if cooldown_angle_degrees > -45:
                points.append((55, 0))
            points.append((27, 0))
            points.append(start_point)
            points.append(end_point)
            
            self.overlay_surface.fill(Colours.Clear.value)
            #pygame.draw.circle(self.overlay_surface, Colours.Red.value, end_point, 5)
            if len(points) > 2:
                pygame.draw.polygon(self.overlay_surface, (0, 0, 0, 95), points)
            pygame.draw.line(self.overlay_surface, Colours.Black.value, start_point, end_point)
        else:
            self.overlay.hide()
        
        self.overlay.set_image(self.overlay_surface)