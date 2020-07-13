
#                   !!! YOU SHOULDN'T BE BUILDING OFF THIS VERSION !!!
"""
    This version of the bot is for the rewrite of VEGA/はかせ
    The primary goal of this version is to have the bot be more effecient, less bug ridden, and a general rewrite
    of the codebase for my own sake, and the sake of others.

    You shouldn't be building off this version due to the fact that alot of the code is still unfinished, and is probably generally bug-ridden.

    If you've forked/cloned this version to help with the bot, thank you! Your help is greatly appreciated :>

    ~ James P.
"""
import json
import pathlib
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

@bot.event
async def on_ready():
    activity = discord.Game(name=f">>cmds | Version {cfg['bot']['version']}")
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

# Autoload Cogs
for path in pathlib.Path("cogs").iterdir():
    if path.is_file():
        basename = path.name
        split = basename.split(".")
        fn = f"cogs.{split[0]}"
        
        try:
            bot.load_extension(fn)
            print(f"Successfully loaded {fn}")
        except Exception as e:
            exc = (f"{type(e).__name__}: {e}")
            print(f"Unable to load {fn}:\n {exc}")


bot.run(cfg['bot']['token'])   # Log into the bot
