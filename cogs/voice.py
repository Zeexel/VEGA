import discord
from discord.ext import commands
from discord.utils import get
from bot import bot as client
import os
import youtube_dl


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):  # TODO: Make this cleaner.
        global v
        v = get(client.voice_clients, guild=ctx.guild)

        if ctx.message.author.voice is None:
            await ctx.send(":x: You're not in a voice channel!")
        else:
            c = ctx.message.author.voice.channel

            if v and v.is_connected(): 
                await v.move_to(c)
            else: 
                v = await c.connect()
            print(f"Bot connected to {c} in server {ctx.guild.id}")

    @commands.command(aliases=['fuckoff', 'disconnect'])
    async def leave(self, ctx):     # TODO: Make this cleaner.
        v = get(client.voice_clients, guild=ctx.guild)

        if ctx.message.author.voice is None:
            await ctx.send(":x: You're not in a voice channel!")
        else:
            c = ctx.message.author.voice.channel
            if v and v.is_connected():
                await v.disconnect()
                print(f"Bot left {c} in server {ctx.guild.id}")
            else:
                await ctx.send(":x: I'm not in a voice channel!")

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, url):
        songThere = os.path.isfile(f'song-{ctx.guild.id}.mp3')

        try:
            if songThere:
                os.remove(f"./song-{ctx.guild.id}.mp3")
                print("Removed previous song file..")
        except PermissionError:
            print("Permission is denied to remove the previous song file.")
            return

        await ctx.send(f"Getting song from url ``{url}``")
        
        v = get(client.voice_clients, guild=ctx.guild)

        ydlOpts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }]
        }

        with youtube_dl.YoutubeDL(ydlOpts) as ydl:
            print(f"Downloading audio from {url}..")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith('.mp3'):
                n = file
                print(f"Renamed File: {n}")
                os.rename(file, f'song-{ctx.guild.id}.mp3')

        v.play(discord.FFmpegPCMAudio(f"song-{ctx.guild.id}.mp3"), after=lambda e: print(f"Song finished playing in server {ctx.guild.id}"))
        v.source = discord.PCMVolumeTransformer(v.source)
        v.source.value = 0.07   # NOTE: Do not go above this for the sake of your ears.

        nn = n.rsplit("-", 2)
        await ctx.send(f"Now playing {nn[0]}. Have fun!")
        print(f"Now playing {nn[0]} in server {ctx.guild.id}")

    @commands.command()
    async def pause(self, ctx):
        v = get(client.voice_clients, guild=ctx.guild)

        if v and v.is_playing():
            v.pause()
            await ctx.send(":white_check_mark: Music paused.")
        else:
            await ctx.send(":x: There's no music playing!")
        
    @commands.command()
    async def resume(self, ctx):
        v = get(client.voice_clients, guild=ctx.guild)

        if v and v.is_paused():
            await ctx.send(":white_check_mark: Resuming.")
            v.resume()
        else:
            await ctx.send(":x: The player isn't paused.")

    @commands.command()
    async def stop(self, ctx):
        v = get(client.voice_clients, guild=ctx.guild)

        if v and v.is_playing() or v and v.is_paused():
            v.stop()
            await ctx.send(":white_check_mark: Stopped the song.")
        else:
            await ctx.send(":x: There's no music playing!")

def setup(bot):
    bot.add_cog(Voice(bot))