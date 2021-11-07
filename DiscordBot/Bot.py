from discord.ext import commands

class Bot(commands.Bot):
    """ commands.Bot instance with singletown """
    _bot_instance = None

    def __new__(cls):
        if cls._bot_instance is None:
            cls._bot_instance = commands.Bot(
                command_prefix=commands.when_mentioned_or('!'))
            # Put any initialization here.
        return cls._bot_instance

bot = Bot()

# general events
@bot.event
async def on_ready():
    """ when bot is ready, hes call a message """
    print('Bot discord is ready!')