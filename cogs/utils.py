import discord
import requests as r
import json as j
from math import floor
import utils.checks as checks
from discord.ext import commands
from jikanpy import Jikan

cfg = j.load(open('JSON/config.json', 'r'))
jikan = Jikan()

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['getavatar', 'avi', 'pfp'])
    async def avatar(self, ctx, u: discord.Member=None):
        if u != None:
            pfpEmbed = discord.Embed(title=f"{u.display_name}'s Avatar", color=0x7289DA)
            pfpEmbed.set_image(url=u.avatar_url)
        else:
            s = ctx.message.author
            pfpEmbed = discord.Embed(title="Here's your avatar!", color=0x7289DA)
            pfpEmbed.set_image(url=s.avatar_url)

        await ctx.send(embed=pfpEmbed)

    @commands.command(aliases=['user', 'userinfo'])
    async def profile(self, ctx, u: discord.Member=None):
        if not isinstance(ctx.channel, discord.DMChannel):
            if u != None:
                userEmbed = discord.Embed(title=f"{u.name}#{u.discriminator}" if not u.bot else f"{u.name}#{u.discriminator} :robot:", description=f"ID: {u.id}", color=u.top_role.colour)
                userEmbed.set_thumbnail(url=u.avatar_url)
                userEmbed.add_field(name="Joined the server on", value=u.joined_at.strftime("%m/%d/%y"), inline=False)
                userEmbed.add_field(name="Joined discord on", value=u.created_at.strftime("%m/%d/%y"), inline=False)
                userEmbed.add_field(name="Roles:", value=", ".join([role.mention for role in u.roles]))
            else:
                s = ctx.message.author
                userEmbed = discord.Embed(title=f"{s.name}#{s.discriminator}", description=f"ID: {s.id}", color=s.top_role.colour)
                userEmbed.set_thumbnail(url=s.avatar_url)
                userEmbed.add_field(name="Joined the server on", value=s.joined_at.strftime("%m/%d/%y"), inline=False)
                userEmbed.add_field(name="Joined discord on", value=s.created_at.strftime("%m/%d/%y"), inline=False)
                userEmbed.add_field(name="Roles:", value=", ".join([role.mention for role in s.roles]))
        else: 
            s = ctx.message.author
            userEmbed = discord.Embed(title=f"{s.name}#{s.discriminator}", description=f"ID: {s.id}", color=0x7289DA)
            userEmbed.set_thumbnail(url=s.avatar_url)
            userEmbed.add_field(name="Joined discord on", value=s.created_at.strftime("%m/%d/%y"), inline=False)

        await ctx.send(embed=userEmbed)

    @checks.server_only()
    @commands.command(aliases=['serverinfo'])
    async def guildinfo(self, ctx):
        g = ctx.message.guild
        guildEmbed = discord.Embed(title=g.name, description=str(g.id), color=0x7289DA)
        guildEmbed.set_thumbnail(url=g.icon_url)
        guildEmbed.add_field(name="Server created", value=g.created_at.strftime("%m/%d/%y"), inline=False)
        guildEmbed.add_field(name="Region", value=g.region, inline=False)
        guildEmbed.add_field(name="Members", value=str(len(g.members)), inline=False)
        if len(g.premium_subscribers) > 0:
            guildEmbed.add_field(name="Nitro Boost Tier", value=f"Tier {g.premium_tier}, boosted by {len(g.premium_subscribers)} members.", inline=False)
        await ctx.send(embed=guildEmbed)

    @commands.command(aliases=['osu'])
    async def osustats(self, ctx, m, u):
        swticher = {
            'osu': 0,
            'taiko': 1,
            'ctb': 2,
            'mania': 3
        }
        # API setup
        url = f"https://osu.ppy.sh/api/get_user?k={cfg['api_keys']['osu_api_key']}&u={u}&m={swticher.get(m)}"
        data = r.get(url=url).json()

        osuEmbed = discord.Embed(title=f"Stats for user {data[0]['username']}", description=f"ID: {data[0]['user_id']}", color=0xff8cd5)
        osuEmbed.set_thumbnail(url=f"http://s.ppy.sh/a/{data[0]['user_id']}")
        osuEmbed.add_field(name="Joined OSU", value=data[0]['join_date'], inline=False)
        osuEmbed.add_field(name="Level", value=str(floor(float(data[0]['level']))))
        osuEmbed.add_field(name="Beatmaps Played", value=data[0]['count300'], inline=False)
        osuEmbed.add_field(name="S/SS/SH/A Ranks achieved", value=data[0]['count_rank_s'], inline=False)
        osuEmbed.set_footer(text=f"{data[0]['username']} - Rank {data[0]['pp_rank']} Globally, {data[0]['pp_country_rank']} in {data[0]['country']}.")

        await ctx.send(embed=osuEmbed)
        
    @commands.command()
    async def weather(self, ctx, *, city):
        try:
            data = r.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={cfg['api_keys']['weather_key']}").json()
            icon = f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"

            def convK2C(var):
                C = var - 273.15
                return f"{round(C)}°C"
            
            weatherEmbed = discord.Embed(title=f"Weather in {data['name']}, {data['sys']['country']}", color=0x616161, description=data['weather'][0]['main'])
            weatherEmbed.set_thumbnail(url=icon)
            weatherEmbed.set_footer(text="Data from OpenWeatherMap")
            weatherEmbed.add_field(name="Temperature", value=convK2C(data['main']['temp']), inline=False)
            weatherEmbed.add_field(name="Today's High", value=convK2C(data['main']['temp_max']), inline=False)
            weatherEmbed.add_field(name="Today's low", value=convK2C(data['main']['temp_min']), inline=False)

            await ctx.send(embed=weatherEmbed)
        except KeyError: await ctx.send(":x: KeyError, this text must be localized.")

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

def setup(bot):
    bot.add_cog(Utilities(bot))