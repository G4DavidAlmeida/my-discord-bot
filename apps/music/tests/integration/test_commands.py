"""
    suite de testes dos commandos da aplicação music
"""
import asyncio
from unittest import TestCase
from unittest.mock import AsyncMock

from apps.music.modules.music_play import ManagerMPSession
from apps.music import commands as music_commands

from .. import utils


class TestComands(TestCase):
    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.context = utils.FakeContext()
        self.voice_client = self.context.voice_client

    def test_leave_command(self):
        """
            TESTE DE CASO DE USO

            o commando leave fará com que o bot caso connectado
            a um cliente de voz, desconectar, e remover ele
            da lista de sessões de music player da classe
            ManagerMPSession

            caso o bot não esteja conectado ele apenas enviará uma
            mensagem informando que o bot não está conectado
        """
        # configurando
        ManagerMPSession.add_music_player(self.context.voice_client)
        self.voice_client.disconnect = AsyncMock()

        self.loop.run_until_complete(music_commands.leave(self.context))

        self.voice_client.disconnect.assert_called_once()
        self.assertFalse(ManagerMPSession.exist(self.voice_client))

    def test_fail_leave_command(self):
        """
            TESTE DE CASO DE USO

            caso o bot não esteja conectado, deverá chammar o método
            send de context com uma mesagem informando que o bot não está conectado
        """
        # configurando
        self.context.send = AsyncMock()
        self.context.voice_client.kwargs['is_connected'] = False

        # executando
        self.loop.run_until_complete(music_commands.leave(self.context))

        # validando resultados
        self.context.send.assert_called_once_with(
            "The bot is not connected to a voice channel.")
