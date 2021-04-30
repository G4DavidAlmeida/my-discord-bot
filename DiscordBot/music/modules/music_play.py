import discord
from .youtube_dl import ffmpeg_options
from .file_manager import FileManager

class MusicPlay(object):
    can_continue = True
    queue_music = []
    voice_client = None

    def next_track(self, error):
        """
            Preste atenção  ao tempo do código, esta função é executada
            quando um musica acaba ou quando ela é parada por exemplo no comando
            voice_client.stop(), isso se não observado poderá causar alguns bugs
            ou erros, gerando um tempo de execução no código confuso
        """
        if error:
            print(error)

        if self.remove_from_queue() and self.can_continue:
            self.voice_client.play(discord.FFmpegPCMAudio(self.queue_music[0],
                before_options=ffmpeg_options['options']), after=self.next_track)

    def remove_from_queue (self):
        if len(self.queue_music) == 0:
            return False

        FileManager.delete_music(self.queue_music[0])
        self.queue_music.pop(0)

        return len(self.queue_music) > 0
        
    def clear_queue(self):
        self.can_continue = False
        for filename in self.queue_music:
            FileManager.delete_music(filename)
        
        self.queue_music.clear()
        self.can_continue = True
        
    
    def add_music_to_queue(self, path):
        self.queue_music.append(path)