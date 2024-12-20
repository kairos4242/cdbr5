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

class Map():

    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    def __init__(self):
        "Set up initial map configuration."

        pygame.init()

        self.TUROK_30PT = pygame.freetype.Font("pygame_tutorial/assets/fonts/turok.ttf", 30)
        self.ARIAL_16PT = pygame.freetype.SysFont("Arial", 16)

        self.player1 = Player(200, 300, ControlType.HUMAN,[], Colours.BlushPink.value, self)
        self.player1.powers = [Powers.ConveyorBelt(self.player1), Powers.Bomb(self.player1)]
        self.player2 = Player(700, 300, ControlType.HUMAN_PLAYER2, [], Colours.Red.value, self)
        self.player2.powers = [Powers.FalconPunch(self.player2), Powers.BodySlam(self.player2)]

        self.player1.opponent = self.player2
        self.player2.opponent = self.player1

        self.screen_shake = 0
        self.render_offset = [0, 0]

        self.events = []

        # do we need references to all the walls? maybe not?

        for i in range(100, 700, 64):
            Wall(i, 100)

        self.object_registry = ObjectRegistry()

        # create game window
        self.game_screen = pygame.display.set_mode(Config.SCREEN_SIZE, flags=pygame.SCALED | pygame.FULLSCREEN, vsync=1)
        self.screen = pygame.surface.Surface((1920, 1080)) #screen to draw everything to before game screen for fullscreen effects like screen shake

        pygame.display.set_caption("CDBR5")

        # set frame rate
        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.game_loop()

    def game_loop(self):
        # game loop
        run_game = True
        while run_game:

            self.clock.tick(self.FPS)

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
            for object in self.object_registry.objects_group.sprites():
                object.step()

            #update display
            self.draw_game_objects()
            pygame.display.update()
        
    def draw_game_objects(self):
        self.screen.fill(Colours.Black.value)
        self.TUROK_30PT.render_to(self.screen, (0, 0), str(self.clock.get_fps()), Colours.Red.value)
        p1_hp = self.player1.hp
        p2_hp = self.player2.hp
        self.ARIAL_16PT.render_to(self.screen, (self.player1.rect.x, self.player1.rect.y - 32), str(p1_hp) + "/100", self.player1.colour)
        self.ARIAL_16PT.render_to(self.screen, (self.player2.rect.x, self.player2.rect.y - 32), str(p2_hp) + "/100", self.player2.colour)
        p1_animation = self.player1.animation
        if p1_animation != None:
            self.TUROK_30PT.render_to(self.screen, (400, 0), str(p1_animation.__class__.__name__), Colours.Red.value)
        """for object in self.object_registry.objects:
            object.draw(self.screen)"""
        self.object_registry.objects_group.draw(self.screen)
        if self.screen_shake > 0:
            self.screen_shake -= 1
            self.render_offset[0] = random.randint(0, 8) - 4
            self.render_offset[1] = random.randint(0, 8) - 4
        else:
            self.render_offset = [0, 0]
        self.game_screen.blit(self.screen, self.render_offset)

if __name__ == "__main__":
    game_map =  Map()