""" utils utilizado em toda aplicação """
from discord.ext import commands


async def command_error(ctx: commands.Context, error: Exception):
    """ default handle error """
    print(error)
    await ctx.send('**internal error**'.upper())
