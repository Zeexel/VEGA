import discord
import asyncio
from discord.ext import commands

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(alias=['purge', 'cleanmsgs'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amnt=10, maxmsg=500):
        if amnt <= maxmsg:
            s = ctx.message.author
            await ctx.channel.purge(limit=amnt + 1)     # Account for the user's message to clear the chat.
            purgeEmbed = discord.Embed(title=f"{amnt} messages successfully cleared!", color=0xff6052)
            purgeEmbed.set_author(name=f"{s.name}#{s.discriminator}", icon_url=s.avatar_url)
            msg = await ctx.send(embed=purgeEmbed)
            await asyncio.sleep(5)
            await msg.delete()
        else: await ctx.send(":x: Over the limit, this needs to be localized.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, u: discord.Member, *, reason=None):
        s = ctx.message.author
        await u.kick(reason=reason)
        kickEmbed = discord.Embed(title=f"Kicked user {u.name}#{u.discriminator}", color=0xff6052)
        kickEmbed.set_thumbnail(url=u.avatar_url)
        kickEmbed.set_author(name=f"{s.name}#{s.discriminator}", icon_url=s.avatar_url)
        if reason != None: kickEmbed.add_field(name="Reason", value=reason)
        await ctx.send(embed=kickEmbed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def ban(self, ctx, u: discord.Member, *, reason=None, md=0):
        s = ctx.message.author
        await u.ban(reason=reason, delete_message_days=md)
        banEmbed = discord.Embed(title=f"Banned user {u.name}#{u.discriminator}", color=0xff6052)
        banEmbed.set_thumbnail(url=u.avatar_url)
        banEmbed.set_author(name=f"{s.name}#{s.discriminator}", icon_url=s.avatar_url)
        if reason != None: banEmbed.add_field(name="Reason", value=reason)
        await ctx.send(embed=banEmbed)

    # TODO: ADD THESE FEATURES
    @commands.command()
    async def softban(self, ctx):
        pass

    @commands.command()
    async def warn(self, ctx):
        pass

    @commands.command()
    async def mute(self, ctx):
        """
        General idea for this:
        - Looks for a 'muted' role
        * Not able to find one? Make one.
        * Set role to not be able to speak in most chats,
          albeit im not entirely sure how well that'll work.
        - Add the muted role to the user
        - Time muted is optional
        """
        pass

    @commands.command()
    async def config(self, ctx):
        pass

    



def setup(bot):
    bot.add_cog(Administration(bot))