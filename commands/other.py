import discord
import random

from discord.ext import commands
from assets.list import *

class Other(commands.Cog):
    def __init__(self, client):
        self.bot = client 

    @commands.command(aliases=['talk', 'echo'])
    async def say(self, ctx, *, message:str):
        """have the bot talk"""
        if ctx.author == ctx.author.bot:
            return
        blocked = message.replace("@everyone", "no lmao")
        await ctx.send("{}".format(blocked.replace("@here", "no lmao")))

    @commands.command(name="8ball")
    async def ball(self, ctx, question):
        """ask the bot something and get a bullshit response"""
        r = random.choice(responses)
        await ctx.send(r)

    @commands.command(aliases=['bruh'])
    async def square(self, ctx):
        """bruh"""
        nigerian = random.choice(emo)
        await ctx.send(nigerian)

    @commands.command(aliases=['removebronx'])
    async def speed(self, ctx):
        """m"""
        brooklyn = random.choice(superior)
        await ctx.send(brooklyn)

    @commands.command(aliases=['virginia'])
    async def super(self, ctx):
        """speed = small [ CENSORED BY DEV ]"""
        stolenquotes = random.choice(stopgivingmefunctions)
        await ctx.send(stolenquotes)

    @commands.command(aliases=['robin'])
    async def terminal(self, ctx):
        """:pensi"""
        await ctx.send(":pensive: <@117678528220233731>")

def setup(client):
    client.add_cog(Other(client))