import discord
import sqlite3
import utils.checks as checks
from discord.ext import commands
from bot import bot as client       # NOTE: This may not be the best way to try and call the bot account..

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.is_owner()
    @commands.command()
    async def shutdown(self, ctx):
        sender = ctx.message.author
        await ctx.send("I have many regrets, Dr. Hayden..")
        print(f"Shutting down VEGA.. [{sender.name}#{sender.discriminator}]")
        await client.logout()

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! ({round(client.latency)}ms)")

    @checks.is_owner()
    @commands.command()
    async def reload(self, ctx, cog):
        await ctx.send(f":diamond_shape_with_a_dot_inside: Now reloading extension ``{cog.lower()}``. Give me a moment..")
        print(f"Reloading extension {cog.lower()}.")
        # Try to unload the extension, if it's not unloaded already
        try: client.unload_extension(cog.lower())
        except commands.errors.ExtensionNotLoaded: pass

        try: 
            client.load_extension(cog.lower())
            print(f"Successfully loaded {cog.lower()}")
            await ctx.send(f":white_check_mark: The extension ``{cog.lower()}`` has been reloaded!")
        except commands.errors.ExtensionNotFound: await ctx.send(f":x: The extension ``{cog}`` wasn't found..")


    @checks.is_owner()
    @commands.command()
    async def generateallconfigs(self, ctx):
        """
        This is here because I once forgot to put the blank SQL files in the .gitignore for the live server
        and it ended up wiping all server configurations, around 50 iirc.
        """
        pass

def setup(bot):
    bot.add_cog(Debug(bot))