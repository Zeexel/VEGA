import json
import random
import asyncio
import discord
import sqlite3
from utils.functions import getTranslation
from discord.ext import commands


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['purge', 'cleanmsgs'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amnt=10, maxmsg=500):
        sender = ctx.message.author
        if amnt > maxmsg:
            await ctx.send(f":x: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'clrError')}")
        else:
            await ctx.channel.purge(limit=amnt)
            await ctx.send(f":white_check_mark: {sender.mention} || {getTranslation(sender.guild.id, 'generalRes', 'clrSuccess')}")

    @clear.error
    async def clear_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f":x: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdNoPerms')}")

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
            await ctx.send(f":x: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdNoPerms')}")

        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == "user":
                await ctx.send(f":x: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdInvalidParam')}\n``>>kick [user]``")

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
            await ctx.send(f":x: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdNoPerms')}")

        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == "user":
                await ctx.send(f":x: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdInvalidParam')}\n``>>ban [user]``")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def softban(self, ctx, user: discord.Member, messages_to_del=7):
        sender = ctx.message.author
        await user.ban(reason='SOFTBANNED', delete_message_days=int(messages_to_del))
        await user.unban(reason=None)

        await ctx.send(f":white_check_mark: {sender.mention} || Softbanned ``{user.name}#{user.discriminator}``")

    @softban.error
    async def softban_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f":x: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdNoPerms')}")

        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == "user":
                await ctx.send(f":x: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdInvalidParam')}\n``>>softban [user]``")



    """ Server Settings Commands """
    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['settings', 'options', 'config'])
    async def setting(self, ctx, var, newvar):
        sender = ctx.message.author
        db = sqlite3.connect('SQL/settings.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT guild_id FROM serversettings where guild_id = '{}'".format(sender.guild.id))
        res = cursor.fetchone()
        if res is not None:
            if var == "language" or var == "lang":
                # TODO: Add a way to let users type in full language names
                # example: French, English, Japanese, Russian
                # Abbreviations are confusing somtimes!
                availableLangs = {
                    'en',
                    'fr',
                    'ru',
                    'es',
                    'lol'
                }
                if newvar.lower() in availableLangs:
                    cursor.execute(f"UPDATE serversettings SET lang = '{newvar}'")
                    db.commit()
                    await ctx.send(f":white_check_mark: Success! The new language is ``{newvar}``!")
                else:
                    await ctx.send(f":x: {sender.mention}, The language ``{newvar}`` is not present within my language file!")     
            elif var == "guild_id": await ctx.send(f":x: I'm sorry, {sender.mention}, but that value cannot be changed.")
            elif var == "prefix":
                cursor.execute(f"UPDATE serversettings SET prefix = '{newvar}'")
                db.commit()
                await ctx.send(f":white_check_mark: {sender.mention} || The new prefix is ``{newvar}``")


    @setting.error
    async def settings_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f":x: {sender.mention} || {getTranslation(sender.guild.id, 'errmsg', 'cmdNoPerms')}")


def setup(bot):
    bot.add_cog(AdminCommands(bot))
