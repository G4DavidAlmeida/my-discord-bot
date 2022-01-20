"""
    todas as váriaveis necessárias para o funcionamento do bot
    devem ser carregadas aqui, tais elas como o toke do discord
    chaves de segurança e API, etc
"""
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./env/.env')

# carregando serviço de musica
APPLICATIONS = [
    'apps.music',
    'apps.gifs',
]

DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_TOKEN = os.getenv("DISCORD_CLIENT_TOKEN")
DISCORD_PREFIX = os.getenv('DISCORD_PREFIX')

GIPHY_API_KEY = os.getenv('GIPHY_API_KEY')
