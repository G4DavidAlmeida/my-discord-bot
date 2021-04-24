import os
from dotenv import load_dotenv
from src.music import bot

load_dotenv(dotenv_path='./env/.env')

# Get the API token from the .env file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


if __name__ == "__main__" :
    bot.run(DISCORD_TOKEN)