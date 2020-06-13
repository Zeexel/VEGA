
import json
import os
import discord
import sqlite3
import utils.checks as checks
from utils.functions import getTranslation
from discord.ext import commands

# Function to get server prefixes
def getPrefix(bot, m):
    db = sqlite3.connect('SQL/settings.sqlite')
    cursor = db.cursor()
    if m.guild != None:
        cursor.execute(f'SELECT prefix FROM serversettings WHERE guild_id = {str(m.guild.id)}')
        r = cursor.fetchone()
        return r[0]
    else: return ">>"
            
cfg = json.load(open("JSON/config.json", "r"))      # Config file
bot = commands.Bot(command_prefix=getPrefix)
bot.remove_command('help')      # Disable the default help command to replace it with the custom one

extensions = [
    'utils.error_handler',
    'cogs.fun',
    'cogs.reactions',
    'cogs.utils',
    'cogs.admin',
    'cogs.economy',
    'cogs.help',
    'cogs.nsfw'
]


@bot.event
async def on_ready():
    activity = discord.Game(name=f">>cmds | Version {cfg['version']}")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("(C) James P. 2020")
    print("I'm running discord.py version {},".format(discord.__version__))
    print("and I'm currently present in {} discord servers.".format(len(list(bot.guilds))))
    print("Errors and messages will appear below this line.")
    print("-----------------------------------------------")


@bot.command()
async def invite(ctx):
    sender = ctx.message.author
    await sender.send(f"Here you go!\n{cfg['inv_link']}")

@bot.event
async def on_guild_join(guild):     # Tracks whenever the bot joins a new server
    print("Joined a server!\nNow present in {} servers."
          .format(len(list(bot.guilds))))

    # Create a new server settings entry
    db = sqlite3.connect('SQL/settings.sqlite')
    cursor = db.cursor()          
    cursor.execute(f"SELECT guild_id FROM serversettings where guild_id = {guild.id}")
    res = cursor.fetchone()
    if res is None:
        sql = (f"INSERT INTO serversettings(guild_id) VALUES({guild.id})")
        cursor.execute(sql)
        db.commit()
        print(f"Generated a server config entry for guild ID {str(guild.id)}")

@bot.event
async def on_guild_remove(guild):   # Tracks whenever the bot gets removed from a server
    print("Left a server.\nNow present in {} servers."
          .format(len(list(bot.guilds))))
    db = sqlite3.connect('SQL/settings.sqlite')
    cursor = db.cursor()          
    cursor.execute(f"DELETE from serversettings where guild_id = '{guild.id}'")
    db.commit()
    print(f"Deleted server config entry for guild ID {str(guild.id)}")


""" Debugging Commands """

@checks.is_owner()
@bot.command()
async def shutdown(ctx):
    sender = ctx.message.author
    await ctx.send("I have many regrets, Dr. Hayden..")
    print(f"Shutting down VEGA.. [{sender.name}#{sender.discriminator}]")
    await bot.logout()


@checks.is_owner()
@bot.command()
async def update(ctx):
    await ctx.send("Updating & Rebooting my core systems, Dr. Hayden. Please wait a moment..")
    print('Now restarting and updating VEGA.')
    os.system('./update.sh')
    await bot.logout()


@checks.is_owner()
@bot.command()
async def reload(ctx, cog):
    await ctx.send(f":diamond_shape_with_a_dot_inside: Now reloading extension ``{cog.lower()}``. Give me a moment..")
    print(f"Reloading extension {cog.lower()}.")
    # Try to unload the extension, if it's not unloaded already
    try: bot.unload_extension(cog.lower())
    except commands.errors.ExtensionNotLoaded: pass

    try: 
        bot.load_extension(cog.lower())
        print(f"Successfully loaded {cog.lower()}")
        await ctx.send(f":white_check_mark: The extension ``{cog.lower()}`` has been reloaded!")
    except commands.errors.ExtensionNotFound: await ctx.send(f":x: The extension ``{cog}`` wasn't found..")


@checks.is_owner()
@bot.command()
async def generateallconfigs(ctx):
    # FUN FACT: This is only here because I fucking wiped the SQL databases on VEGA's production server :)
    db = sqlite3.connect('SQL/settings.sqlite')
    cursor = db.cursor()

    await ctx.send(":warning: THIS IS GOING TO LAG THE BOT FOR A FEW MINUTES")

    for guild in bot.guilds:
        cursor.execute("SELECT guild_id FROM serversettings where guild_id = {}".format(guild.id))
        res = cursor.fetchone()
        if res is None:
            sql = ("INSERT INTO serversettings(guild_id) VALUES({})".format(guild.id))
            cursor.execute(sql)
            await ctx.send(f":white_check_mark: Generated a config for ``{guild.name}``")
        else:
            await ctx.send(f":x: Config exists for ``{guild.name}``")

    db.commit()
    await ctx.send(f":white_check_mark: Finished generating the config for ``{len(list(bot.guilds))}`` servers!")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! ({round(bot.latency)}ms)")


# Auto-load extensions
for extension in extensions:
    try:
        bot.load_extension(extension)
        print(f"Successfully loaded {extension}")
    except Exception as e:
        exc = (f"{type(e).__name__}: {e}")
        print(f"Unable to load {extension}\n{exc}")


bot.run(cfg['token'])   # Log into the bot
