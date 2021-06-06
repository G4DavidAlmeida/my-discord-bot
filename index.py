import os

# load envs first of all
from dotenv import load_dotenv
load_dotenv(dotenv_path='./env/.env')

from DiscordBot.Bot import Bot
from DiscordBot import config # carrega todos os serviços

# Get the API token from the .env file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = Bot()

if __name__ == "__main__" :
    bot.run(DISCORD_TOKEN)
