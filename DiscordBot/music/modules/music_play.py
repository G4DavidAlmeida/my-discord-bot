"""
    MusicPlayer é uma classe de gerênciamento
    de sessões de channel

    o método .play() do VoiceChannel só toca uma música por vez,
    para implementar uma fila de músicas, ManagerMPSession
    ficará encarregada disso


"""
import discord
from typing import Dict, List
from .youtube_dl import YTDLSource

class MusicPlayer:
    """
        fica encarregada das funções básicas de um music player
    """
    def __init__(self, channel: discord.VoiceChannel):
        self._channel = channel
        self._queue: List[discord.FFmpegPCMAudio] = []

    def play(self, music: YTDLSource):
        """
            adiciona uma musica a fila de musicas, caso a lista esteja vazia
            o play é executado
        """

        # a fila estando vazia, tocamos a musica antes de adicionar a queue
        if not self._queue:
            self._channel.play(music)

        self._queue.append(music)

    def pause(self):
        """ pausa a música atual """
        self._channel.pause()

    def skip(self):
        """ pula a música atual """

        # estando vazia, não fazemos nada
        if self._queue:
            self._channel.stop()
            self._queue.pop(0)

        # se ainda houver mais um item, tocamos ele
        if self._queue:
            self._channel.play(self._queue[0])

    def stop(self):
        """ limpa a fila de musica """
        self._channel.stop()
        self._queue.clear()
        

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
        return cls._map.pop(channel)
