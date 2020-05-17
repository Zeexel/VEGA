# NSFW Cog

import requests
import random
import json
import praw
import utils.checks as checks
from utils.functions import getTranslation
import discord
from discord.ext import commands

cfg = json.load(open("JSON/config.json"))
reddit = praw.Reddit(client_id=cfg['reddit_clientid'],
                     client_secret=cfg['reddit_clientsecret'],
                     user_agent='Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0')


class Nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.is_nsfw_channel()
    @commands.command(aliases=['r34'])
    async def rule34(self, ctx, *, tags: str):
        sender = ctx.message.author     # Command Sender
        limit = 500      # Post selection limit
        header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0"}     # User Agent
        r34_url = "http://rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&"    # r34.xxx URL

        try:
            data = requests.get(r34_url + f"limit={limit}&tags={tags}", headers=header).json()

        except json.JSONDecodeError:
            await ctx.send(f"{getTranslation(sender.guild.id, 'errmsg', 'nsfwNoRes')} ``{tags}``")
            print("JSON Decode error - Tags were {}".format(tags))
            return

        count = len(data)

        if count == 0:
            await ctx.send(f"{getTranslation(sender.guild.id, 'errmsg', 'nsfwNoRes')} ``{tags}``")
            print("Count was 0 - tags were {}".format(tags))
            return

        image_count = 1

        if count < 1:
            image_count = count

        images = []
        image = data[random.randint(0, count)]      # Randomly choose an image from the site

        # Create embed
        embed = discord.Embed(title=f"Here's what I found on Rule34, {sender.display_name}", color=0xaae5a3,
                              url="http://img.rule34.xxx/images/{dir}/{img}"    # Set title link to the image URL
                              .format(dir=image["directory"], img=image["image"]))

        embed.set_image(url="http://img.rule34.xxx/images/{dir}/{img}"
                        .format(dir=image["directory"], img=image["image"]))

        embed.set_footer(text=image["tags"])    # Set footer with the tags of the image

        await ctx.send(embed=embed)     # Send out the embed

    @rule34.error
    async def r34_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f":warning: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdInvalidParam')}\n``>>rule34 [tag(s)]``")
        if isinstance(error, checks.NotNsfwChannel):
            await ctx.send(f":warning: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdNSFWErr')}")       

    @checks.is_nsfw_channel()
    @commands.command(aliases=['gel', 'gbooru', 'gb'])
    async def gelbooru(self, ctx, *, tags: str):
        sender = ctx.message.author  # Command Sender
        limit = 500  # Post selection limit
        header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0"}  # User Agent
        gel_url = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&"  # gelbooru URL

        try:
            data = requests.get(gel_url + "limit={limit}&tags={tags}".format(limit=limit, tags=tags),
                                headers=header).json()

        except json.JSONDecodeError:
            await ctx.send(f"{getTranslation(sender.guild.id, 'errmsg', 'nsfwNoRes')} ``{tags}``")
            print("JSON Decode error - Tags were {}".format(tags))
            return

        count = len(data)
        if count == 0:
              await ctx.send(f"{getTranslation(sender.guild.id, 'errmsg', 'nsfwNoRes')} ``{tags}``")
              print("Count was 0 - tags were {}".format(tags))
              return

        image_count = 1

        if count < 1:
            image_count = count

        images = []
        image = data[random.randint(0, count)]

        # Create embed
        embed = discord.Embed(title=f"Here's what I found on Gelbooru, {sender.display_name}", color=0x0064e3, url=image['file_url'])

        # embed.set_image(url=data[random.randint(0, count)]["file_url"])
        embed.set_image(url=image['file_url'])
        embed.set_footer(text=image['tags'])

        await ctx.send(embed=embed)  # Send out the embed

    @gelbooru.error
    async def gel_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f":warning: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdInvalidParam')}\n``>>gelbooru [tag(s)]``")
        if isinstance(error, checks.NotNsfwChannel):
            await ctx.send(f":warning: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdNSFWErr')}")       


    @checks.is_nsfw_channel()
    @commands.command(aliases=['x', 'xb'])
    async def xbooru(self, ctx, *, tags: str):
        sender = ctx.message.author     # Command Sender
        limit = 500      # Post selection limit
        header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0"}     # User Agent
        xb_url = "https://xbooru.com/index.php?page=dapi&s=post&q=index&json=1&"    # r34.xxx URL

        try:
            data = requests.get(xb_url + "limit={limit}&tags={tags}".format(limit=limit, tags=tags),
                                headers=header).json()

        except json.JSONDecodeError:
            await ctx.send(f"{getTranslation(sender.guild.id, 'errmsg', 'nsfwNoRes')} ``{tags}``")
            print("JSON Decode error - Tags were {}".format(tags))
            return

        count = len(data)

        if count == 0:
            await ctx.send(f"{getTranslation(sender.guild.id, 'errmsg', 'nsfwNoRes')} ``{tags}``")
            print("Count was 0 - tags were {}".format(tags))
            return

        image_count = 1

        if count < 1:
            image_count = count

        images = []
        post = data[random.randint(0, count)]      # Randomly choose an image from the site

        # Create embed
        embed = discord.Embed(title=f"Here's what I found on Gelbooru, {sender.display_name}",
                              color=0xf3efc0,
                              url="http://img3.xbooru.com/images/{dir}/{img}"    # Set title link to the image URL
                              .format(dir=post["directory"], img=post["image"]))
                              

        embed.set_image(url="http://img3.xbooru.com/images/{dir}/{img}"
                        .format(dir=post["directory"], img=post["image"]))

        embed.set_footer(text=post["tags"])    # Set footer with the tags of the image

        await ctx.send(embed=embed)     # Send out the embed

    @xbooru.error
    async def x_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f":warning: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdInvalidParam')}\n``>>xbooru [tag(s)]``")
        if isinstance(error, checks.NotNsfwChannel):
            await ctx.send(f":warning: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdNSFWErr')}")    

    @checks.is_nsfw_channel()
    @commands.command(aliases=['boobs', 'boobies', 'titties'])
    async def tits(self, ctx):
        sender = ctx.message.author

        # Pick a post in the "hot" category from a random sub
        submissions = reddit.subreddit('boobs').hot()
        post_to_pick = random.randint(1, 20)

        for i in range(0, post_to_pick):
            # Pick a post that isn't stickied
            submission = next(x for x in submissions if not x.stickied)

        # Create an embed
        embed = discord.Embed(title="Here's what I found, {sndr}."
                              .format(sndr=sender.display_name),
                              color=0xb50a16,
                              url=submission.shortlink)

        embed.set_image(url=submission.url)
        embed.set_footer(text=getTranslation(ctx.message.guild.id, 'generalRes', 'reddFooter'))
        await ctx.send(embed=embed)  # Send the embed

    @tits.error
    async def boob_squish(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, checks.NotNsfwChannel):
            await ctx.send(f":warning: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdNSFWErr')}")    

    @checks.is_nsfw_channel()
    @commands.command(aliases=['pawg'])
    async def ass(self, ctx):
        sender = ctx.message.author

        # Pick a post in the "hot" category from a random sub
        subs = ['ass', 'pawg']
        submissions = reddit.subreddit(random.choice(subs)).hot()
        post_to_pick = random.randint(1, 20)

        for i in range(0, post_to_pick):
            # Pick a post that isn't stickied
            submission = next(x for x in submissions if not x.stickied)

        # Create an embed
        embed = discord.Embed(title="Here's what I found, {sndr}."
                              .format(sndr=sender.display_name),
                              color=0xb50a16,
                              url=submission.shortlink)

        embed.set_image(url=submission.url)
        embed.set_footer(text=getTranslation(ctx.message.guild.id, 'generalRes', 'reddFooter'))
        await ctx.send(embed=embed)  # Send the embed

    @ass.error
    async def ass_pound(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, checks.NotNsfwChannel):
            await ctx.send(f":warning: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdNSFWErr')}")  

    @checks.is_nsfw_channel()
    @commands.command(aliases=['traps', 'femboy', 'trap'])
    async def femboys(self, ctx):
        sender = ctx.message.author

        # Pick a post in the "hot" category from a random sub
        subs = ['femboys', 'traps']
        submissions = reddit.subreddit(random.choice(subs)).hot()
        post_to_pick = random.randint(1, 20)

        for i in range(0, post_to_pick):
            # Pick a post that isn't stickied
            submission = next(x for x in submissions if not x.stickied)

        # Create an embed
        embed = discord.Embed(title="Here's what I found, {sndr}."
                              .format(sndr=sender.display_name),
                              color=0xb50a16,
                              url=submission.shortlink)

        embed.set_image(url=submission.url)
        embed.set_footer(text=getTranslation(ctx.message.guild.id, 'generalRes', 'reddFooter'))
        await ctx.send(embed=embed)  # Send the embed

    @femboys.error
    async def racist_femboy(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, checks.NotNsfwChannel):
            await ctx.send(f":warning: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdNSFWErr')}")  


def setup(bot):
    bot.add_cog(Nsfw(bot))
