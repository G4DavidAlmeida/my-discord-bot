class GameStateMap:
    """
        devido ao fato do bot poder ser utilizado por
        mais de um server, ou futuramente dividir estados
        por canal de voz, é preciso haver uma mapeamento
        entre entre os server e seu estado de game
    """
    _map = None
