import discord
import json
from discord.ext import commands

cfg = json.load(open('JSON/config.json', 'r'))

class NotNsfwChannel(commands.CommandError):
    pass


def is_nsfw_channel():

    def predicate(ctx):
        # If the channel is a DM, and it's marked as NSFW..
        if isinstance(ctx.channel, discord.DMChannel) or ctx.channel.is_nsfw():
            return True
        else:
            raise NotNsfwChannel
    return commands.check(predicate)


class NoDM(commands.CheckFailure):
    pass

def server_only():
    def predicate(ctx):
        if ctx.guild is None:
            raise NoDM('Using this command in DMs has been disabled.')
        return True
    return commands.check(predicate)


def is_owner():     # NOTE: This check is stupid and it was used with the original Gladward bot, it's fucking outdated
    devs = (108268232556703744)     # Zeexel#2951
    async def predicate(ctx):
        return ctx.message.author.id == devs
    return commands.check(predicate)