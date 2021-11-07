import discord
from discord.ext import commands

from DiscordBot.Bot import Bot
from .modules.youtube_dl import YTDLSource
from .modules.music_play import MusicPlay
# from .modules.file_manager import FileManager
from .utils import enter_room

bot = Bot()

async def comand_error(ctx: commands.Context, error: Exception):
    """ default handle error """
    print(error)
    await ctx.send('**warning: an internal error has occurred**'.upper())

# deixar call
@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx: commands.Context):
    """ faz o bot deixar a chamada de voz """
    if ctx.voice_client and ctx.voice_client.is_connected():
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

# tocar musica ou adicionar a fila
@bot.command(name='play', help='Play a song')
async def play(ctx: commands.Context, url: str):
    """ faz o bot tocar uma música """
    if await enter_room(ctx) and ctx.voice_client:
        # pode ser um str out list[str]
        filenames = await YTDLSource.from_url(url, loop=bot.loop)

        # verifica qual dos dois é e salva na lista
        filename = filenames if isinstance(filenames, str) else filenames[0]

        # verifica se já tem uma musica tocando
        if not ctx.voice_client.is_playing():
            ctx.voice_client.play(discord.FFmpegPCMAudio(filename))
            await ctx.send(f'**Now playing:** {filename}')
        else:
            await ctx.send(f'**New music added to queue: **{filename}')

@bot.command(name='pause', help='pause the song')
async def pause(ctx: commands.Context):
    """ se o bot estiver tocando uma música, ele pausa ela """
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

# resumir musica
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx: commands.Context):
    """ se o bot deu pausa em uma música, da o re-play """
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
    else:
        await ctx.send("Mermão, já tá tocando")

# parar de tocar
@bot.command(name='stop', help='Stops the song')
async def stop(ctx: commands.Context):
    """ se o bot estiver tocando música, para sua execução e limpa a fila """
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
    else:
        await ctx.send("Não tá tocando nada seu imbecil")

@bot.command(name='skip', help='Skip to the next music')
async def skip (ctx: commands.Context):
    """ se o bot estiver tocando uma música, então ele pula a atual e vai para a próxima """
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
