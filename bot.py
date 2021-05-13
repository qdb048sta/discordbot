# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

client.run(TOKEN)
@bot.event
async def on_message_delete(message):
    Tracker_id = 815980145235591249   #這段放自己BOT的ID
    if message.author.id != Tracker_id:
        await message.channel.send(F'{message.author.mention} 還敢偷刪訊息阿： {message.content}')