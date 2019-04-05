import discord
import time 
from discord.ext import commands 

class Info(commands.Cog):
    def __init__(self, client):
        self.bot = client 

    @commands.command(aliases=['dev', 'creator'])
    async def developer(self, ctx):
        """who"""
        await ctx.send("speed#3413")

    @commands.command(aliases=['latency'])
    async def ping(self, ctx):
        """bot latency"""
        time1 = time.perf_counter()
        await ctx.channel.trigger_typing()
        time2 = time.perf_counter()
        await ctx.send("latency: `{}`ms".format(round((time2-time1)*1000)))

    @commands.command(aliases=['git'])
    async def github(self, ctx):
        """links to github repository"""
        await ctx.send("https://github.com/jsinitx4/content")

    @commands.command(aliases=['user'])
    async def userinfo(self, ctx, *, user:discord.Member):
        """returns user stats"""
        name = user.name 
        discrim = user.discriminator
        userid = user.id
        avatar = user.avatar_url
        activity = None
        if user.activity:
            activity = user.activity.name
        bot = user.bot
        created = user.created_at
        joined = user.joined_at
        nick = user.nick
        await ctx.send("`User Name:` " + f"{name}" + "\n`User Discriminator:` " + f"{discrim}" + "\n`User ID:` " + f"{userid}""\n`User Avatar:` " + "`" f"{avatar}" + "`" + "\n`User Activity:` " + f"{activity}" + "\n`Bot?` " + f"{bot}" + "\n`User Account Creation Date:` " + f"{created}" + "\n`User Guild Join Date:` " + f"{joined}" + "\n`User Nickname:` " + f"{nick}")

    @commands.command()
    async def serverinfo(self, ctx):
        """returns server stats"""
        guild = ctx.guild
        name = guild.name
        owner = guild.owner
        region = guild.region
        icon = guild.icon_url
        member = guild.member_count
        created = guild.created_at
        await ctx.send("`Guild Name:` " + f"{name}" + "\n`Guild Owner:` " + f"{owner}" + "\n`Guild Region:` " + f"{region}" + "\n`Guild Icon:` " + "`" f"{icon}" + "`" + "\n`Member Count:` " + f"{member}" + " members" + "\n`Guild Creation:` " + f"{created}")

    @commands.command()
    async def avatar(self, ctx, *, user:discord.Member):
        """returns user avatar"""
        avatar = user.avatar_url 
        await ctx.send(avatar)

    @commands.command()
    async def info(self, ctx):
        """commands but on a website"""
        await ctx.send("https://speed-is-a.living-me.me/s/j936") # is this an ip logger?

def setup(client):
    client.add_cog(Info(client))
