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
    def __init__(self, source, *, data, requester, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.requester = requester

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_search(cls, ctx, search:str, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(search, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)

        if earrape is True:
            return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options_earrape), data=data, requester=ctx.author)
        else:    
            return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data, requester=ctx.author)

class Queue():
    def __init__(self, client, voice_client, channel):
        self.bot = client
        self.queue = asyncio.Queue()
        self.voice_client = voice_client
        self.channel = channel
        self.next = asyncio.Event()
        self.queues = []
        self.current = None
        self.task = self.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        while True:
            self.next.clear()
            source = await self.queue.get()
            self.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            await self.channel.send(f'now playing: **{source.title}**\nrequested by: **{source.requester}**')
            await self.next.wait()
            source.cleanup()    

class Music(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.players = {}

    def get_player(self, ctx):
        player = self.players.get(ctx.guild.id)
        if player is None:
            player = Queue(self.bot, ctx.voice_client, ctx.channel)
            self.players[ctx.guild.id] = player
        return player

    async def clean(self, guild):
        try:
            del self.players[guild.id]
        except KeyError:
            pass

    @commands.command(aliases=['summon', 'connect'])
    async def join(self, ctx):
        """connects bot to vc"""
        await ctx.author.voice.channel.connect()
        await ctx.send("i'm in")
		
    @commands.command(aliases=['p'])
    async def play(self, ctx, *, search:str):
        """plays a song"""
        await ctx.channel.trigger_typing()
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        player = self.get_player(ctx)
        source = await YTDLSource.from_search(ctx, search, loop=self.bot.loop, stream=True)
        await player.queue.put(source)
        requester = ctx.author
        await ctx.send('queued: ' + "**" + f"{source.title}" + "**" + '\nrequested by: ' + "**" + f"{requester}" + "**")

    @commands.command()
    async def clear(self, ctx):
        """clears the queue"""
        if not ctx.voice_client or not ctx.voice_client.is_connected():
            return await ctx.send('nothing is playing')
        await self.clean(ctx.guild)
        await ctx.send("cleared the queue")

    @commands.command(aliases=['s'])
    async def skip(self, ctx):
        """skips playing song"""
        if not ctx.voice_client or not ctx.voice_client.is_connected():
            return await ctx.send('nothing is playing')
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
        if not ctx.voice_client or not ctx.voice_client.is_connected():
            return await ctx.send('nothing is playing')
        ctx.voice_client.source.volume = number
        await ctx.send("volume set to **{}**%".format(number))

    @commands.command()
    async def pause(self, ctx):
        """pauses the playing song"""
        if not ctx.voice_client or not ctx.voice_client.is_connected():
            return await ctx.send('nothing is playing')
        ctx.voice_client.pause()
        await ctx.send("done paused")

    @commands.command(aliases=['unpause'])
    async def resume(self, ctx):
        """resumes playing the paused song"""
        if not ctx.voice_client or not ctx.voice_client.is_connected():
            return await ctx.send('nothing is playing')
        ctx.voice_client.resume()
        await ctx.send("done resumed")

    @commands.command(aliases=['disconnect', 'stop'])
    async def leave(self, ctx):
        """disconnects bot from vc"""
        await ctx.voice_client.disconnect()
        await ctx.send("ok bye")

def setup(client):
    client.add_cog(Music(client))