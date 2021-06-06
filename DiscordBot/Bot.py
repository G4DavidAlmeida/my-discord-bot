from discord.ext import commands

class Bot(object):
    """
        Classe singleton, serve apenas para manter sempre o mesmo módulo do bot
        carregado evitando a criação de mais de uma estancia do bot
    """
    _bot_instance = None

    def __new__(cls):
        if cls._bot_instance is None:
            cls._bot_instance = commands.Bot(command_prefix='!')
            # Put any initialization here.
        return cls._bot_instance

bot = Bot()

# general events
@bot.event
async def on_ready():
    print('Bot discord is ready!')