from discord.ext import commands


async def enter_room(ctx: commands.Context):
    """ faz o bot entrar na sala se aplicável """
    try:
        # se não connectado, então connectar
        if not ctx.voice_client:
            if not ctx.author.voice:
                await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel")
                return False
            else:
                channel = ctx.author.voice.channel
            await channel.connect()
        return True
    except Exception as e:
        print(e)
        return False


async def music_message_add(ctx: commands.Context, music_play, music):
    """ retorna uma mensagem baseado em quando a fila tá """
    if music_play.queue_is_empty:
        await ctx.send(f'**Tocando {music}**')
    else:
        await ctx.send(f'**{music} adicionado a fila**')
