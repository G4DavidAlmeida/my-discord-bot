from typing import Optional
from youtube_dl import YoutubeDL
import discord
import asyncio


class MyLogger:
    """ classe de log do youtube dl customizada """

    def debug(self, msg):
        """ TODO entender pra que serve """

    def warning(self, msg):
        """ TODO entender pra que serve """

    def error(self, msg):
        """ TODO entender pra que serve """


def my_hook(d):
    """ progress_hooks:
            * status: "downloading", "error", or "finished"

            If status is one of "downloading", or "finished", the
            following properties may also be present:
            * filename: The final filename (always present)
            * tmpfilename: The filename we're currently writing to
            * downloaded_bytes: Bytes on disk
            * total_bytes: Size of the whole file, None if unknown
            * total_bytes_estimate: Guess of the eventual file size, None if unavailable.
            * elapsed: The number of seconds since download started.
            * eta: The estimated time in seconds, None if unknown
            * speed: The download speed in bytes/second, None if unknown
            * fragment_index: The counter of the currently downloaded video fragment.
            * fragment_count: The number of fragments (= individual files that will be merged)
    """
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
    if d['status'] == 'downloading':
        print('download in progress')
    else:
        print('download failed')


ytdl_format_options = {
    'outtmpl': 'static/audios/%(extractor_key)s/%(id)s-%(title)s.%(ext)s',
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'default_search': 'auto',
    'noplaylist': False,
    'nooverwrites': True,
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0',
    # 'postprocessors': [{
    #     'key': 'FFmpegExtractAudio',
    #     'preferredcodec': 'mp3',
    #     'preferredquality': '192',
    # }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

ffmpeg_options = {
    'options': '-vn'
}


class YTDLSource(discord.PCMVolumeTransformer):
    """
        Permite um maior controle sobre os audios executados
        no .play() do VoiceChannel()
    """

    def __init__(self, source, *, data, volume=0.1):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    def _create_source(cls, item, stream: bool, ytdl):
        filename = item['url'] if stream else ytdl.prepare_filename(item)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=item)

    @classmethod
    async def from_url(
        cls,
        url: str,
        *,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        stream: bool = False
    ):
        """
            faz o download da musica mediante a url passada
            `url`: a url da música a ser baixada
            `loop`: é o evento loop do bot,
            `stream`; se verdadeiro, baixar o vídeo em stream
            tornando o download rápido e eliminando a necessidade
            de usar o sistema de arquivos (FileSystem)
        """
        loop = loop or asyncio.get_event_loop()
        with YoutubeDL(ytdl_format_options) as ytdl:
            data = await loop.run_in_executor(
                None, lambda: ytdl.extract_info(url, download=not stream))

            if 'entries' in data:
                return [cls._create_source(item, stream, ytdl) for item in data['entries']]

            return [cls._create_source(data, stream, ytdl)]

    def __str__(self) -> str:
        return str(self.title)
