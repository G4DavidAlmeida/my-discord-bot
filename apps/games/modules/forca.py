""" estados e máquina de estados do jogo da forca """
from typing import Type

from DiscordBot.machine_state import MachineState, State


class HangmanGameMT(MachineState):
    """
        máquina de estados do jogo da forca
    """

    def __init__(self):
        self._state = GameOverState()


class GameInitializedState(State):
    """ estado inicializador do jogo """

    def next(self, state: Type["State"]):
        return self

    def action(self):
        return None


class GameOverState(State):
    """ representa o estado final desta partida """

    def next(self, state: Type[State]):
        return self

    def action(self):
        return None
