import discord
import random

from discord.ext import commands
from assets.list import *

class Other(commands.Cog):
    def __init__(self, client):
        self.bot = client 

    @commands.command(aliases=['talk', 'echo'])
    async def say(self, ctx, *, content:str):
        """have the bot talk"""
        await ctx.send(content)

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

def setup(client):
    client.add_cog(Other(client))
