"""
    commandos da aplicação game
"""
from discord.ext import commands
from DiscordBot.Bot import Bot
from DiscordBot.utils import command_error
from apps.games.modules.forca import HangmanGameMT

bot = Bot()


@bot.command
async def start_hangman_game(ctx: commands.Context):
    """ inicia um jogo da forca """
    try:
        HangmanGameMT()
    except Exception as error:
        command_error(ctx, error)
