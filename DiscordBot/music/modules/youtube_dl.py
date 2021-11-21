import youtube_dl
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
    'format': 'worstaudio/worst',
    'restrictfilenames': True,
    'default_search': 'auto',
    'nooverwrites': True,
    'source_address': '0.0.0.0', # bind to ipv4 since ipv6 addresses cause issues sometimes
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

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
