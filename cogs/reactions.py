# Reactions cog

import random
import discord
import utils.checks as checks
from discord.ext import commands

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
                await ctx.send("<:vega:618947299267182602> {} || ".format(sender.mention)
                               + "According to my calculations, it's impossible to fuck the air.")

def setup(bot):
    bot.add_cog(Reactions(bot))