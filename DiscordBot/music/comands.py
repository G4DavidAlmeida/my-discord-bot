import discord

from DiscordBot.Bot import Bot
from .modules.youtube_dl import YTDLSource
from .modules.music_play import MusicPlay
from .modules.file_manager import FileManager
from .utils import enter_room

bot = Bot()
media_play = MusicPlay()

async def comand_error(ctx, error: Exception):
    """ default handle error """
    print(error)
    await ctx.send('**warning: an internal error has occurred**'.upper())

# deixar call
@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    try:
        voice_client = ctx.message.guild.voice_client
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
            media_play.clear_queue()
        else:
            await ctx.send("The bot is not connected to a voice channel.")
    except Exception as e:
        await comand_error(ctx, e)

# tocar musica ou adicionar a fila
@bot.command(name='play', help='Play a song')
async def play(ctx, url: str):
    try:
        if not await enter_room(ctx):
            return

        await ctx.send('**start download**')

        server = ctx.message.guild
        voice_client = server.voice_client

        # verifica se o canal de voz ainda é o mesmo
        if not (media_play.voice_client is voice_client):
            media_play.voice_client = voice_client

        # pode ser um str out list[str]
        filenames = await YTDLSource.from_url(url, loop=bot.loop)

        # verifica qual dos dois é e salva na lista
        if isinstance(filenames, str):
            filename = filenames
            media_play.add_music_to_queue(filename)
        else:
            for file in filenames:
                media_play.add_music_to_queue(file)
            filename = filenames[0]

        # verifica se já tem uma musica tocando
        if not voice_client.is_playing():
            # async with ctx.typing():
            voice_client.play(discord.FFmpegPCMAudio(filename), after=media_play.next_track)
            await ctx.send(f'**Now playing:** {filename}')
        else:
            await ctx.send(f'**New music added to queue: **{filename}')
    except Exception as e:
        await comand_error(ctx, e)


# pausar musica
@bot.command(name='pause', help='pause the song')
async def pause(ctx):
    try:
        if not ctx.message.guild.voice_client:
            return

        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")
    except Exception as e:
        await comand_error(ctx, e)

# resumir musica
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    try:
        if not ctx.message.guild.voice_client:
            return

        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play command")
    except Exception as e:
        await comand_error(ctx, e)

# parar de tocar
@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    try:
        if not ctx.message.guild.voice_client:
            return

        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            media_play.clear_queue()
        else:
            await ctx.send("The bot is not playing anything at the moment.")
    except Exception as e:
        await comand_error(ctx, e)

@bot.command(name='skip', help='Skip to the next music')
async def skip (ctx):
    try:
        if not ctx.message.guild.voice_client:
            return
        
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")
    except Exception as e:
        await comand_error(ctx, e)