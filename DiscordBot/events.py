"""
    eventos padrões do bot

    aqui terão eventos e ações que não são relacionadas a nenhum aplicação
    mas ao bot em si, funções de manutenção e derivados

    para uma documentação dos eventos veja o seguinte link:
    https://discordpy.readthedocs.io/en/stable/api.html#event-reference
"""
from .Bot import Bot

bot = Bot()


@bot.add_listener
async def on_ready():
    """ when bot is ready, hes call a message """
    print('Bot discord is ready!')


# @bot.add_listener
# async def on_disconnect():
#     await bot.logout()
#     print('bot desconectado')
