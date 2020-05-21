# Fun cog

import json
import random
import asyncio
import praw
import subprocess
import discord
from PIL import Image, ImageDraw, ImageFont
from utils.functions import *
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

    @commands.command(aliases=['flman'])
    async def floridaman(self, ctx, *, title=None):
        sender = ctx.message.author
        img = Image.open('res/images/imagegeneration/flman/floridaman_template.png')
        parts = json.load(open("JSON/parts.json"))

        person_images = [
            'res/images/imagegeneration/flman/deathgrips.jpg',
            'res/images/imagegeneration/flman/neckbeard.jpg',
            'res/images/imagegeneration/flman/niggaskissing.jpg',
            'res/images/imagegeneration/flman/thickneck.jpg'
        ]

        title = title

        if title is None:
            str1 = "{MW} {pt1} {pt2} {pt3}".format(MW=random.choice(["Florida Man", "Florida Woman", "Florida Couple"]),
                                                   pt1=random.choice(parts['part1']),
                                                   pt2=random.choice(parts['part2']),
                                                   pt3=random.choice(parts['part3']))   # Generate a title based off the JSON file provided
            author = "By " + random.choice(parts['authors'])    # Random author name
        else:
            str1 = title    # Custom Title
            author = "By " + random.choice(parts['authors'])    # Random author name

        person = Image.open(random.choice(person_images))
        today = datetime.today()
        now = datetime.now()

        img.paste(person, (50, 225))

        font1 = ImageFont.truetype("georgia.ttf", 32)
        font2 = ImageFont.truetype("arial.ttf", 16)

        draw = ImageDraw.Draw(img)
        draw.text((20, 80), str1, font=font1, fill="black")
        draw.text((95, 165), author, font=font2, fill="black")
        draw.text((250, 165), today.strftime("%b %d, %Y").upper(), font=font2, fill="gray")
        draw.text((360, 165), now.strftime("%I:%M %p"), font=font2, fill="gray")

        print(str1)
        img.save('res/images/imagegeneration/flman/floridaman.png')
        await ctx.send(file=discord.File('res/images/imagegeneration/flman/floridaman.png'))

    @commands.command(aliases=['scatman', 'scatland', 'scatworld'])
    async def scatmansworld(self, ctx, img_url, *, line=None):
        sender = ctx.message.author

         # Add the title and caption to the image

        img = Image.open('res/images/imagegeneration/scatmansworld/scatmans_world_base.jpg')
        save_dir = 'res/images/imagegeneration/scatmansworld/scatmansworld.png'
        W, H = (480, 360)   # Image width & height
        draw = ImageDraw.Draw(img)
        font1 = ImageFont.truetype("georgia.ttf", 25)
        font2 = ImageFont.truetype("arial.ttf", 15)
        line2 = None

        if line is None:
            await ctx.send(f":warning: {sender.mention}, {getTranslation(ctx.message.guild.id, 'errmsg', 'cmdInvalidParam')}" +
            "\n``>>scatman [url] [title]")
            return
        
        if '|' in line:
            split = line.split('|')
            line1 = split[0]
            line2 = split[1]
        else:
            split = line.split('|')
            line1 = split[0]

            if len(split) > 2:
                line1 = ' '.join(split[:2])
                line2 = ' '.join(split[:1])
            else:
                line1 = split[0]
                if len(split) > 1:
                    line2 = ' '.join(split[1:])

        if line2 is None:
            line2 = ''

        print("SCATMAN - Adding text..")

        title = line1
        caption = line2
        w, h = draw.textsize(title, font=font1)     # Width & Height of the title based off the string size
        w2, h2 = draw.textsize(caption, font=font2)     # Width & Height of the caption based off the string size

        draw.text(((W-w)/2, 260), title, font=font1, fill="white")
        draw.text(((W-w2)/2, 290), caption, font=font2, fill="white")

        print("SCATMAN - String provided: " + title + caption)
        print("SCATMAN - Caption & Text added!")

        dl_img(img_url, 'res/images/imagegeneration/scatmansworld/fullsize.jpg')
        print("SCATMAN - Image downloaded from\n" + img_url)

        # Resize the image provided and paste it onto the template

        fullsize_img_dir = "res/images/imagegeneration/scatmansworld/fullsize.jpg"
        fullsize_img = Image.open(fullsize_img_dir)
        fullsize_img = fullsize_img.resize((295, 185), Image.ANTIALIAS) # Resize the image w/ anti-aliasing

        print("SCATMAN - Adding provided image & resizing it..")

        img.paste(fullsize_img, (92, 65))

        img.save(save_dir)  # Save it to a PNG file
        print("SCATMAN - Image saved at \n " + save_dir)
        print("SCATMAN - Sending Image")
        await ctx.send(file=discord.File('res/images/imagegeneration/scatmansworld/scatmansworld.png'))

    @scatmansworld.error
    async def scatmansworld_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'img_url':
                await ctx.send(f":warning: {sender.mention}, {getTranslation(ctx.message.guild.id, 'errmsg', 'cmdInvalidParam')}" +
                "\n``>>scatman [url] [title]")

    @commands.command(aliases=['jpeg', 'jpg', 'android'])
    async def deepfry(self, ctx, url, quality=1):
        print("DEEPFRY - Downloading image from " + url)
        dl_img(url, 'res/images/imagegeneration/deepfry/notdeepfried.jpg')

        img = Image.open('res/images/imagegeneration/deepfry/notdeepfried.jpg')
        img.save('res/images/imagegeneration/deepfry/deepfried_img.jpg', quality=quality)
        await ctx.send(file=discord.File('res/images/imagegeneration/deepfry/deepfried_img.jpg'))

    @commands.command()
    async def absolutelydisgusting(self, ctx, url):
        save_dir = 'res/images/imagegeneration/absolutelydisgusting/absolutelydisgusting.png'

        dl_img(url, 'res/images/imagegeneration/absolutelydisgusting/fullsize.jpg')

        img = Image.open('res/images/imagegeneration/absolutelydisgusting/AD_template.jpg')
        fullsize = Image.open('res/images/imagegeneration/absolutelydisgusting/fullsize.jpg')
        fullsize = fullsize.resize((273, 164), Image.ANTIALIAS)

        img.paste(fullsize, (0, 0))
        img.save(save_dir)

        await ctx.send(file=discord.File(save_dir))

    @absolutelydisgusting.error
    async def absolutelydisgusting_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name is 'url':
                await ctx.send(f":warning: {sender.mention}, {getTranslation(ctx.message.guild.id, 'errmsg', 'cmdInvalidParam')}" +
                "\n``>>absolutelydisgusting [url]")
    
    @commands.command()
    async def superhotchicks(self, ctx, url):
        save_dir = 'res/images/imagegeneration/superhotchicks/hotchicks.png'
        template_dir = 'res/images/imagegeneration/superhotchicks/hotchicks_template.jpg'

        dl_img(url, 'res/images/imagegeneration/superhotchicks/fullsize.jpg')

        img = Image.open(template_dir)
        fullsize = Image.open('res/images/imagegeneration/superhotchicks/fullsize.jpg')
        fullsize = fullsize.resize((74, 107), Image.ANTIALIAS)

        img.paste(fullsize, (6, 3))
        img.save(save_dir)
        await ctx.send(file=discord.File(save_dir))

    @superhotchicks.error
    async def superhotchicks_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'url':
                await ctx.send(f":warning: {sender.mention}, {getTranslation(ctx.message.guild.id, 'errmsg', 'cmdInvalidParam')}" +
                "\n``>>absolutelydisgusting [url]")

def setup(bot):
    bot.add_cog(Fun(bot))
