import discord # rewrite
import random

from discord.ext import commands
from re import match
from assets.list import *

TOKEN = open("token.txt", "r").read()
blacklist = []

client = commands.Bot(command_prefix = 'c!')

extensions = [
    "commands.moderation",
    "commands.info",
    "commands.music",
    "commands.other"
]

if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
            print(f"{extension}" + " loaded successfully")
        except Exception as e:
            print("{} didn't load {}".format(extension, e))

# events

@client.event
async def is_owner(ctx):
    return ctx.author.id == 365274392680333329

@client.event
async def on_ready():
    print("ready to die")
    await client.change_presence(activity = discord.Activity(name="OK 🤣🤣🤣 BOOMER 😂😂😂", url="https://www.twitch.tv/monstercat", type=discord.ActivityType.streaming))

@client.event
async def on_command_error(ctx, error):
    await ctx.send("something happened: `{}`".format(error))

@client.before_invoke
async def on_command_preprocess(ctx):
    print(f"{ctx.message.author}" + " (" + f"{ctx.message.author.id}" + ") " + "ran the command: " + f"{ctx.message.content}" + " in the guild: " f"{ctx.message.guild.name}" + " (" + f"{ctx.message.guild.id}" + ")")

@client.event
async def on_message(message):
    if match("<@!?552616565754036239>", message.content) is not None:
        resp = random.choice(mentionrsp)
        await message.channel.send(resp)

    if message.author.id in blacklist and message.content.startswith('c!'):
        await message.channel.send("bruh you're blacklisted")
        print("[blacklist] {} tried running {}".format(message.author, message.content))
        return
    await client.process_commands(message)

# commands

@client.command(hidden=True)
@commands.check(is_owner)
async def fetch(ctx):
    """good dog"""
    servers = await client.fetch_guilds(limit=25).flatten()
    await ctx.send("aight check your dms b")
    await ctx.author.send("```py\n" + f"{servers}" + "\n```")

@client.command(hidden=True)
@commands.check(is_owner)
async def activity(ctx, activitytype:str, *, status:str):
    """changes the streaming status"""
    if activitytype == "s":
        await client.change_presence(activity = discord.Activity(name=status, url="https://www.twitch.tv/monstercat", type=discord.ActivityType.streaming))
    elif activitytype == "p":
        await client.change_presence(activity=discord.Game(name=status))
    elif activitytype == "l":
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
    elif activitytype == "w":
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
    await ctx.send("done changed the status to " + "**" + status + "**")

@client.command(hidden=True, aliases=['enable'])
@commands.check(is_owner)
async def load(ctx, extension):
    """enables said extension"""
    try:
        client.load_extension(extension)
        await ctx.send("loaded {} successfully".format(extension))
        print("loaded {} successfully".format(extension))
    except Exception as e:
        await ctx.send("{} didn't load successfully: `{}`".format(extension, e))
        print("{} didn't load successfully: {}".format(extension, e))

@client.command(hidden=True, aliases=['disable'])
@commands.check(is_owner)
async def unload(ctx, extension):
    """disables said extension"""
    try:
        client.unload_extension(extension)
        await ctx.send("unloaded {} successfully".format(extension))
        print("unloaded {} successfully".format(extension))
    except Exception as e:
        await ctx.send("{} didn't unload successfully: `{}`".format(extension, e))
        print("{} didn't unload successfully: {}".format(extension, e))

@client.command(hidden=True)
@commands.check(is_owner)
async def reload(ctx, extension):
    """reloads said extension"""
    try:
        client.unload_extension(extension)
        client.load_extension(extension)
        await ctx.send("reloaded {} successfully".format(extension))
        print("reloaded {} successfully".format(extension))
    except Exception as e:
        await ctx.send("{} didn't reload successfully: `{}`".format(extension, e))
        print("{} didn't reload successfully: {}".format(extension, e))

# you will be blacklisted if you abuse this etc etc
@client.command()
async def suggest(ctx, *, suggestion:str):
    """suggest a feature"""
    user = client.get_user(365274392680333329)
    await user.send(f"suggestion from **{ctx.author} ({ctx.author.id})**: {suggestion}")
    await ctx.send("ok your suggestion has been sent to the bot dev")

@client.command(hidden=True)
@commands.check(is_owner)
async def dm(ctx, id:int, *, message:str):
    """sends a message to a user"""
    await client.get_user(id).send(message)
    await ctx.send(f"sent a dm to: **{id}**")

@client.command(hidden=True)
@commands.check(is_owner)
async def cm(ctx, id:int, *, message:str):
    """sends a message to a channel"""
    await client.get_channel(id).send(message)
    await ctx.send(f"sent a message to channel: **{id}**")

@client.command(hidden=True)
@commands.check(is_owner)
async def shutdown(ctx):
    """shuts the bot down"""
    await ctx.send("bye")
    await client.logout()

client.run(TOKEN)