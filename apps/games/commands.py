"""
    commandos da aplicação game
"""
from typing import TYPE_CHECKING

from DiscordBot.Bot import Bot
from DiscordBot.utils import command_error
from apps.games.modules.forca import HangmanGameMT

if TYPE_CHECKING:
    from discord.ext.commands import Context

bot = Bot()


@bot.command
async def start_hangman_game(ctx: "Context"):
    """ inicia um jogo da forca """
    try:
        HangmanGameMT()
    except Exception as error:
        command_error(ctx, error)
