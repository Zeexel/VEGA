import json
err_msgs = json.load(open("JSON/error_responses.json", "r"))

import random
import asyncio
import discord
from discord.ext import commands


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['purge', 'cleanmsgs'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amnt=10, maxmsg=500):
        sender = ctx.message.author
        if amnt > maxmsg:
            await ctx.send("<:vega:618947299267182602> {} || ".format(sender.mention) + random.choice(err_msgs)
                           + "\n``Max messages you can clear is 500!``")
        else:
            await ctx.channel.purge(limit=amnt)
            await asyncio.sleep(0.5)
            await ctx.send("<:vega:618947299267182602> {sndr} || Successfully cleared ``{amount}`` messages!"
                           .format(sndr=sender.mention, amount=amnt))

    @clear.error
    async def clear_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("<:vega:618947299267182602> {} || ".format(sender.mention) + random.choice(err_msgs)
                           + """\n``Missing permission "Manage messages"``""")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        sender = ctx.message.author
        await user.kick(reason=reason)

        if reason is not None:
            await ctx.send("{sndr} || Kicked user ``{name}#{dis}`` for ``{res}``."
                            .format(sndr=sender.mention, name=user.name, dis=user.discriminator, res=reason))
        else:
            await ctx.send("{sndr} || Kicked user ``{name}#{dis}``"
                           .format(sndr=sender.mention, name=user.name, dis=user.discriminator))

    @kick.error
    async def kick_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("{} || ".format(sender.mention) + random.choice(err_msgs)
                           + """\n``Missing permission "Kick Members"``""")

        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == "user":
                await ctx.send("{} || ".format(sender.mention) + random.choice(err_msgs)
                               + """\n``Missing required argument "User"``""")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None, messages_to_del=0):
        sender = ctx.message.author
        await user.ban(reason=reason, delete_message_days=int(messages_to_del))

        if reason is not None:
            await ctx.send("{sndr} || Banned user ``{name}#{dis}`` for ``{res}``"
                            .format(sndr=sender.mention, name=user.name, dis=user.discriminator, res=reason))
        else:
            await ctx.send("{sndr} || Banned user ``{name}#{dis}``"
                           .format(sndr=sender.mention, name=user.name, dis=user.discriminator))

    @ban.error
    async def ban_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("{} || ".format(sender.mention) + random.choice(err_msgs)
                           + """\n``Missing permission "Ban Members"``""")

        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == "user":
                await ctx.send("{} || ".format(sender.mention) + random.choice(err_msgs)
                               + """\n``Missing required argument "User"``""")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def softban(self, ctx, user: discord.Member, messages_to_del=7):
        sender = ctx.message.author
        await user.ban(reason='SOFTBANNED', delete_message_days=int(messages_to_del))
        await user.unban(reason=None)

        await ctx.send("{sndr} || Softbanned ``{name}#{discrim}``"
                       .format(sndr=sender.mention, name=user.name, discrim=user.discriminator))

    @softban.error
    async def softban_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("{} || ".format(sender.mention) + random.choice(err_msgs)
                           + """\n``Missing permission "Kick Members"``""")

        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == "user":
                await ctx.send("{} || ".format(sender.mention) + random.choice(err_msgs)
                               + """\n``Missing required argument "User"``""")


def setup(bot):
    bot.add_cog(AdminCommands(bot))
