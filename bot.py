import discord
from discord.ext import commands
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '!', intents = intents)
client = discord.Client(intents = intents)

bot.remove_command("help")

TOKEN = "ODQyMzA5NjIzMzg1ODE3MTE4.YJzb9w.pL8HXFCNaBNJjDn2QaNFVQdqfDc"

@bot.command()
async def help(ctx):
    a = "css\n"
    b = "1. !rank {[cmd]+[SERVER]}⤵\n"
    c = "  - Track once an hour, can know pts/hour\n\n"
    d = "2. !point {[cmd]+[SERVER]}⤵\n"
    e = "  - Track every 2 minutes, can know pts/game\n\n\n"
    f = "[cmd] has 3 choice⤵\n"
    g = "(1) run\n  - Start the tracker\n\n"
    h = "(2) stop\n  - Stop the tracker\n\n"
    i = "(3) clean\n  - Clean the data [USE THIS CMD WHEN EVENT CHANGE]\n\n\n"
    j = "[SERVER] only can choose TW、JP ('tw、jp' ✘, 'TW、JP' ✔)\n\n\n"
    k = "For example:  !rank runTW"
    await ctx.send(f"```{a}{b}{c}{d}{e}{f}{g}{h}{i}{j}{k}```")

@bot.event
async def on_ready():
    print(">> 時速警察已上線 <<")

@bot.event
async def on_message_delete(message):
    Tracker_id = 815980145235591249
    if message.author.id != Tracker_id:
        await message.channel.send(F'{message.author.mention} 還敢偷刪訊息阿： {message.content}')

@bot.command()
async def load(ctx, extension):
    bot.load_extension(F'cmds.{extension}')
    await ctx.send(F'loaded {extension} done.')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(F'cmds.{extension}')
    await ctx.send(F'un - lo aded {extension} done.')

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(F'cmds.{extension}')
    await ctx.send(F're - loaded {extension} done.')

'''for filename in os.listdir('./discordbot'):
    if filename.endswith('.py'):
        bot.load_extension(F'cmds.{filename[:-3]}')
'''
if __name__ == "__main__":
    bot.run(TOKEN)