async def enter_room (ctx):
    try:
        # se não connectado, então connectar
        if not ctx.message.guild.voice_client:
            if not ctx.author.voice:
                await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel")
                return False
            else:
                channel = ctx.author.voice.channel
            await channel.connect()
        return True
    except Exception as e:
        print(e)
        return False