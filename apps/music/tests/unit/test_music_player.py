"""
    testes de music player
"""
from unittest import TestCase
from apps.music.modules.music_play import MusicPlayer


def create_fake_client_voice():
    """ cria um voice fake """
    voice = object()
    return voice


class MusicPlayerTest(TestCase):
    """ testes de music player """

    def setUp(self):
        self.voice_channel = create_fake_client_voice()
        self.music_player = MusicPlayer(self.voice_channel)

    def test_play(self):
        """ testando play """
