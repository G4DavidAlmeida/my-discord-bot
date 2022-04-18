"""
    MusicPlayer é uma classe de gerênciamento
    de sessões de channel

    o método .play() do VoiceChannel só toca uma música por vez,
    para implementar uma fila de músicas, ManagerMPSession
    ficará encarregada disso


"""
import discord
from typing import Dict, List, Union
from .youtube_dl import YTDLSource


class MusicPlayer:
    """
        fica encarregada das funções básicas de um music player
    """

    def __init__(self, channel: discord.VoiceChannel):
        self._channel = channel
        self._queue: List[discord.FFmpegPCMAudio] = []

    def _after_callback(self, error):
        if error:
            print(f'Player error: {error}')
        self._skip()

    def play(self, musics: Union["YTDLSource", List["YTDLSource"]]):
        """
            adiciona uma musica a fila de musicas, caso nenhuma música
            esteja sendo tocada no momento, iniciamos o play

            caso vários links tenham sidos passados, adicionamos cada um deles a fila
        """
        if not isinstance(musics, (list, YTDLSource)):
            raise TypeError(
                'musics must be a list of AudioSource or a AudioSource')

        if isinstance(musics, YTDLSource):
            musics = [musics]

        for music in musics:
            self._play(music)

    def _play(self, music: Union["YTDLSource", List["YTDLSource"]]):
        """
            adiciona uma musica a fila de musicas, caso nenhuma música
            esteja sendo tocada no momento, iniciamos o play
        """
        if not self._queue and not self._channel.is_playing():
            self._channel.play(music, after=self._after_callback)

        self._queue.append(music)

    def pause(self):
        """ pausa a música atual """
        if self._channel.is_playing():
            self._channel.pause()

    def resume(self):
        """ faz a musica continuar de onde parou quando pausada """
        if not self._channel.is_playing():
            self._channel.resume()

    def _skip(self):
        """ pula a música atual """

        # estando vazia, não fazemos nada
        if self._queue:
            self._queue.pop(0)

        # se ainda houver mais um item, tocamos ele
        if self._queue:
            self._channel.play(self._queue[0], after=self._after_callback)

    def skip(self):
        """ pula o player para o próximo da lista """
        if self._channel.is_playing():
            self._channel.stop()

    def stop(self):
        """ limpa a fila de musica """
        if self._channel.is_playing():
            self._queue.clear()  # primeiro limpamos a fila
            self._channel.stop()  # e após isso, podemos parar o play

    @property
    def queue(self):
        """ copia da fila de musicas """
        return self._queue.copy()

    @property
    def queue_is_empty(self):
        return len(self._queue) == 0


class ManagerMPSession:
    """
        tem como responsabilidade abstrair a correlação
        entre o voicechannel e o MusicPlayer
    """
    _map: Dict[discord.VoiceChannel, MusicPlayer] = {}

    @classmethod
    def add_music_player(cls, channel: discord.VoiceChannel):
        """ cria uma nova instância de music player e adiciona na map """
        instance = MusicPlayer(channel)
        cls._map[channel] = instance
        return instance

    @classmethod
    def exist(cls, channel: discord.VoiceChannel):
        """ verifica se há um MusicPlayer salvo referente a esse channel """
        return channel in cls._map

    @classmethod
    def get(cls, channel: discord.VoiceChannel):
        """
            retorna uma instância de MusicPlayer mediante ao channel passado
        """
        return cls._map.get(channel)

    @classmethod
    def get_or_create(cls, channel: discord.VoiceChannel):
        """
            caso channel exista no mapeamento, retorna o mesmo, do contrário,
            se não, cria uma nova instância e salva no map
        """
        return cls.get(channel) or cls.add_music_player(channel)

    @classmethod
    def remove(cls, channel):
        """
            remove o musicplayer do mapeamento referente ao channel

            após a remoção, é feita a limpeza do musicplayer removido
            (parar a execução da musica e limpar a fila)
        """
        ms_player = cls._map.pop(channel)
        ms_player.stop()
        return ms_player
