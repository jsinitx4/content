import discord
import asyncio
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

    @commands.command()
    async def addrole(self, ctx, member:discord.Member, *, name:str):
        """adds a role to said member"""
        if ctx.message.author.guild_permissions.manage_roles:
            role = discord.utils.get(ctx.guild.roles, name=name)
            await member.add_roles(role)
            await ctx.send("added " + "**" + f"{name}" + "**" + " role to " + f"{member}")
        else:
            await ctx.send("no permissions to run addrole :pensive:")

    @commands.command()
    async def createrole(self, ctx, *, name:str):
        """creates a role"""
        if ctx.message.author.guild_permissions.manage_roles:
            guild = ctx.guild
            await guild.create_role(name=name, permissions=guild.default_role.permissions)
            await ctx.send("created role " + "**" + f"{name}" + "**")
        else:
            await ctx.send("no permissions to run createrole :pensive:")

    @commands.command()
    async def deleterole(self, ctx, *, name:str):
        """deletes a role"""
        if ctx.message.author.guild_permissions.manage_roles:
            role = discord.utils.get(ctx.guild.roles, name=name)
            await role.delete()
            await ctx.send("deleted role " + "**" + f"{name}" + "**")
        else:
            await ctx.send("no permissions to run deleterole :pensive:")

    @commands.command()
    async def removerole(self, ctx, member:discord.Member, *, name:str):
        """removes a role from said member"""
        if ctx.message.author.guild_permissions.manage_roles:
            role = discord.utils.get(ctx.guild.roles, name=name)
            await member.remove_roles(role)
            await ctx.send("ok removed " + "**" + f"{name}" + "**" + " from " + f"{member}")
        else:
            await ctx.send("no permissions to run removerole :pensive:")

    @commands.command(aliases=['banish'])
    async def ban(self, ctx, member:discord.Member, *, reason:str):
        """*swings ban hammer upon thy*"""
        if member.guild_permissions.manage_messages:
            await ctx.send("can't ban them they're a mod")
        elif ctx.message.author.guild_permissions.ban_members:
            guild = ctx.guild.name
            await member.ban(reason=reason)
            await member.send("ily but you're banned from " + "**" + f"{guild}" + "**" + " now")
            await ctx.send("ok banned " + "**" + f"{member}" + "**" + " for " + "**" + f"{reason}" + "**")
        else:
            await ctx.send("no permissions to run ban :pensive:")

    @commands.command()
    async def unban(self, ctx, *, member:discord.User):
        """unbans rule breaker etc etc"""
        if ctx.message.author.guild_permissions.ban_members:
            guild = ctx.guild.name
            await ctx.guild.unban(member)
            await member.send("you've been unbanned on " + "**" + f"{guild}" + "**" + " b")
            await ctx.send("ok boss unbanned " + "**" + f"{member}" + "**")
        else:
            await ctx.send("no permissions to run unban :pensive:")

    @commands.command()
    async def kick(self, ctx, member:discord.Member, *, reason:str):
        """lol cucked"""
        if member.guild_permissions.manage_messages:
            await ctx.send("can't kick them they're a mod")
        elif ctx.message.author.guild_permissions.ban_members:
            guild = ctx.guild.name 
            await member.kick(reason=reason)
            await member.send("ily but you've been kicked from " + "**" + f"{guild}" + "**")
            await ctx.send("ok kicked " + "**" + f"{member}" + "**" + " for " + "**" + f"{reason}" + "**")
        else:
            await ctx.send("no permissions to run kick :pensive:")

def setup(client):
    client.add_cog(Moderation(client))
