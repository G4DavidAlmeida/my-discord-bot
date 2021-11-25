"""
    testes de music player
"""
from unittest import TestCase
from DiscordBot.music.modules.music_play import MusicPlayer


class MusicPlayerTest(TestCase):
    """ testes de music player """

    def setUp(self):
        self.voice_channel = object()
        self.music_player = MusicPlayer(self.voice_channel)

    def test_play(self):
        """ testando play """
