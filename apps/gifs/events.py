"""
    carregamentos dos eventos da aplicação gif
"""
from DiscordBot.Bot import Bot

bot = Bot()


@bot.add_listener
async def on_ready():
    """ dispara quando o bot está pronto """
    print('gifs app was loaded')
