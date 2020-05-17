# This is all some simple error handling
# It's really just made to prevent the output on the host console to be spammed with errors such as missing commands,
# disabled commands, and commands that are disabled in DM chats.

import traceback
import sys
from utils.functions import getTranslation
import discord
from discord.ext import commands


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        sender = ctx.message.author

        if hasattr(ctx.command, 'on_error'):
            return

        ignored = commands.UserInputError
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.CommandNotFound):
            return await ctx.send(f":x: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdNotFound')}")

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f":x: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdDisabled')}")

        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.send(f":x: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdDMDisabled')}")

        elif isinstance(error, discord.errors.Forbidden):
            pass
        else:
            pass

        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
