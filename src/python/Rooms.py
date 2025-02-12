from abc import abstractmethod
import os
from typing import TYPE_CHECKING
import pygame
from pygame import Event
import pygame_gui

from Colours import Colours
from game_objects.player import PlayerPrototype
from powers import Powers
from powers.PowerIcon import PowerIcon
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
                    self.game.goto_room(self.game.generate_shop())

            self.ui_manager.process_events(event)
            self.ui_manager.draw_ui(self.game_screen)

    def draw_ui(self):
        self.ui_manager.draw_ui(self.game_screen)

class Shop(Room):

    def __init__(self, game: "Game", game_screen: "pygame.Surface", pygame_clock: "pygame.time.Clock", ui_manager: "pygame_gui.UIManager"):
        super().__init__(game, game_screen, pygame_clock, ui_manager)
        self.active_player = self.game.p1_prototype
        self.hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)), text='P1 Done', manager=self.ui_manager)

        #generate shop list
        self.shop_commons = [
            Powers.Sprint(),
            Powers.Blink(), 
            Powers.Dash(),
            Powers.ConveyorBelt(),
            Powers.Swap(),
            Powers.CrossCannon(),
            Powers.FalconPunch(),
            Powers.BodySlam(),
            Powers.Bomb(),
            Powers.Sword(),
            Powers.Turret(),
            Powers.Shotgun(),
            Powers.SniperRifle(),
            Powers.ChipDamage(),
            Powers.AtlasStone(),
            Powers.Storm(),
            Powers.HealthInvestment()
            ]
        self.shop_icons = [] #type: list[PowerIcon]
        self.player_icons = [] #type: list[PowerIcon]
        self.player_money = None
        anchors = {'centerx': 'centerx', 'centery': 'centery'}
        num_columns = 8
        for index, power in enumerate(self.shop_commons):
            row = index % num_columns
            column = index // num_columns
            pos = (-76 * (num_columns / 2)) + (row * 76)
            icon_layout_rect = pygame.Rect(pos, 55 * column, 55, 55)
            power_name = power.name
            surface = pygame.image.load(os.path.join('assets', 'testing', 'Power Icons', f'{power_name}_55.png')).convert()
            icon = PowerIcon(icon_layout_rect, surface, self.ui_manager, anchors, power)
            self.shop_icons.append(icon)

        self.regenerate_player_icons(self.active_player)

    def remove_player_icons(self):
        for icon in self.player_icons:
            icon.kill()
        self.player_icons = []

    def regenerate_player_icons(self, prototype: "PlayerPrototype"):
        for icon in self.player_icons:
            icon.kill()
        self.player_icons = []
        if self.player_money != None:
            self.player_money.kill()

        anchors = {'centerx': 'centerx', 'bottom': 'bottom'}
        for index, power in enumerate(prototype.powers):
            pos = -152 + (index * 76)
            icon_layout_rect = pygame.Rect(pos, -128, 55, 55)
            power_name = power.name
            surface = pygame.image.load(os.path.join('assets', 'testing', 'Power Icons', f'{power_name}_55.png')).convert()
            icon = PowerIcon(icon_layout_rect, surface, self.ui_manager, anchors, power)
            self.player_icons.append(icon)

        money_layout_rect = pygame.Rect(0, -256, 64, 64)
        self.player_money = pygame_gui.elements.UITextBox("$" + str(prototype.money), money_layout_rect, self.ui_manager, anchors = anchors)

    def step(self, keys_pressed, events: list["Event"], time_delta: float):

        self.ui_manager.update(time_delta)
        
        # event handler
        for event in events:
            if event.type == pygame.QUIT:
                self.game.end_game()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.hello_button:
                    if self.active_player == self.game.p1_prototype:
                        self.active_player = self.game.p2_prototype
                        self.regenerate_player_icons(self.active_player)
                        self.hello_button.set_text('P2 Done')
                    else:
                        self.game.goto_room(self.game.generate_map())
            if event.type == pygame.MOUSEBUTTONDOWN:
                # have to do this janky way to check if we clicked on an icon since UIImage isn't clickable
                for icon in self.shop_icons:
                    pressed = icon.on_possible_press(self.active_player, pygame.mouse.get_pos())
                    if pressed:
                        self.regenerate_player_icons(self.active_player)

            self.ui_manager.process_events(event)

        for icon in self.shop_icons:
            icon.step()

        pygame.draw.rect(self.game_screen, Colours.Black.value, (0, 0, 1920, 1080))
        self.ui_manager.draw_ui(self.game_screen)