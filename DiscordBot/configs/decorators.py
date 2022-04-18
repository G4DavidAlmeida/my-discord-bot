import functools
from typing import TYPE_CHECKING
from DiscordBot.utils import command_error
from discord.ext.commands import Context

if TYPE_CHECKING:
    from typing import TYPE_CHECKING, Callable


def default_handler_error_command(func) -> "Callable":
    @functools.wraps(func)
    async def decorator(context: Context, *args, **kwargs):
        try:
            await func(context, *args, **kwargs)
        except Exception as err:
            await command_error(context, err)
    return decorator
