import os
from dotenv import load_dotenv

from DiscordBot.Bot import Bot

# só a importação garante que todos os serviços serão carregados
from DiscordBot import loading_services

load_dotenv(dotenv_path='./env/.env')

# Get the API token from the .env file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = Bot()

if __name__ == "__main__" :
    bot.run(DISCORD_TOKEN)