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

    @commands.command()
    async def botinvite(self, ctx):
        """sends you a shady link"""
        await ctx.author.send("https://speed-is-a.living-me.me/s/gaqo") # is this an ip logger?
        await ctx.send("check your dms thanks")

    @commands.command()
    async def serverinvite(self, ctx):
        """invite your bros :brofist:"""
        link = await ctx.channel.create_invite(max_age = 86400, max_uses = 0)
        await ctx.channel.trigger_typing()
        await ctx.send("invite your bros :brofist:")
        await ctx.send(link)

    @commands.command(aliases=['bruh'])
    async def square(self, ctx):
        """bruh"""
        nigerian = random.choice(emo)
        await ctx.send(nigerian)

def setup(client):
    client.add_cog(Other(client))
