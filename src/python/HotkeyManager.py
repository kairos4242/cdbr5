import pygame
from Hotkeys import Hotkeys


class HotkeyManager():

    def __init__(self):
        self.keys = dict()

    @staticmethod
    def load_default_hotkeys() -> "HotkeyManager":
        # debating on doing this more generic and not player-specific. Should each player know about the other's hotkeys?
        # doing it more generic would require both players having references to quit and such still, unless that went into another object
        manager = HotkeyManager()
        manager.keys = {
            Hotkeys.P1_LEFT: pygame.K_a,
            Hotkeys.P1_RIGHT: pygame.K_d,
            Hotkeys.P1_UP: pygame.K_w,
            Hotkeys.P1_DOWN: pygame.K_s,
            Hotkeys.P1_AB1: pygame.K_SPACE,
            Hotkeys.P1_AB2: pygame.K_j,
            Hotkeys.P1_AB3: pygame.K_LSHIFT,
            Hotkeys.P2_LEFT: pygame.K_LEFT,
            Hotkeys.P2_RIGHT: pygame.K_RIGHT,
            Hotkeys.P2_UP: pygame.K_UP,
            Hotkeys.P2_DOWN: pygame.K_DOWN,
            Hotkeys.P2_AB1: pygame.K_KP_7,
            Hotkeys.P2_AB2: pygame.K_7,
            Hotkeys.P2_AB3: pygame.K_INSERT,
            Hotkeys.QUIT: pygame.K_ESCAPE,
            Hotkeys.SAVE_REPLAY: pygame.K_p
        }
        return manager
    
    def check_pressed(self, keys, hotkey: Hotkeys):
        return keys[self.keys[hotkey]]
