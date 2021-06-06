import discord
from .youtube_dl import ffmpeg_options
from .file_manager import FileManager

class MusicPlay(object):
    _can_continue = True
    _queue_music = []
    voice_client = None

    def next_track(self, error):
        """
            Preste atenção  ao tempo do código, esta função é executada
            quando um musica acaba ou quando ela é parada por exemplo no comando
            voice_client.stop(), isso se não observado poderá causar alguns bugs
            ou erros, gerando um tempo de execução no código confuso
        """
        error and print(error)

        if self._can_continue and self.remove_from_queue():
            self.voice_client.play(discord.FFmpegPCMAudio(self._queue_music[0],
                before_options=ffmpeg_options['options']), after=self.next_track)

    def remove_from_queue (self):
        if len(self._queue_music) == 0:
            return False

        FileManager.delete_music(self._queue_music[0])
        self._queue_music.pop(0)

        return len(self._queue_music) > 0
        
    def clear_queue(self):
        self._can_continue = False
        FileManager.remove_list(self._queue_music)        
        self._queue_music.clear()
        self._can_continue = True
        
    
    def add_music_to_queue(self, path):
        self._queue_music.append(path)