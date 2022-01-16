"""
    inicializador do discord python
"""
import logging

from DiscordBot.Bot import Bot


# configurando logger
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Get the API token from the .env file.

if __name__ == "__main__":
    Bot().run()
