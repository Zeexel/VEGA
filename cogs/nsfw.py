import requests
import json
import utils.checks as checks
from random import randint
import discord
from discord.ext import commands

class Nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.is_nsfw_channel()
    @commands.command(aliases=['r34'])
    async def rule34(self, ctx, *, tags):
        limit = 500
        url = "http://rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&"

        try: d = requests.get(f"{url}limit={limit}&tags={tags}").json()
        except json.JSONDecodeError:
            await ctx.send(":x: Wasn't able to find anything with that, this text must be localized.")
            return
        
        count = len(d)
        
        if count == 0:
            await ctx.send(":x: Wasn't able to find anything with that, this text must be localized.")
            return
        
        i = d[randint(0, count)]

        img_url = f"http://img.rule34.xxx/images/{i['directory']}/{i['image']}"

        embed = discord.Embed(title="Here's what I found on Rule34!", color=0xaae5a3, url=img_url)
        embed.set_image(url=img_url)
        embed.set_footer(text=i['tags'])

        await ctx.send(embed=embed)

    
    @checks.is_nsfw_channel()
    @commands.command(aliases=['gel'])
    async def gelbooru(self, ctx, *, tags):
        limit = 500
        url = "https://gelbooru.com/index.php?page=dapi&s=post&json=1&q=index&"

        try: d = requests.get(f"{url}limit={limit}&tags={tags}").json()
        except json.JSONDecodeError:
            await ctx.send(":x: Wasn't able to find anything with that, this text must be localized.")
            return
        
        count = len(d)
        
        if count == 0:
            await ctx.send(":x: Wasn't able to find anything with that, this text must be localized.")
            return
        
        i = d[randint(0, count)]

        embed = discord.Embed(title="Here's what I found on Gelbooru!", color=0x0064e3, url=i['file_url'])
        embed.set_image(url=i['file_url'])
        embed.set_footer(text=i['tags'])

        await ctx.send(embed=embed)


    @checks.is_nsfw_channel()
    @commands.command()
    async def e621(self, ctx, *, tags):
        limit = 500
        headers = {"User-Agent": "VEGA-HAKASE/REWRITE (by Zeexel)"}
        url = f"https://e621.net/posts.json?limit={limit}&"

        try: d = requests.get(f"{url}tags={tags}", headers=headers).json()
        except json.JSONDecodeError:
            await ctx.send(":x: Wasn't able to find anything with that, this text must be localized.")
            return
        
        count = len(d)
        
        if count == 0:
            await ctx.send(":x: Wasn't able to find anything with that, this text must be localized.")
            return
        
        i = d['posts'][randint(0, count)]

        embed = discord.Embed(title="Here's what I found on E621!", color=0x0064e3, url=i['file']['url'])
        embed.set_image(url=i['file']['url'])

        await ctx.send(embed=embed)

    @checks.is_nsfw_channel()
    @commands.command(aliases=['x'])
    async def xbooru(self, ctx, *, tags):
        limit = 500
        url = "http://xbooru.com/index.php?page=dapi&s=post&q=index&json=1&"

        try: d = requests.get(f"{url}limit={limit}&tags={tags}").json()
        except json.JSONDecodeError:
            await ctx.send(":x: Wasn't able to find anything with that, this text must be localized.")
            return
        
        count = len(d)
        
        if count == 0:
            await ctx.send(":x: Wasn't able to find anything with that, this text must be localized.")
            return
        
        i = d[randint(0, count)]

        img_url = f"http://img.xbooru.com/images/{i['directory']}/{i['image']}"

        embed = discord.Embed(title="Here's what I found on Xbooru!", color=0xffe18f, url=img_url)
        embed.set_image(url=img_url)
        embed.set_footer(text=i['tags'])

        await ctx.send(embed=embed)


    @checks.is_nsfw_channel()
    @commands.command(aliases=['real'])
    async def realbooru(self, ctx, *, tags):
        limit = 500
        url = "http://realbooru.com/index.php?page=dapi&s=post&q=index&json=1&"

        try: d = requests.get(f"{url}limit={limit}&tags={tags}").json()
        except json.JSONDecodeError:
            await ctx.send(":x: Wasn't able to find anything with that, this text must be localized.")
            return
        
        count = len(d)
        
        if count == 0:
            await ctx.send(":x: Wasn't able to find anything with that, this text must be localized.")
            return
        
        i = d[randint(0, count)]

        img_url = f"http://realbooru.com/images/{i['directory']}/{i['image']}"

        embed = discord.Embed(title="Here's what I found on RealBooru!", url=img_url)
        embed.set_image(url=img_url)
        embed.set_footer(text=i['tags'])

        await ctx.send(embed=embed)
        





def setup(bot):
    bot.add_cog(Nsfw(bot))