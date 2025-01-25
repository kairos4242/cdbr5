from abc import abstractmethod
from typing import TYPE_CHECKING
import pygame
from pygame import Event
import pygame_gui
if TYPE_CHECKING:
    from CdbrLogic import Game


class Room():

    def __init__(self, game: "Game", game_screen: "pygame.Surface", pygame_clock: "pygame.time.Clock", ui_manager: "pygame_gui.UIManager"):
        self.game = game
        self.game_screen = game_screen
        self.pygame_clock = pygame_clock
        self.ui_manager = ui_manager

    @abstractmethod
    def step(self, keys_pressed, events: list["Event"], time_delta: float):
        pass

class MainMenu(Room):

    def __init__(self, game: "Game", game_screen: "pygame.Surface", pygame_clock: "pygame.time.Clock", ui_manager: "pygame_gui.UIManager"):
        super().__init__(game, game_screen, pygame_clock, ui_manager)
        self.hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                             text='Get Cooking',
                                             manager=self.ui_manager)

    def step(self, keys_pressed, events: list["Event"], time_delta: float):

        self.ui_manager.update(time_delta)
        
        # event handler
        for event in events:
            if event.type == pygame.QUIT:
                self.game.end_game()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.hello_button:
                    self.game.goto_room(self.game.map)

            self.ui_manager.process_events(event)
            self.ui_manager.draw_ui(self.game_screen)

    def draw_ui(self):
        self.ui_manager.draw_ui(self.game_screen)
