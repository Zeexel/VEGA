
import json
import os
import datetime
import time
import psutil
import discord
import sqlite3
import utils.checks as checks
from discord.ext import commands

cfg = json.load(open("JSON/config.json", "r"))      # Config file
start_time = time.time()
bot = commands.Bot(command_prefix=cfg['prefix'])
bot.remove_command('help')      # Disable the default help command to replace it with the custom one

extensions = [
    'utils.error_handler',
    'cogs.fun',
    'cogs.reactions',
    'cogs.utils',
    'cogs.admin',
#    'cogs.economy', I'm gonna disable this for now, it's a bit broken
    'cogs.nsfw'
]


@bot.event
async def on_ready():
    activity = discord.Game(name=f"{cfg['prefix']}cmds | Version {cfg['version']}")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("(C) James P. 2020")
    print("I'm running discord.py version {},".format(discord.__version__))
    print("and I'm currently present in {} discord servers.".format(len(list(bot.guilds))))
    print("Errors and messages will appear below this line.")
    print("-----------------------------------------------")



@bot.command(aliases=['cmds', 'commands'])
async def help(ctx):
    sender = ctx.message.author
    await ctx.send("{}, here you go!\nhttps://gist.github.com/Zeexel/d68d3cd9bdf4a5147490b535a2640545"
                    .format(sender.mention))

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
    cursor.execute("SELECT guild_id FROM serversettings where guild_id = {}".format(guild.id))
    res = cursor.fetchone()
    if res is None:
        sql = ("INSERT INTO serversettings(guild_id) VALUES({})".format(guild.id))
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


""" Commands relating to server settings """

# TODO: Add translations for this command & add an available language list somewhere.

# @commands.has_permissions(administrator=True)
@bot.command(aliases=['settings', 'options', 'config'])
async def setting(ctx, action, var, newvar):
    sender = ctx.message.author
    db = sqlite3.connect('SQL/settings.sqlite')
    cursor = db.cursor()
    cursor.execute("SELECT guild_id FROM serversettings where guild_id = '{}'".format(sender.guild.id))
    res = cursor.fetchone()
    if res is not None:
        if action == "change" or "set":
            if var == "language" or "lang":
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
            
            if var == "guild_id": await ctx.send(f":x: I'm sorry, {sender.mention}, but that value cannot be changed.")


@commands.has_permissions(administrator=True)
@bot.command()
async def generateconfig(ctx):
    sender = ctx.message.author
    db = sqlite3.connect('SQL/settings.sqlite')
    cursor = db.cursor()          
    cursor.execute("SELECT guild_id FROM serversettings where guild_id = {}".format(sender.guild.id))
    res = cursor.fetchone()
    if res is None:
        sql = ("INSERT INTO serversettings(guild_id) VALUES({})".format(sender.guild.id))
        cursor.execute(sql)
        db.commit()
        await ctx.send(f":white_check_mark: {sender.mention}, a config file was successfully generated for your server!")
    else:
        await ctx.send(f":x: {sender.mention}, your server already has a config file!")


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
    await ctx.send(f"Now reloading extension ``{cog.lower()}``. Give me a moment..")
    print(f"Reloading extension {cog.lower()}.")
    # Try to unload the extension, if it's not unloaded already
    try: bot.unload_extension(cog.lower())
    except commands.errors.ExtensionNotLoaded: pass
    bot.load_extension(cog.lower())
    print(f"Successfully loaded {cog.lower()}")
    await ctx.send(f"The extension ``{cog.lower()}`` has been reloaded!")

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
