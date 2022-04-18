from typing import TYPE_CHECKING
from .decorators import default_handler_error_command

if TYPE_CHECKING:
    from typing import Callable
    from ..Bot import Bot


class BaseAppCommands:
    """ base command discord app """

    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.initializer()

    def initializer(self):
        """ initializer method for default configs """

    @classmethod
    def apply_configs_command(cls, method: "Callable") -> "Callable":
        """
            apply defauf configs on commands methods
        """
        return default_handler_error_command(method)

    @classmethod
    def as_commands(cls, bot: "Bot"):
        """ register only public methods of instance on command register  """
        instance = cls(bot)
        return [(name.replace('command_', ''), cls.apply_configs_command(getattr(instance, name)))
                for name in dir(instance)
                if name.startswith('command_')]
