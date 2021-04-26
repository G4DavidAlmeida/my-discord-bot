from DiscordBot.Bot import Bot

import pprint
log = pprint.PrettyPrinter(indent=2).pprint

bot = Bot()

@bot.event
async def on_ready():
    print('Bot discord is ready!')

""" @bot.event
async def on_voice_state_update (ctx, *args, **kwargs):
    log(ctx)

@bot.event
async def on_voice_server_update(ctx, *args, **kwargs):
    log(ctx) """