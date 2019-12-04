iimport discord
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

    @commands.command()
    async def github(self, ctx):
        """links to github repository"""
        await ctx.send("https://github.com/jsinitx4/content")

    @commands.command()
    async def userinfo(self, ctx, *, user:discord.Member):
        """returns user info"""
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
    async def channelinfo(self, ctx, *, channel:discord.TextChannel):
        """returns channel info"""
        name = channel.name 
        id = channel.id 
        description = channel.topic
        nsfw = channel.is_nsfw()
        created = channel.created_at 
        await ctx.send("`Channel Name:` " + f"{name}" + "\n`Channel ID:` " + f"{id}" + "\n`Channel Description:` " + f"{description}" + "\n`NSFW?` " + f"{nsfw}" + "\n`Channel Creation Date:` " + f"{created}")

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
    async def roleinfo(self, ctx, *, role:discord.Role):
        name = role.name
        id = role.id
        color = role.color
        mention = role.mentionable
        created = role.created_at
        await ctx.send("`Role Name:` " + f"{name}" + "\n`Role ID:` " + f"{id}" + "\n`Role Color:` " + f"{color}" + "\n`Mentionable?` " + f"{mention}" + "\n`Role Creation Date:` " + f"{created}")

    @commands.command()
    async def botinfo(self, ctx):
        guilds = str(len(self.bot.guilds))
        dev = "speed#3413"
        versionpy = discord.__version__
        await ctx.send("`Guild Size:` " + f"{guilds}" + " servers" + "\n`Developer:` " + dev + "\n`discord.py version:` " + versionpy)

    @commands.command()
    async def avatar(self, ctx, *, user:discord.User):
        """returns a users avatar"""
        avatar = user.avatar_url 
        await ctx.send(avatar)

    @commands.command()
    async def botinvite(self, ctx):
        """sends you a shady link"""
        await ctx.author.send("https://discordapp.com/oauth2/authorize?client_id=552616565754036239&permissions=8&scope=bot") # is this an ip logger?
        await ctx.send("check your dms thanks")

    @commands.command()
    async def serverinvite(self, ctx):
        """invite your bros :brofist:"""
        link = await ctx.channel.create_invite(max_age = 86400, max_uses = 0)
        await ctx.channel.trigger_typing()
        await ctx.send("invite your bros :brofist:")
        await ctx.send(link)

def setup(client):
    client.add_cog(Info(client))
