"""
    para uma documentação dos eventos veja o seguinte link:
    https://discordpy.readthedocs.io/en/stable/api.html#event-reference
"""
import discord
from DiscordBot.Bot import Bot

bot = Bot()


@bot.add_listener
async def on_ready():
    """ dispara quando o bot está pronto """
    print('music app was loaded')


async def on_guild_remove(guild: "discord.Guild"):
    """ disparado quando o bot deixa uma guild """
