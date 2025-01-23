from Clock import Clock
from Rooms import MainMenu, Room
from animations.Animations import AnimationManager
from input_controllers.PlayerInputController import PlayerInputController
from commands.CommandRegistry import CommandRegistry
from HotkeyManager import HotkeyManager
from Hotkeys import Hotkeys
from events.EventManager import EventManager
from game_objects.Objects import Wall
from game_objects.player import Player
import pygame
import pygame.freetype
from pygame import Event
import pygame_gui
import random
from ObjectRegistry import ObjectRegistry
from ControlType import ControlType
from Colours import Colours
import Config
from input_controllers.ReplayInputController import ReplayInputController
from powers import Powers
import os
import ctypes
import random
ctypes.windll.user32.SetProcessDPIAware()

class Game():

    def __init__(self):

        pygame.init()

        random.seed(10)

        # create game window
        self.game_screen = pygame.display.set_mode(Config.SCREEN_SIZE, flags=pygame.SCALED | pygame.FULLSCREEN, vsync=1)

        self.hotkey_manager = HotkeyManager.load_default_hotkeys()

        #self.input_controller = ReplayInputController(self.hotkey_manager, "test_filename.cdbr")
        self.input_controller = PlayerInputController(self.hotkey_manager)

        # set frame rate
        self.pygame_clock = pygame.time.Clock()
        self.FPS = 60

        self.room = MainMenu(self, self.game_screen, self.pygame_clock, pygame_gui.UIManager(Config.SCREEN_SIZE, theme_path="base_theme.json"))
        self.map = Map(self, self.game_screen, self.hotkey_manager, self.pygame_clock, self.input_controller, pygame_gui.UIManager(Config.SCREEN_SIZE, theme_path="base_theme.json"))

        self.game_loop()

    def goto_room(self, room: "Room"):
        self.room = room

    def end_game(self):
        self.run_game = False

    def game_loop(self):
        # game loop
        self.run_game = True
        while self.run_game:

            time_delta = self.pygame_clock.tick(self.FPS) / 1000

            self.events = pygame.event.get()

            # check manual quit
            keys = pygame.key.get_pressed()
            if self.hotkey_manager.check_pressed(keys, Hotkeys.QUIT):
                self.end_game()

            if self.hotkey_manager.check_pressed(keys, Hotkeys.SAVE_REPLAY):
                self.map.command_registry.save_replay("test_filename.cdbr")

            self.room.step(keys, self.events, time_delta)
            pygame.display.update()

class Map(Room):

    def __init__(self, game: Game, game_screen: "pygame.Surface", hotkey_manager: "HotkeyManager", pygame_clock: "pygame.time.Clock", input_controller: "PlayerInputController", ui_manager: pygame_gui.UIManager):
        "Set up initial map configuration."

        super().__init__(game, game_screen, pygame_clock, ui_manager)

        self.game_screen = game_screen
        self.screen = pygame.surface.Surface((1920, 1080)) #screen to draw everything to before game screen for fullscreen effects like screen shake
        self.hotkey_manager = hotkey_manager

        self.TUROK_30PT = pygame.freetype.Font("pygame_tutorial/assets/fonts/turok.ttf", 30)
        self.ARIAL_16PT = pygame.freetype.SysFont("Arial", 16)

        self.background = pygame.image.load(os.path.join('assets', 'testing', 'Cream Black Background.png')).convert()

        self.screen_shake = 0
        self.render_offset = [0, 0]

        self.events = []

        self.pygame_clock = pygame_clock

        self.clock = Clock()
        self.event_manager = EventManager()
        self.animation_manager = AnimationManager()
        self.input_controller = input_controller
        
        self.command_registry = CommandRegistry(self.clock, self.event_manager)
        self.object_registry = ObjectRegistry()

        self.player1 = Player(
            200,
            400,
            ControlType.HUMAN,
            [],
            Colours.Red,
            self,
            self.command_registry,
            self.hotkey_manager,
            self.animation_manager,
            image = 'Player 1.png',
            name = 'Player 1')

        self.player2 = Player(
            700, 
            400, 
            ControlType.HUMAN_PLAYER2, 
            [], 
            Colours.Blue, 
            self, 
            self.command_registry, 
            self.hotkey_manager, 
            self.animation_manager, 
            image = 'Player 2.png', 
            name = 'Player 2')
        
        self.player1.powers = [Powers.Storm(self.player1), Powers.CrossCannon(self.player1)]
        self.player2.powers = [Powers.BloodKnight(self.player2), Powers.ChipDamage(self.player2), Powers.Repeater(self.player2)]

        
        self.player1.opponent = self.player2
        self.player2.opponent = self.player1

        for i in range(150, 700, 64):
            Wall(i, 200, self.command_registry)

        pygame.display.set_caption("CDBR5")

    def step(self, keys_pressed, events: list[Event], time_delta: float):

        self.clock.tick()
        self.ui_manager.update(time_delta)

        # event handler
        self.events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.game.end_game()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.hello_button:
                    self.goto_room(self.map)

            self.ui_manager.process_events(event)

        self.keys = keys_pressed

        moves = self.input_controller.get_input(self.player1, self.player2, self.keys, self.clock)
        for move in moves:
            move.execute(self.command_registry)

        #run steps
        for object in self.object_registry.objects:
            object.step()

        #update display
        self.draw_game_objects()
        self.ui_manager.draw_ui(self.game_screen)
        
    def draw_game_objects(self):
        #self.screen.fill(Colours.PapayaWhip.value)
        self.screen.blit(self.background)
        self.ARIAL_16PT.render_to(self.screen, (0, 0), str(self.pygame_clock.get_fps()), Colours.Black.value)
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

if __name__ == "__main__":
    game =  Game()