from game_objects.Wall import Wall
from game_objects.player import Player
import pygame
import pygame.freetype
from ObjectRegistry import ObjectRegistry
from ControlType import ControlType
from Colours import Colours
import Config

class Map():

    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    def __init__(self):
        "Set up initial map configuration."

        pygame.init()

        self.TUROK_30PT = pygame.freetype.Font("pygame_tutorial/assets/fonts/turok.ttf", 30)
        self.game_objects = []
        self.player1 = Player(200, 300, ControlType.HUMAN)
        self.player2 = Player(700, 300, ControlType.AI)

        # do we need references to all the walls? maybe not?

        for i in range(100, 700, 64):
            Wall(i, 100)

        self.object_registry = ObjectRegistry()

        # create game window
        

        self.screen = pygame.display.set_mode(Config.SCREEN_SIZE)
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
            for event in pygame.event.get():
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
        self.screen.fill(Colours.Black.value)
        self.TUROK_30PT.render_to(self.screen, (0, 0), str(self.clock.get_fps()), Colours.Red.value)
        for object in self.object_registry.objects:
            object.draw(self.screen)

if __name__ == "__main__":
    game_map =  Map()