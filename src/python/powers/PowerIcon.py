import pygame
import pygame_gui

class PowerIcon():

    #essentially a wrapper for a pygame_gui ui image with a step() and simple functions for on use, etc

    def __init__(self, relative_rect: pygame.Rect, image_surface: pygame.Surface, manager: pygame_gui.UIManager, anchors: dict[str, str]):

        self.icon = pygame_gui.elements.UIImage(relative_rect=relative_rect,
                                        image_surface=image_surface, manager=manager,
                                        anchors=anchors)
        
        self.scale = 1
        self.original_width = image_surface.get_width()
        self.original_height = image_surface.get_height()
        
    def on_use(self):
        self.scale = 1.25
        self.icon.set_dimensions((self.original_width * self.scale, self.original_height * self.scale))

    def step(self):
        if self.scale > 1:
            self.scale = max(self.scale - 0.05, 1)
            self.icon.set_dimensions((self.original_width * self.scale, self.original_height * self.scale))