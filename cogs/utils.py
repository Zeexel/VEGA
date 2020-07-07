# Utils cog

import discord
import json
import requests
import math
import datetime
import utils.checks as checks
from utils.functions import getTranslation
from jikanpy import Jikan
from discord.ext import commands

cfg = json.load(open("JSON/config.json", "r"))
jikan = Jikan()


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["getavatar", "pfp", "getpfp"])
    async def avatar(self, ctx, user: discord.Member=None):
        sender = ctx.message.author
        if user == None:
            await ctx.send("{} || Here's your avatar!".format(sender.mention))
            await ctx.send(sender.avatar_url)
        else:
            await ctx.send("{} || Here's {}'s avatar!".format(sender.mention, user.name))
            await ctx.send(user.avatar_url)

    @commands.command(aliases=['whois'])
    async def profile(self, ctx, user: discord.Member=None):
        sender = ctx.message.author
        # Create embed
        if isinstance(ctx.channel, discord.DMChannel):
            embed = discord.Embed(title="{}#{} :robot:".format(sender.name, sender.discriminator) if sender.bot else "{}#{}".format(sender.name, sender.discriminator),
                                  description="ID: " + str(sender.id),
                                  color=0x858585)
            embed.set_thumbnail(url=sender.avatar_url)

            embed.add_field(name="Display Name", value=sender.display_name,
                            inline=False)
            embed.add_field(name="Joined Discord on", value=sender.created_at.strftime("%m/%d/%y"), inline=False)
        elif user != None:
            embed = discord.Embed(title="{}#{} :robot:".format(user.name, user.discriminator) if user.bot else "{}#{}".format(user.name, user.discriminator),
                                  description="ID: " + str(user.id),
                                  color=user.top_role.colour)
            embed.set_thumbnail(url=user.avatar_url)

            embed.add_field(name="Display Name", value=user.display_name,
                            inline=False)
            embed.add_field(name="Joined the server on", value=user.joined_at.strftime("%m/%d/%y"), inline=False)
            embed.add_field(name="Joined Discord on", value=user.created_at.strftime("%m/%d/%y"), inline=False)
            embed.add_field(name="Roles", value=", ".join([role.mention for role in user.roles]))
        else:
            
            embed = discord.Embed(title="{}#{} :robot:".format(sender.name, sender.discriminator) if sender.bot else "{}#{}".format(sender.name, sender.discriminator),
                                  description="ID: " + str(sender.id),
                                  color=sender.top_role.colour)
            embed.set_thumbnail(url=sender.avatar_url)

            embed.add_field(name="Display Name", value=sender.display_name,
                            inline=False)
            embed.add_field(name="Joined the server on", value=sender.joined_at.strftime("%m/%d/%y"), inline=False)
            embed.add_field(name="Joined Discord on", value=sender.created_at.strftime("%m/%d/%y"), inline=False)
            embed.add_field(name="Roles", value=", ".join([role.mention for role in sender.roles]))
        
        await ctx.send(embed=embed)

    @checks.server_only()
    @commands.command(aliases=['serverinfo'])
    async def guildinfo(self, ctx):
        guild = ctx.message.guild

        embed = discord.Embed(title=guild.name, color=0xfc5246, description=str(guild.id))
        embed.set_thumbnail(url=guild.icon_url)

        embed.add_field(name="Guild owner", value=guild.owner.mention, inline=False)
        embed.add_field(name="Created on", value=guild.created_at.strftime("%m/%d/%y"), inline=False)
        embed.add_field(name="Member Count", value=str(len(guild.members)))
        if len(guild.premium_subscribers) != 0:
            embed.add_field(name="Nitro Boost status", value=f"Tier {str(guild.premium_tier)}, boosted by {len(guild.premium_subscribers)} members.", inline=False)
        embed.add_field(name="Region", value=guild.region, inline=False)

        await ctx.send(embed=embed)

    @guildinfo.error
    async def guilderror_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, checks.NoDM):
            await ctx.send(f"{sender.mention} || This command has been disabled for DM channels.")

    @commands.command(aliases=['osu'])
    async def osustats(self, ctx, m, *, user):
        s = ctx.message.author
        modes = {'osu':'0','taiko':'1','ctb':'2','mania':'3'}   # Wow, this is way better than spamming 'elif' statements!
        print(modes.get(m.lower()))
        try:
            d = requests.get(f"https://osu.ppy.sh/api/get_user?k={cfg['osu_api_key']}&m={modes.get(m.lower())}&u={user}").json()

            osuEmbed = discord.Embed(title=f"Info for {d[0]['username']}", color=0xff8ae6,description=f"User ID: {d[0]['user_id']}")
            osuEmbed.set_thumbnail(url=f"http://s.ppy.sh/a/{d[0]['user_id']}")
            osuEmbed.add_field(name="Join Date (UTC)", value=f"{d[0]['join_date']}",inline=False)
            osuEmbed.add_field(name='Level', value=f"{str(round(float(d[0]['level'])))}", inline=False)
            osuEmbed.add_field(name='Beatmaps Played', value=f"{d[0]['playcount']}", inline=False)     #  Only counts ranked, approved, and loved beatmaps
            osuEmbed.add_field(name='Accuracy', value=f"{d[0]['accuracy']}", inline=False)
            osuEmbed.add_field(name='Country', value=f"{d[0]['country']}", inline=False)
            osuEmbed.add_field(name='S Ranks', value=f"{d[0]['count_rank_s']}")    # Counts for SS/SSH/S/SH/A ranks on maps
            osuEmbed.add_field(name='A ranks', value=f"{d[0]['count_rank_a']}")
            osuEmbed.set_footer(text=f"{d[0]['username']} - Rank {d[0]['pp_rank']} Globally, {d[0]['pp_country_rank']} in {d[0]['country']}", icon_url=f"http://s.ppy.sh/a/{d[0]['user_id']}")

            await ctx.send(embed=osuEmbed)
        except TypeError:
            if isinstance(ctx.channel, discord.DMChannel):
                await ctx.send(f":x: {s.mention} || {getTranslation(None, 'errmsg', 'userNotFound')} ``{user}``")
            else: await ctx.send(f":x: {s.mention} || {getTranslation(s.guild.id, 'errmsg', 'userNotFound')} ``{user}``")
        except KeyError:
            if isinstance(ctx.channel, discord.DMChannel):
                await ctx.send(f":x: {s.mention} || {getTranslation(None, 'errmsg', 'cmdError')}")
            else: await ctx.send(f":x: {s.mention} || {getTranslation(s.guild.id, 'errmsg', 'cmdError')}")
        except IndexError:
            if isinstance(ctx.channel, discord.DMChannel):
                await ctx.send(f":x: {s.mention} || {getTranslation(None, 'errmsg', 'cmdError')}")
            else: await ctx.send(f":x: {s.mention} || {getTranslation(s.guild.id, 'errmsg', 'cmdError')}")

    @commands.command(aliases=['mal'])
    async def myanimelist(self, ctx, type, title, *subtype):
 
        if type == "user":
            user = jikan.user(username=title)
            embed = discord.Embed(title=user['username'], url=user['url'], description=f"MAL User ID: {str(user['user_id'])}", color=0x2d58c4)
            embed.set_thumbnail(url=user['image_url'])
            embed.add_field(name='Mean Score', value=str(user['anime_stats']['mean_score']), inline=False)
            embed.add_field(name='Watching', value=str(user['anime_stats']['watching']))
            embed.add_field(name='On Hold', value=str(user['anime_stats']['on_hold']))
            embed.add_field(name='Dropped', value=str(user['anime_stats']['dropped']))
            embed.add_field(name='Completed', value=str(user['anime_stats']['completed']))
            embed.add_field(name='Episodes Watched', value=str(user['anime_stats']['episodes_watched']))

            await ctx.send(embed=embed)
        else:
            res = jikan.search(type, title)
            embed = discord.Embed(title=res['results'][0]['title'], color=0x2d58c4, description="Scored " + str(res['results'][0]['score']), url=res['results'][0]['url'])
            embed.set_thumbnail(url=res['results'][0]['image_url'])
            embed.add_field(name='Synopsis', value=res['results'][0]['synopsis'], inline=False)

            if type == "anime":
                embed.add_field(name="Airing?", value="Yes" if res['results'][0]['airing'] == True else "No", inline=False)
                embed.add_field(name='Episodes', value=str(res['results'][0]['episodes']), inline=False)

            if type == "manga":
                embed.add_field(name="Publishing?", value="Yes" if res['results'][0]['publishing'] == True else "No", inline=False)
                embed.add_field(name="Chapters", value=str(res['results'][0]['chapters']), inline=False)
                embed.add_field(name="Volumes", value=str(res['results'][0]['volumes']), inline=False)
            
            embed.add_field(name="Type", value=res['results'][0]['type'])
            embed.add_field(name='MAL ID', value=str(res['results'][0]['mal_id']))

            await ctx.send(embed=embed)
  
    @commands.command()
    async def weather(self, ctx, *, city):
        sender = ctx.message.author

        try:
            res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={cfg['weather_key']}")
            data = res.json()
            icon = f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
            
            def convertK2C(var1):   # For whatever reason, OpenWeatherMap uses Kelvin by default
                C = var1 - 273.15
                return str(round(C)) + "°C"

            embed = discord.Embed(title=f"{data['name']}, {data['sys']['country']}", color=0x616161, description=data['weather'][0]['main'])
            embed.set_thumbnail(url=icon)
            embed.set_footer(text="Data from OpenWeatherMap")
            
            embed.add_field(name="Temperature", value=convertK2C(data['main']['temp']))
            embed.add_field(name="Feels Like..", value=convertK2C(data['main']['feels_like']))
            embed.add_field(name="Today's High", value=convertK2C(data['main']['temp_max']))
            embed.add_field(name="Today's Low", value=convertK2C(data['main']['temp_min']))
            embed.add_field(name="Humidity", value=f"{str(data['main']['humidity'])}%")
            embed.add_field(name="Wind Speed", value=f"{str(round(data['wind']['speed'] * 3.6))} KMH")

            await ctx.send(embed=embed)
        except KeyError: await ctx.send(f":x: {sender.mention} || {getTranslation(ctx.message.guild.id, 'errmsg', 'owmLocNotFound')} ``{city}``")


def setup(bot):
    bot.add_cog(Utils(bot))