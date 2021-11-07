import os
import logging

from dotenv import load_dotenv

from DiscordBot.Bot import Bot
from DiscordBot import config # carrega todos os serviços

load_dotenv(dotenv_path='./env/.env')

# configurando logger
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Get the API token from the .env file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = Bot()

if __name__ == "__main__" :
    bot.run(DISCORD_TOKEN)
