class FakeClientVoice:
    """ voice channel fake """

    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs

    def is_playing(self):
        """ mock de is_playing, remete se o player está tocando uma música """
        return self.kwargs.get('is_playing')

    def is_connected(self):
        """ informa se o cliente de voz da mensagem está connectado """
        return self.kwargs.get('is_connected', True)

    async def disconnect(self):
        """ simula a desconexão do cliente de voz """

    def play(self, source, after=None):
        """ mock de play, apenas um método vazio """

    def stop(self):
        """ mock de stop, apenas um método vazio """


class FakeMessage:
    """ mensagem falso para uso nos testes """


class FakeContext:
    """ contexto falso para simular nos testes """

    def __init__(self, voice_client=None, message=None, **kwargs):
        self.voice_client = voice_client or FakeClientVoice()
        self.message = message or FakeMessage()
        self.kwargs = kwargs

    async def send(self, text):
        """ simula um envio de mensagem no contexto """
