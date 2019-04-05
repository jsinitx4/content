# literally useless
import discord 
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command(aliases=['summon', 'connect'])
    async def join(self, ctx):
        """connects bot to vc"""
        await ctx.author.voice.channel.connect()
        await ctx.send("i'm in")

    @commands.command(aliases=['disconnect'])
    async def leave(self, ctx):
        """disconnects bot from vc"""
        await ctx.voice_client.disconnect()
        await ctx.send("ok bye")

def setup(client):
    client.add_cog(Music(client))