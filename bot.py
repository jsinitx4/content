import discord
from discord.ext import commands

TOKEN = ' '

client = commands.Bot(command_prefix = 'c!')

@client.event
async def on_ready():
    print("ready to die")
    await client.change_presence(status=discord.Status.dnd, activity = discord.Activity(name="little t bg media scary moments", url="https://www.twitch.tv/monstercat", type=discord.ActivityType.streaming))

@client.event
async def on_command_error(ctx, error):
    await ctx.send("something happened: `{}`".format(error))
    
@client.command(pass_context=True)
async def say(ctx, *, content:str):
    """have the bot talk"""
    await ctx.send(content)

client.run(TOKEN)
