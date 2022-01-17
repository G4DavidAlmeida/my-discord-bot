"""
    módulo com configurações básicas para máquina de estados
"""
from typing import Type


class State:
    """ classe base de estados """

    def next(self, state: Type["State"]):
        """
            aciona a troca de estados, se bem sucedido
            o retorno desta função será um novo estado
        """
        raise NotImplementedError(
            f"next method of {self} is not implemented")

    def action(self):
        """ executa a ação deste estado """
        raise NotImplementedError(
            f"action method of {self} is not implemented ")


class MachineState:
    """ classe base de máquina de estados """
