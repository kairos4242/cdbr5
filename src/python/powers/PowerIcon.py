import pygame
import pygame_gui
import copy

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from powers.Powers import Power
    from game_objects.player import PlayerPrototype

class PowerIcon():

    #essentially a wrapper for a pygame_gui ui image with a step() and simple functions for on use, etc

    def __init__(self, relative_rect: pygame.Rect, image_surface: pygame.Surface, manager: pygame_gui.UIManager, anchors: dict[str, str], power: "Power"):

        self.icon = pygame_gui.elements.UIImage(relative_rect=relative_rect,
                                        image_surface=image_surface, manager=manager,
                                        anchors=anchors)
        
        self.scale = 1
        self.original_width = image_surface.get_width()
        self.original_height = image_surface.get_height()
        self.relative_rect = relative_rect
        self.anchors = anchors
        self.manager = manager
        self.power = power
        self.tooltip = None
        self.hover_time_max = 20
        self.hover_time = self.hover_time_max

    def on_possible_press(self, prototype: "PlayerPrototype", mouse_coords: tuple[int, int]) -> bool:
        if self.icon.hovered:
            prototype.powers.append(copy.deepcopy(self.power))
            return True
        return False
        
    def on_use(self):
        self.scale = 1.25
        self.icon.set_dimensions((self.original_width * self.scale, self.original_height * self.scale))

    def kill(self):
        self.icon.hide()
        self.icon.kill()

    def step(self):
        if self.scale > 1:
            self.scale = max(self.scale - 0.05, 1)
            self.icon.set_dimensions((self.original_width * self.scale, self.original_height * self.scale))
        if self.icon.hovered:
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