# import discord

from DiscordBot.Bot import Bot
from .modules.giphy import GiphyAPI

bot = Bot()
Giphy = GiphyAPI()

async def comand_error(ctx, error: Exception):
    print(error)
    await ctx.send('**warning: an internal error has occurred**'.upper())

@bot.command(name='gif', help='To make the bot leave the voice channel')
async def rand_gif(ctx, message=None):
    try:
        async with ctx.typing():
            img = await Giphy.rand_gif(tag=message)

        await ctx.send(img)
    except Exception as e:
        await comand_error(ctx, e)