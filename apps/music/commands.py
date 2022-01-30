"""
    comandos da aplicação music
"""
from datetime import timedelta
from discord.ext import commands
from DiscordBot.Bot import Bot
from DiscordBot.utils import command_error

from .modules.youtube_dl import YTDLSource
from .modules.music_play import ManagerMPSession
from .utils import enter_room, music_message_add

bot = Bot()


@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx: commands.Context):
    """ faz o bot deixar a chamada de voz """
    try:
        if ctx.voice_client and ctx.voice_client.is_connected():
            ManagerMPSession.remove(ctx.voice_client)
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")
    except Exception as error:
        await command_error(ctx, error)


@bot.command(name='play', help='Play a song')
async def play(ctx: commands.Context, url: str):
    """ faz o bot tocar uma música """
    try:
        if await enter_room(ctx) and ctx.voice_client:
            music_play = ManagerMPSession.get_or_create(ctx.voice_client)

            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)

                music_play.play(player)
                await music_message_add(ctx, music_play, player[0])
    except Exception as error:
        await command_error(ctx, error)


@bot.command(name='pause', help='pause the song')
async def pause(ctx: commands.Context):
    """ se o bot estiver tocando uma música, ele pausa ela """
    try:
        if ctx.voice_client:
            music_play = ManagerMPSession.get(ctx.voice_client)
            if music_play:
                music_play.pause()
    except Exception as error:
        await command_error(ctx, error)


@bot.command(name='resume', help='Resumes the song')
async def resume(ctx: commands.Context):
    """ se o bot deu pausa em uma música, da o re-play """
    try:
        if ctx.voice_client:
            music_play = ManagerMPSession.get(ctx.voice_client)
            if music_play:
                music_play.resume()
    except Exception as error:
        await command_error(ctx, error)


@bot.command(name='stop', help='Stops the song')
async def stop(ctx: commands.Context):
    """ se o bot estiver tocando música, para sua execução e limpa a fila """
    try:
        if ctx.voice_client:
            music_play = ManagerMPSession.get(ctx.voice_client)
            if music_play:
                music_play.stop()
    except Exception as error:
        await command_error(ctx, error)


@bot.command(name='skip', help='Skip to the next music')
async def skip(ctx: commands.Context):
    """ se o bot estiver tocando uma música, então ele pula a atual e vai para a próxima """
    try:
        if ctx.voice_client:
            music_play = ManagerMPSession.get(ctx.voice_client)
            if music_play:
                music_play.skip()
    except Exception as error:
        await command_error(ctx, error)


@bot.command(name='list_musics', help='list musics on the queue')
async def list_queue(ctx: commands.Context):
    """ lista as músicas que estão na fila """
    try:
        if not ctx.voice_client:
            return

        music_play = ManagerMPSession.get(ctx.voice_client)

        if not music_play:
            return

        list_text = ''

        for index, music in enumerate(music_play.queue):
            time = timedelta(seconds=music.data.get('duration'))
            list_text += f'{index + 1} - {music} **{time}**\n'

        if list_text:
            await ctx.send(list_text)

    except Exception as error:
        await command_error(ctx, error)
