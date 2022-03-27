"""
    testes de music player
"""
import asyncio
from unittest import TestCase
from unittest.mock import MagicMock
from apps.music.modules.music_play import MusicPlayer, YTDLSource

from ..utils import FakeClientVoice


class MusicPlayerTest(TestCase):
    """ testes de music player """

    def setUp(self) -> None:
        loop = asyncio.get_event_loop()
        self.music_links = loop.run_until_complete(asyncio.gather(
            YTDLSource.from_url(
                'https://www.youtube.com/watch?v=fRenWezrDxg', stream=True),
            YTDLSource.from_url(
                'https://www.youtube.com/watch?v=fRenWezrDxg', stream=True),
        ))

    def test_play_success(self):
        """
            FLUXO DE DADOS
            ao passar um link do youtube por parâmetro na função,
            deverá adicionar uma música na fila
        """

        voice_channel = FakeClientVoice()
        voice_channel.play = MagicMock()

        music_player = MusicPlayer(voice_channel)
        music_player.play(self.music_links[0])

        # a lista de músicas não deverá estar vazia
        self.assertFalse(music_player.queue_is_empty)

    def test_add_on_queue_play(self):
        """
            TESTE DE ESTRUTURA DE CONTROLE
            quando houver uma música na fila, ao adicionar mais uma,
            ele deverá esperar na fila e não chamar o play
        """

        # simula que há música tocando
        voice_channel = FakeClientVoice(is_playing=True)
        voice_channel.play = MagicMock()

        music_player = MusicPlayer(voice_channel)
        music_player.play(self.music_links[0])

        voice_channel.play.assert_not_called()

    def test_add_many_musics(self):
        """
            TESTE DE CICLO

            se mais de uma música foi passada, então adiciona todas a fila
        """

        voice_channel = FakeClientVoice()
        music_player = MusicPlayer(voice_channel)

        music_player.play(self.music_links)
        # valida se foram chamadas várias vezes
        self.assertEqual(music_player.queue, self.music_links)

    def test_stop_music(self):
        """
            TESTE DE CAMINHO

            se não houver nenhuma musica tocando, então
            não deverá fazer nada
        """
        voice_channel = FakeClientVoice()
        voice_channel.stop = MagicMock()

        music_play = MusicPlayer(voice_channel)
        music_play.stop()

        voice_channel.stop.assert_not_called()
