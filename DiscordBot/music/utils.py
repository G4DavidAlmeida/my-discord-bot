import discord

class MusicPlay(object):
    queue_music = []
    voice_client = None
    ctx_send = None

    async def next_track(self, error):
        if error:
            print(error)

        if len(self.queue_music) <= 1:
            return

        self.queue_music.pop(0)
        filename = self.queue_music[0]
        self.voice_client.play(discord.FFmpegPCMAudio(filename),
                                            after=self.next_track)

        await self.ctx_send(f'**Now playing:** {filename}')
    
    def add_music_to_queue(self, path):
        self.queue_music.append(path)