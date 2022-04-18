"""
    comandos da aplicação music
"""
from datetime import timedelta
from discord.ext import commands

from DiscordBot.Bot import Bot
from DiscordBot.configs.commands import BaseAppCommands
from DiscordBot.utils import command_error

from youtube_dl.YoutubeDL import DownloadError

from .modules.youtube_dl import YTDLSource
from .utils import enter_room, music_message_add
from .modules.music_play import ManagerMPSession


class MusicCommands(BaseAppCommands):
    """ commands of music app """

    def initializer(self):
        self.sessions = ManagerMPSession

    async def command_leave(self, ctx: commands.Context):
        """ To make the bot leave the voice channel """
        if ctx.voice_client and ctx.voice_client.is_connected():
            self.sessions.remove(ctx.voice_client)
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    async def command_play(self, ctx: commands.Context, url: str = None):
        """ Play a song """
        if not url:
            await ctx.send('O comando play requer a URL do vídeo ou um texto de pesquisa')

        elif await enter_room(ctx) and ctx.voice_client:
            music_play = self.sessions.get_or_create(ctx.voice_client)

            async with ctx.typing():
                try:
                    player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)

                except DownloadError as err:
                    if 'Unsupported' in err.args[0]:
                        await ctx.send('O link fornecido não é suportado')
                    else:
                        await command_error(ctx, err)

                else:
                    if not player:  # pode haver casos de não achar nenhum link
                        await ctx.send(f'Não foi encontrado nenhum source para {url}')
                    else:
                        music_play.play(player)
                        await music_message_add(ctx, music_play, player[0])

    async def command_pause(self, ctx: commands.Context):
        """ pause the song """
        if ctx.voice_client:
            music_play = self.sessions.get(ctx.voice_client)
            if music_play:
                music_play.pause()

    async def command_resume(self, ctx: commands.Context):
        if ctx.voice_client:
            music_play = self.sessions.get(ctx.voice_client)
            if music_play:
                music_play.resume()

    async def command_stop(self, ctx: commands.Context):
        """ Stops the song """
        if ctx.voice_client:
            music_play = self.sessions.get(ctx.voice_client)
            if music_play:
                music_play.stop()

    async def command_skip(self, ctx: commands.Context):
        """ Skip to the next music """
        if ctx.voice_client:
            music_play = self.sessions.get(ctx.voice_client)
            if music_play:
                music_play.skip()

    async def command_list_queue(self, ctx: commands.Context):
        """ lista as músicas que estão na fila """
        if ctx.voice_client and self.sessions.exist(ctx.voice_client):
            music_play = self.sessions.get(ctx.voice_client)

            list_text = ''

            for index, music in enumerate(music_play.queue):
                time = timedelta(seconds=music.data.get('duration'))
                list_text += f'{index + 1} - {music} **{time}**\n'

            if list_text:
                await ctx.send(list_text)
