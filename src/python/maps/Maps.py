import os
import random
import pygame
import pygame_gui
from Clock import Clock
from Colours import Colours
import Config
from ControlType import ControlType
from HotkeyManager import HotkeyManager
from ObjectRegistry import ObjectRegistry
from Rooms import Room
from animations import Animations
from commands.CommandRegistry import CommandRegistry
from events.Event import Event
from events.EventManager import EventManager
from game_objects.Objects import Storm, Turret, Wall
from game_objects.Teams import Team, TeamManager
from game_objects.player import NeutralPlayer, Player
from input_controllers.PlayerInputController import PlayerInputController
from powers import Powers
from powers.PowerIcon import PowerIcon

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from CdbrLogic import Game

class Map(Room):

    def __init__(self, 
                game: "Game", 
                game_screen: "pygame.Surface", 
                hotkey_manager: "HotkeyManager", 
                pygame_clock: "pygame.time.Clock", 
                input_controller: "PlayerInputController", 
                ui_manager: pygame_gui.UIManager,
                p1_pos: tuple[int, int],
                p2_pos:tuple[int, int]
                ):
        "Set up initial map configuration."

        super().__init__(game, game_screen, pygame_clock, ui_manager)

        self.setup_dependencies(hotkey_manager, pygame_clock, input_controller)

        self.setup_players(p1_pos, p2_pos)

        self.setup_gui()

    def setup_dependencies(self, hotkey_manager, pygame_clock, input_controller):
        self.screen = pygame.surface.Surface((1920, 1080)) #screen to draw everything to before game screen for fullscreen effects like screen shake
        pygame.display.set_caption("CDBR5")
        self.hotkey_manager = hotkey_manager
        self.ARIAL_16PT = pygame.freetype.SysFont("Arial", 16)

        self.background = pygame.image.load(os.path.join('assets', 'testing', 'Cream Black Background.png')).convert()

        self.screen_shake = 0
        self.render_offset = [0, 0]

        self.events = []

        self.pygame_clock = pygame_clock

        self.clock = Clock()
        self.event_manager = EventManager()
        self.animation_manager = Animations.AnimationManager()
        self.input_controller = input_controller
        
        self.command_registry = CommandRegistry(self.clock, self.event_manager)
        self.object_registry = ObjectRegistry()

    def setup_players(self, p1_pos: tuple[int, int], p2_pos: tuple[int, int]):
        self.p1team = Team("Player 1 Team")
        self.p2team = Team("Player 2 Team")
        self.neutral_team = Team("Neutral Team")
        self.team_manager = TeamManager([self.p1team, self.p2team])

        self.player1 = Player(
            p1_pos[0],
            p1_pos[1],
            ControlType.HUMAN,
            [],
            Colours.Red,
            self.p1team,
            self,
            self.command_registry,
            self.hotkey_manager,
            self.animation_manager,
            image = 'Player 1.png',
            name = 'Player 1')

        self.player2 = Player(
            p2_pos[0], 
            p2_pos[1], 
            ControlType.HUMAN_PLAYER2, 
            [], 
            Colours.Blue,
            self.p2team,
            self,
            self.command_registry, 
            self.hotkey_manager, 
            self.animation_manager, 
            image = 'Player 2.png', 
            name = 'Player 2')
        
        self.neutral_player = NeutralPlayer(None, Colours.Black, self.neutral_team, self, self.command_registry, self.hotkey_manager, self.animation_manager)
        
        self.player1.opponent = self.team_manager.get_first_enemy(self.p1team)
        self.player2.opponent = self.team_manager.get_first_enemy(self.p2team)
        
        self.player1.powers = [Powers.ConveyorBelt(self.player1), Powers.CrossCannon(self.player1), Powers.AggressiveDash(self.player1), Powers.ConveyorBelt(self.player1), Powers.FalconPunch(self.player1)]
        self.player2.powers = [Powers.ChipDamage(self.player2), Powers.Repeater(self.player2)]
        # idea with this is it serves as the source for all damage natural hazards on the map or such do
        self.neutral_power = Powers.NullPower(self.neutral_player)
        self.neutral_player.powers = [self.neutral_power]

    def setup_gui(self):
        # Set up power buttons

        power_bar_layout_rect = pygame.Rect(0, -150, 404, 100)
        power_bar_surface = pygame.image.load(os.path.join('assets', 'testing', 'Power Bar.png')).convert()
        anchors = {'centerx': 'centerx', 'bottom': 'bottom'}
        self.power_bar = pygame_gui.elements.UIImage(relative_rect=power_bar_layout_rect,
                                        image_surface=power_bar_surface, manager=self.ui_manager,
                                        anchors=anchors)
        
        self.player1_power_icons = []
        for index, power in enumerate(self.player1.powers):
            pos = -152 + (index * 76)
            icon_layout_rect = pygame.Rect(pos, -128, 55, 55)
            power_name = power.name
            surface = pygame.image.load(os.path.join('assets', 'testing', 'Power Icons', f'{power_name}_55.png')).convert()
            icon = PowerIcon(icon_layout_rect, surface, self.ui_manager, anchors, power)
            self.player1_power_icons.append(icon)
            power.icon = icon

        self.player1_buttons = []
        prev_button = None
        for index, power in enumerate(self.player1.powers):
            if index == 0:
                button_layout_rect = pygame.Rect(50, 0, 100, 50)
                anchors = {'top': 'top', 'left': 'left'}
            else:
                button_layout_rect = pygame.Rect(10, 0, 100, 50)
                anchors = {'top': 'top', 'left': 'left', 'left_target': prev_button}
            button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (100, 50)),
                                        text=power.name, manager=self.ui_manager,
                                        anchors=anchors)
            self.player1_buttons.append(button)
            prev_button = button

        self.player2_buttons = []
        prev_button = None
        for index, power in enumerate(self.player2.powers):
            if index == 0:
                button_layout_rect = button_layout_rect = pygame.Rect(-100, 0, 100, 50)
                anchors = {'top': 'top', 'right': 'right'}
            else:
                anchors = {'top': 'top', 'right': 'right', 'right_target': prev_button}
                button_layout_rect = button_layout_rect = pygame.Rect(-110, 0, 100, 50)
            button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                        text=power.name, manager=self.ui_manager,
                                        anchors=anchors)
            self.player2_buttons.append(button)
            prev_button = button

    def step(self, keys_pressed, events: list[Event], time_delta: float):

        self.clock.tick()
        self.ui_manager.update(time_delta)

        # event handler
        self.events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.game.end_game()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element in self.player1_buttons:
                    print("player1 button pressed")
                elif event.ui_element in self.player2_buttons:
                    print("player2 button pressed")


            self.ui_manager.process_events(event)

        self.keys = keys_pressed

        moves = self.input_controller.get_input(self.player1, self.player2, self.keys, self.clock)
        for move in moves:
            move.execute(self.command_registry)

        #run steps
        for object in self.object_registry.objects:
            object.step()

        for power_icon in self.player1_power_icons:
            power_icon.step()

        #update display
        self.draw_game_objects()
        self.ui_manager.draw_ui(self.game_screen)
        
    def draw_game_objects(self):
        #self.screen.fill(Colours.PapayaWhip.value)
        self.screen.blit(self.background)
        self.ARIAL_16PT.render_to(self.screen, (0, Config.SCREEN_HEIGHT - 30), str(self.pygame_clock.get_fps()), Colours.Black.value)
        p1_hp = self.player1.hp
        p1_max_hp = self.player1.max_hp
        p2_hp = self.player2.hp
        p2_max_hp = self.player2.max_hp
        p1_shield = self.player1.shield
        p2_shield = self.player2.shield
        self.ARIAL_16PT.render_to(self.screen, (860, 30), str(p1_hp) + "/" + str(p1_max_hp), Colours.Black.value)
        if p1_shield > 0:
            self.ARIAL_16PT.render_to(self.screen, (760, 30), '(' + str(p1_shield) + ')', Colours.Black.value)
        self.ARIAL_16PT.render_to(self.screen, (1060, 30), str(p2_hp) + "/" + str(p2_max_hp), Colours.Black.value)
        if p2_shield > 0:
            self.ARIAL_16PT.render_to(self.screen, (1160, 30), '(' + str(p2_shield) + ')', Colours.Black.value)
        p1_animation = self.player1.timeline
        if p1_animation != None:
            self.ARIAL_16PT.render_to(self.screen, (400, 0), str(p1_animation.__class__.__name__), Colours.Black.value)
        render_list = self.object_registry.get_objects()
        for object in render_list:
            object.draw(self.screen)
        if self.screen_shake > 0:
            self.screen_shake -= 1
            self.render_offset[0] = random.randint(0, 8) - 4
            self.render_offset[1] = random.randint(0, 8) - 4
        else:
            self.render_offset = [0, 0]
        self.game_screen.blit(self.screen, self.render_offset)

    def add_screen_shake(self, amount: int):
        self.screen_shake = max(self.screen_shake, amount)



class GoombaMap(Map):

    def __init__(self, game, game_screen, hotkey_manager, pygame_clock, input_controller, ui_manager):
        
        super().__init__(game, game_screen, hotkey_manager, pygame_clock, input_controller, ui_manager, (200, 400), (700, 400))

        for i in range(150, 700, 64):
            Wall(i, 200, self.command_registry)

        for i in range(200, 1000, 200):
            Storm(1200, i, 2000, self.neutral_power, self.animation_manager.get_animation(Animations.StormAnimation), Colours.Black)