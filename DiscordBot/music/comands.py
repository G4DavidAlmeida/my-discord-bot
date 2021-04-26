import discord

from DiscordBot.Bot import Bot
from .modules.youtube_dl import YTDLSource
from .utils import MusicPlay

bot = Bot()
media_play = MusicPlay()

# deixar call
@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    try:
        voice_client = ctx.message.guild.voice_client
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")
    except Exception as e:
        print(e)

# tocar musica ou adicionar a fila
@bot.command(name='play', help='To play song')
async def play(ctx,url):
    try :
        # se não connectado, então connectar
        if not ctx.message.guild.voice_client:
            if not ctx.author.voice:
                await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel")
                return
            else:
                channel = ctx.author.voice.channel
            await channel.connect()

        server = ctx.message.guild
        voice_client = server.voice_client

        # verifica se o canal de voz ainda é o mesmo
        if not (media_play.voice_client is voice_client):
            media_play.voice_client = voice_client
            

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            media_play.add_music_to_queue(filename)
            media_play.ctx_send = ctx.send

            if not voice_client.is_playing():
                voice_client.play(discord.FFmpegPCMAudio(filename), after=media_play.next_track)

                await ctx.send(f'**Now playing:** {filename}')
            else:
                await ctx.send(f'**New music added to queue: **{filename}')
    except Exception as e:
        print(e)


# pausar musica
@bot.command(name='pause', help='This command pauses the song')
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
        print(e)

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
        print(e)

# parar de tocar
@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    try:
        if not ctx.message.guild.voice_client:
            return

        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            media_play.queue_music.clear()
        else:
            await ctx.send("The bot is not playing anything at the moment.")
    except Exception as e:
        print(e)

@bot.command(name='skip', help='Skip to the next music')
async def skip (ctx):
    try:
        if not ctx.message.guild.voice_client:
            return
        
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            await media_play.next_track(None)
        else:
            await ctx.send("The bot is not playing anything at the moment.")
    except Exception as e:
        print(e)