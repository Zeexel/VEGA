
import traceback
import sys
import json
from discord.ext import commands

cfg = json.load(open('JSON/config.json', 'r'))


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        sender = ctx.message.author
        admin = ctx.bot.get_user(108268232556703744)

        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.UserInputError)     # Ignored error types

        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.CommandNotFound):
            return await ctx.send(f"Command Not Found, {sender.mention}")

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f"I apologize, {sender.mention}, but that command has been disabled.")

        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.send(f"That command doesn't work in Direct Messages, {sender.mention}.")
        else:
            pass

        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

        if admin is not None:
            await admin.send(f"{admin.mention} || An error occured while running the command {ctx.command}." + 
            "```Ignoring exception in command {}:\n{}```"
            .format(ctx.command, traceback.format_exception(type(error), error, error.__traceback__)))

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
    