
"""
    comandos da aplicação de gif
"""
from typing import TYPE_CHECKING

from discord.ext import commands
from DiscordBot.Bot import Bot
from DiscordBot.utils import command_error
from .modules.giphy import GiphyAPI

bot = Bot()
gif_api = GiphyAPI()


@bot.command(name='gif', help='the bot create send a gif')
async def rand_gif(ctx: commands.Context, message=None):
    """ comando para gerar uma gif aleatória """
    try:
        async with ctx.typing():
            img = await gif_api.rand_gif(tag=message)

        await ctx.send(img)
    except Exception as e:
        await command_error(ctx, e)
