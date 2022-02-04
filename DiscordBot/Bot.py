"""
    Bot base
"""
from importlib import import_module
from discord.ext import commands
from . import settings


class Bot(commands.Bot):
    """ commands.Bot instance with singletown """
    _bot_instance = None

    def __new__(cls):
        if cls._bot_instance is None:
            cls._bot_instance = super(Bot, cls).__new__(cls)
        return cls._bot_instance

    def __init__(self):
        if not hasattr(self, 'command_prefix'):
            self.settings = settings
            super(Bot, self).__init__(
                command_prefix=commands.when_mentioned_or(
                    self.settings.DISCORD_PREFIX
                )
            )

    def _load_apps(self):
        """ carregas as aplicações salvas nas configurações """
        for app_prefix in self.settings.APPLICATIONS:
            for required_module in ['commands', 'events', 'logs']:
                import_module(f'{app_prefix}.{required_module}')

    def _load_default_events(self):
        import_module('DiscordBot.events')

    def run(self, *args, **kwargs):
        self._load_default_events()
        self._load_apps()
        return super().run(self.settings.DISCORD_CLIENT_TOKEN, *args, **kwargs)

    def event(self, _):
        """
            este decorator é inabilitado por padrão nesta aplicação
            caso queira adicionar um evento, opte por pelo decorator 'add_listener'
        """
        raise Exception("""
            este decorator é inabilitado por padrão nesta aplicação
            caso queira adicionar um evento, opte pelo decorator '.add_listener'
        """)
