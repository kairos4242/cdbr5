from Colours import Colours
from ObjectRegistry import ObjectRegistry
from Rooms import MainMenu, Room, Shop
from game_objects.player import PlayerPrototype
from input_controllers.PlayerInputController import PlayerInputController
from input_controllers.ReplayInputController import ReplayInputController
from HotkeyManager import HotkeyManager
from Hotkeys import Hotkeys
import pygame
import pygame.freetype
import pygame_gui
import random
import Config
from maps.Maps import GoombaMap
import ctypes
import random
from powers import Powers
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

        self.p1_prototype = PlayerPrototype(
            money=100,
            income=50,
            win_bonus=25,
            powers=[Powers.ConveyorBelt(None)],
            colour=Colours.Red,
            name="Player 1"
        )

        self.p2_prototype = PlayerPrototype(
            money=100,
            income=50,
            win_bonus=25,
            powers=[Powers.AtlasStone(None)],
            colour=Colours.Blue,
            name="Player 2"
        )

        self.room = MainMenu(self, self.game_screen, self.pygame_clock, pygame_gui.UIManager(Config.SCREEN_SIZE, theme_path="base_theme.json", enable_live_theme_updates=False))
        
        self.game_loop()

    def generate_shop(self):
        return Shop(self, self.game_screen, self.pygame_clock, pygame_gui.UIManager(Config.SCREEN_SIZE, theme_path="base_theme.json", enable_live_theme_updates=False))

    def generate_map(self):
        ObjectRegistry().clear_object_registry()
        return GoombaMap(
            self,
            self.game_screen,
            self.hotkey_manager,
            self.pygame_clock,
            self.input_controller,
            pygame_gui.UIManager(Config.SCREEN_SIZE, theme_path="base_theme.json", enable_live_theme_updates=False),
            self.p1_prototype,
            self.p2_prototype
        )

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

if __name__ == "__main__":
    game =  Game()