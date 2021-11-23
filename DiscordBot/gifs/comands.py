from .modules.giphy import GiphyAPI
from DiscordBot.Bot import Bot # pylint: disable=import-error

bot = Bot()
gif_api = GiphyAPI()

async def comand_error(ctx, error: Exception):
    print(error)
    await ctx.send('**warning: an internal error has occurred**'.upper())

@bot.command(name='gif', help='the bot create send a gif')
async def rand_gif(ctx, message=None):
    try:
        async with ctx.typing():
            img = await gif_api.rand_gif(tag=message)

        await ctx.send(img)
    except Exception as e:
        await comand_error(ctx, e)