from CdbrLogic import Map
from game_objects.Objects import Turret, Wall
from powers.Powers import Power


class GoombaMap(Map):

    def __init__(self, game, game_screen, hotkey_manager, pygame_clock, input_controller, ui_manager):
        
        super().__init__(game, game_screen, hotkey_manager, pygame_clock, input_controller, ui_manager, (200, 400), (700, 400))

        for i in range(150, 700, 64):
            Wall(i, 200, self.command_registry)

        for i in range(300, 700, 64):
            Turret(1200, i, Power(), )