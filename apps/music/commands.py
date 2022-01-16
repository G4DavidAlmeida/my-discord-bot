from discord.ext import commands

from DiscordBot.Bot import Bot
from .modules.youtube_dl import YTDLSource
from .modules.music_play import ManagerMPSession
from .utils import enter_room, music_message_add

bot = Bot()


async def comand_error(ctx: commands.Context, error: Exception):
    """ default handle error """
    print(error)
    await ctx.send('**warning: an internal error has occurred**'.upper())


@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx: commands.Context):
    """ faz o bot deixar a chamada de voz """
    if ctx.voice_client and ctx.voice_client.is_connected():
        ManagerMPSession.remove(ctx.voice_client)
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name='play', help='Play a song')
async def play(ctx: commands.Context, url: str):
    """ faz o bot tocar uma música """
    if await enter_room(ctx) and ctx.voice_client:
        music_play = ManagerMPSession.get_or_create(ctx.voice_client)

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)

            music_play.play(player)
            await music_message_add(ctx, music_play, player[0])


@bot.command(name='pause', help='pause the song')
async def pause(ctx: commands.Context):
    """ se o bot estiver tocando uma música, ele pausa ela """
    if ctx.voice_client:
        music_play = ManagerMPSession.get(ctx.voice_client)
        if music_play:
            music_play.pause()


@bot.command(name='resume', help='Resumes the song')
async def resume(ctx: commands.Context):
    """ se o bot deu pausa em uma música, da o re-play """
    if ctx.voice_client:
        music_play = ManagerMPSession.get(ctx.voice_client)
        if music_play:
            music_play.resume()


@bot.command(name='stop', help='Stops the song')
async def stop(ctx: commands.Context):
    """ se o bot estiver tocando música, para sua execução e limpa a fila """
    if ctx.voice_client:
        music_play = ManagerMPSession.get(ctx.voice_client)
        if music_play:
            music_play.stop()


@bot.command(name='skip', help='Skip to the next music')
async def skip(ctx: commands.Context):
    """ se o bot estiver tocando uma música, então ele pula a atual e vai para a próxima """
    if ctx.voice_client:
        music_play = ManagerMPSession.get(ctx.voice_client)
        if music_play:
            music_play.skip()
