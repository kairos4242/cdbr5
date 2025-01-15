from Clock import Clock
from CommandRegistry import CommandRegistry
from commands.EventManager import EventManager
from game_objects.Objects import Wall
from game_objects.player import Player
import pygame
import pygame.freetype
import random
from ObjectRegistry import ObjectRegistry
from ControlType import ControlType
from Colours import Colours
import Config
from powers import Powers
import os
import ctypes
ctypes.windll.user32.SetProcessDPIAware()

class Map():

    def __init__(self):
        "Set up initial map configuration."

        pygame.init()

        # create game window
        self.game_screen = pygame.display.set_mode(Config.SCREEN_SIZE, flags=pygame.SCALED | pygame.FULLSCREEN, vsync=1)
        self.screen = pygame.surface.Surface((1920, 1080)) #screen to draw everything to before game screen for fullscreen effects like screen shake

        self.TUROK_30PT = pygame.freetype.Font("pygame_tutorial/assets/fonts/turok.ttf", 30)
        self.ARIAL_16PT = pygame.freetype.SysFont("Arial", 16)

        self.background = pygame.image.load(os.path.join('assets', 'testing', 'Cream Black Background.png')).convert()

        self.screen_shake = 0
        self.render_offset = [0, 0]

        self.events = []

        self.clock = Clock()
        self.event_manager = EventManager()
        self.command_registry = CommandRegistry(self.clock, self.event_manager)
        self.object_registry = ObjectRegistry()

        self.player1 = Player(200, 400, ControlType.HUMAN,[], Colours.Red, self, self.command_registry, image = 'Player 1.png')
        self.player1.powers = [Powers.Rift(self.player1), Powers.BodySlam(self.player1), Powers.BloodKnight(self.player1)]
        self.player2 = Player(700, 400, ControlType.HUMAN_PLAYER2, [], Colours.Blue, self, self.command_registry, image = 'Player 2.png')
        self.player2.powers = [Powers.DanseMacabre(self.player2), Powers.ChipDamage(self.player2), Powers.Repeater(self.player2)]


        self.player1.opponent = self.player2
        self.player2.opponent = self.player1

        # do we need references to all the walls? maybe not?

        for i in range(150, 700, 64):
            Wall(i, 200, self.command_registry)

        pygame.display.set_caption("CDBR5")

        # set frame rate
        self.pygame_clock = pygame.time.Clock()
        self.FPS = 60

        self.game_loop()

    def game_loop(self):
        # game loop
        run_game = True
        while run_game:

            self.pygame_clock.tick(self.FPS)
            self.clock.tick()

            # event handler
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    run_game = False

            # check manual quit
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                run_game = False

            #run steps
            for object in self.object_registry.objects:
                object.step()

            #update display
            self.draw_game_objects()
            pygame.display.update()
        
    def draw_game_objects(self):
        #self.screen.fill(Colours.PapayaWhip.value)
        self.screen.blit(self.background)
        self.ARIAL_16PT.render_to(self.screen, (0, 0), str(self.pygame_clock.get_fps()), Colours.Black.value)
        p1_hp = self.player1.hp
        p1_max_hp = self.player1.max_hp
        p2_hp = self.player2.hp
        p2_max_hp = self.player2.max_hp
        self.ARIAL_16PT.render_to(self.screen, (860, 30), str(p1_hp) + "/" + str(p1_max_hp), Colours.Black.value)
        self.ARIAL_16PT.render_to(self.screen, (1060, 30), str(p2_hp) + "/" + str(p2_max_hp), Colours.Black.value)
        p1_animation = self.player1.animation
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
    game_map =  Map()