# Fun cog

import json
import random
import asyncio
import praw
import subprocess
import discord
from utils.functions import *
import utils.checks as checks
from datetime import datetime
from discord.ext import commands

cfg = json.load(open("JSON/config.json", "r"))    # Bot config

reddit = praw.Reddit(client_id=cfg['reddit_clientid'],
                     client_secret=cfg['reddit_clientsecret'],
                     user_agent='Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0')


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['8ball', '8-ball'])
    async def eightball(self, ctx, q):
        sender = ctx.message.author
        await ctx.send(f":8ball: {sender.mention} || {getTranslation(ctx.message.guild.id, 'eightballRes', str(random.randint(1, 14)))}")

    @eightball.error
    async def eightball_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'q':
                await ctx.send(f":warning: {sender.mention} || {getTranslation(ctx.message.guild.id, 'errmsg', 'cmdInvalidParam')}\n``Correct Usage: >>8ball [question]``")

    @commands.command(aliases=['coinflip'])
    async def flipacoin(self, ctx):
        sender = ctx.message.author

        await ctx.send("{} || Flipping..".format(sender.mention))
        async with ctx.typing():
            await asyncio.sleep(1.3)
        await ctx.send(f"{sender.mention}, {getTranslation(ctx.message.guild.id, 'headsTails', str(random.randint(1, 6)))}")

    @commands.command()
    async def lovecalc(self, ctx, user1: discord.Member, user2: discord.Member):
        sender = ctx.message.author

        if user1 is not user2:
            await ctx.send(f"{getTranslation(sender.guild.id, 'generalRes', 'loveCalculating')}")
            async with ctx.typing():
                await asyncio.sleep(1.5)
            await ctx.send(f":white_check_mark: {sender.mention} || {getTranslation(sender.guild.id, 'generalRes', 'loveCalcFinal')} {str(random.randint(0, 115))}%")
        else:
            await ctx.send(f":warning: {sender.mention} || I do recommend loving yourself, but I don't think that's fit for this situation..")

    @lovecalc.error
    async def lovecalc_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'user1' or 'user2':
                await ctx.send(f":warning: {sender.mention}, {getTranslation(ctx.message.guild.id, 'errmsg', 'cmdInvalidParam')}" +
                "\n ``>>lovecalc [user1] [user2]")

    @commands.command()
    async def meme(self, ctx):

        subs = ['me_irl', 'dankmemes']
        sender = ctx.message.author

        # Pick a post in the "hot" category from a random sub
        meme_submissions = reddit.subreddit(random.choice(subs)).hot()
        post_to_pick = random.randint(1, 20)

        for i in range(0, post_to_pick):
            # Pick a post that isn't stickied
            submission = next(x for x in meme_submissions if not x.stickied)

        # Create an embed
        embed = discord.Embed(title="Here's a meme for you, {sndr}."
                              .format(sndr=sender.display_name),
                              color=0x98f019,
                              url=submission.shortlink)

        embed.set_image(url=submission.url)
        embed.set_footer(text=getTranslation(ctx.message.guild.id, 'generalRes', 'reddFooter'))
        await ctx.send(embed=embed)  # Send the embed

    @commands.command()
    async def animeme(self, ctx):

        sender = ctx.message.author

        # Pick a post in the "hot" category from a random sub
        meme_submissions = reddit.subreddit('animemes').hot()
        post_to_pick = random.randint(1, 20)

        for i in range(0, post_to_pick):
            # Pick a post that isn't stickied
            submission = next(x for x in meme_submissions if not x.stickied)

        # Create an embed
        embed = discord.Embed(title="Here's a meme for you, {sndr}."
                              .format(sndr=sender.display_name),
                              color=0x98f019,
                              url=submission.shortlink)

        embed.set_image(url=submission.url)
        embed.set_footer(text=getTranslation(ctx.message.guild.id, 'generalRes', 'reddFooter'))
        await ctx.send(embed=embed)  # Send the embed

    @commands.command()
    async def hug(self, ctx, user: discord.Member):
        sender = ctx.message.author
        hug_files = [
            discord.File('res/images/reactions/hug/hug1.gif'),
            discord.File('res/images/reactions/hug/hug2.gif'),
            discord.File('res/images/reactions/hug/hug3.gif'),
            discord.File('res/images/reactions/hug/hug4.gif'),
            discord.File('res/images/reactions/hug/hug5.gif'),
            discord.File('res/images/reactions/hug/hug6.gif')
        ]

        if user is not sender:
            await ctx.send("{sndr} gave {usr} a hug!".format(sndr=sender.mention, usr=user.mention),
                           file=random.choice(hug_files))
        else:
            await ctx.send("<:vega:618947299267182602> {} || I don't believe that's possible..".format(sender.mention))

    @hug.error
    async def hug_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name is 'user':
                await ctx.send("<:vega:618947299267182602> {} || ".format(sender.mention)
                               + "According to my calculations, it's impossible to hug the air.")


    @commands.command()
    async def kiss(self, ctx, user: discord.Member):
        sender = ctx.message.author
        kiss_files = [
            discord.File('res/images/reactions/kiss/kiss1.gif'),
            discord.File('res/images/reactions/kiss/kiss2.gif'),
            discord.File('res/images/reactions/kiss/kiss3.gif'),
            discord.File('res/images/reactions/kiss/kiss4.gif'),
            discord.File('res/images/reactions/kiss/kiss5.gif'),
            discord.File('res/images/reactions/kiss/kiss6.gif')
        ]


        if user is not sender:
            await ctx.send("{sndr} kissed {usr}!".format(sndr=sender.mention, usr=user.mention),
                            file=random.choice(kiss_files))
        else:
            await ctx.send("{} || {}"
                            .format(sender.mention,
                                    random.choice(['Would a mirror help?', "I don't think that's possible.."])))

    @kiss.error
    async def kiss_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name is 'user':
                await ctx.send("<:vega:618947299267182602> {} || ".format(sender.mention)
                               + "According to my calculations, it's impossible to kiss the air.")

    @checks.is_nsfw_channel()
    @commands.command()
    async def fuck(self, ctx, user: discord.Member):
        sender = ctx.message.author

        fuck_files = [
            discord.File('res/images/reactions/fuck/fuck1.gif'),
            discord.File('res/images/reactions/fuck/fuck2.gif'),
            discord.File('res/images/reactions/fuck/fuck3.gif'),
            discord.File('res/images/reactions/fuck/fuck4.gif'),
            discord.File('res/images/reactions/fuck/fuck5.gif')
        ]

        if user is not sender:
            await ctx.send("{sndr} fucked {usr}!"
                            .format(sndr=sender.mention, usr=user.mention),
                            file=random.choice(fuck_files))
        else:
            await ctx.send("{} || I think it's impossible to fuck yourself..".format(sender.mention))
    
    @fuck.error
    async def fuck_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name is 'user':
                await ctx.send(":x: {} || ".format(sender.mention)
                               + "According to my calculations, it's impossible to fuck the air.")

def setup(bot):
    bot.add_cog(Fun(bot))
