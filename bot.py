import discord #rewrite
import random
import time 
import youtube_dl

from assets.list import *
from discord.ext import commands

TOKEN = open("token.txt", "r").read()

client = commands.Bot(command_prefix = 'c!')

async def is_owner(ctx):
    return ctx.author.id == 365274392680333329

@client.event
async def on_ready():
    print("ready to die")
    await client.change_presence(activity = discord.Activity(name="minecraft 😔", url="https://www.twitch.tv/monstercat", type=discord.ActivityType.streaming))

@client.event
async def on_command_error(ctx, error):
    await ctx.send("something happened: `{}`".format(error))

@client.command(aliases=['talk', 'echo'])
async def say(ctx, *, content:str):
    """have the bot talk"""
    await ctx.send(content)

@client.command(aliases=['summon', 'connect'])
async def join(ctx):
    """connects bot to vc"""
    await ctx.author.voice.channel.connect()
    await ctx.send("i'm in")

@client.command(aliases=['disconnect'])
async def leave(ctx):
    """disconnects bot from vc"""
    await ctx.voice_client.disconnect()
    await ctx.send("ok bye")

@client.command(aliases=['dev', 'creator'])
async def developer(ctx):
    """who"""
    await ctx.send("speed#3413")

@client.command(aliases=['latency'])
async def ping(ctx):
    """bot latency"""
    time1 = time.perf_counter()
    await ctx.channel.trigger_typing()
    time2 = time.perf_counter()
    await ctx.send("latency: `{}`ms".format(round((time2-time1)*1000)))

@client.command(name="8ball")
async def ball(ctx, question):
    """ask the bot something and get a bullshit response"""
    r = random.choice(responses)
    await ctx.send(r)

@client.command(hidden=True)
@commands.check(is_owner)
async def shutdown(ctx):
    """shuts the bot down"""
    await ctx.send("Ok")
    await client.close()

client.run(TOKEN)
