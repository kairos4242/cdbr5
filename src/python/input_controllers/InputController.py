from abc import abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Clock import Clock
    from commands.Command import Command
    from game_objects.player import Player


class InputController():

    @abstractmethod
    def get_move_input(self, player1: "Player", player2: "Player", keys, clock: "Clock") -> list["Command"]:
        pass

    @abstractmethod
    def get_power_input(self, player1: "Player", player2: "Player", keys, clock: "Clock") -> list["Command"]:
        pass