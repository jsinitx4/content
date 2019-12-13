import asyncio
import discord 
import youtube_dl

from discord.ext import commands

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'before_options': "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    'options': '-vn'
}

ffmpeg_options_earrape = {
    'before_options': "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    'options': '-vn -filter:a "volume=100dB"'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

earrape = False

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_search(cls, search:str, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(search, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        if earrape is True:
            return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options_earrape), data=data)
        else:    
            return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command(aliases=['summon', 'connect'])
    async def join(self, ctx):
        """connects bot to vc"""
        await ctx.author.voice.channel.connect()
        await ctx.send("i'm in")
		
    @commands.command(aliases=['p'])
    async def play(self, ctx, *, search):
        """plays a song"""
        await ctx.channel.trigger_typing()
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        source = await YTDLSource.from_search(search, stream=True)
        ctx.voice_client.play(source, after=lambda e: print('%s' % e) if e else None)
        requester = ctx.author
        await ctx.send('playing: ' + "**" + f"{source.title}" + "**" + '\nrequested by: ' + "**" + f"{requester}" + "**")

    @commands.command(aliases=['s'])
    async def skip(self, ctx):
        """skips playing song"""
        ctx.voice_client.stop()
        await ctx.send('**' + f"{ctx.author}" + '**' + ' skipped the song')

    @commands.command()
    async def earrape(self, ctx):
        """increases db of a song to 100"""
        global earrape
        if earrape is False:
            earrape = True
            return await ctx.send("enabled earrape for the next song")
        if earrape is True:
            earrape = False
            return await ctx.send("disabled earrape for the next song") 

    @commands.command(aliases=['vol', 'v'])
    async def volume(self, ctx, number:float):
        """changes the song volume"""
        ctx.voice_client.source.volume = number
        await ctx.send("volume set to **{}**%".format(number))

    @commands.command()
    async def pause(self, ctx):
        """pauses the playing song"""
        ctx.voice_client.pause()
        await ctx.send("done paused")

    @commands.command()
    async def resume(self, ctx):
        """resumes playing the paused song"""
        ctx.voice_client.resume()
        await ctx.send("done resumed")

    @commands.command(aliases=['disconnect', 'stop'])
    async def leave(self, ctx):
        """disconnects bot from vc"""
        await ctx.voice_client.disconnect()
        await ctx.send("ok bye")

def setup(client):
    client.add_cog(Music(client))
