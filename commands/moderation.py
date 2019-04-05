import discord
from discord.ext import commands 

class Moderation(commands.Cog):
    def __init__(self, client):
        self.bot = client 

    @commands.command(aliases=['prune'])
    async def purge(self, ctx, *, number:int):
        """delete this"""
        if ctx.message.author.guild_permissions.manage_messages:
            delethis = await ctx.message.channel.purge(limit=number)
            await ctx.send("purged " + f"{len(delethis)}" + " messages")
        else:
            await ctx.send("no permissions to run purge :pensive:")

    @commands.command(aliases=['banish'])
    async def ban(self, ctx, member:discord.Member, *, reason:str):
        """*swings ban hammer upon thy*"""
        if member.guild_permissions.manage_messages:
            await ctx.send("can't ban them they're a mod")
        elif ctx.message.author.guild_permissions.ban_members:
            guild = ctx.guild.name
            await member.send("ily but you're banned from " + "**" + f"{guild}" + "**" + " now")
            await member.ban(reason=reason)
            await ctx.send("ok banned " + "**" + f"{member}" + "**" + " for " + "**" + f"{reason}" + "**")
        else:
            await ctx.send("no permissions to run ban :pensive:")

    @commands.command()
    async def kick(self, ctx, member:discord.Member, *, reason:str):
        """lol cucked"""
        if member.guild_permissions.manage_messages:
            await ctx.send("can't kick them they're a mod")
        elif ctx.message.author.guild_permissions.ban_members:
            guild = ctx.guild.name 
            await member.send("ily but you've been kicked from " + "**" + f"{guild}" + "**")
            await member.kick(reason=reason)
            await ctx.send("ok kicked " + "**" + f"{member}" + "**" + " for " + "**" + f"{reason}" + "**")
        else:
            await ctx.send("no permissions to run kick :pensive:")

def setup(client):
    client.add_cog(Moderation(client))