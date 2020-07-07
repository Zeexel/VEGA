from discord import Embed

import json
from discord.ext import commands

cfg = json.load(open("JSON/config.json", "r")) 

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['cmds', 'cmd'])
    async def help(self, ctx, page = None):
        
        initEmbed = Embed(title="VEGA Commands", description=f"Version {cfg['version']}", color=0x6ba6ff)  # NOTE: Add version number
        initEmbed.set_thumbnail(url='https://cdn.discordapp.com/avatars/618633293121847317/de4c54a0d734ff7b9ff17c729ddb589f.webp?size=1024')
        initEmbed.add_field(name="\u200b", value="🖊Utilities")
        initEmbed.add_field(name="\u200b", value="🎉Fun")
        initEmbed.add_field(name="\u200b", value="\u200b")
        initEmbed.add_field(name="\u200b", value="🚨Moderation")
        initEmbed.add_field(name="\u200b", value="🔞NSFW")

        utilEmbed = Embed(title="Utility Commands", color=0xd3fc60)
        utilEmbed.set_thumbnail(url='https://cdn.discordapp.com/avatars/618633293121847317/de4c54a0d734ff7b9ff17c729ddb589f.webp?size=1024')
        utilEmbed.add_field(name=">>profile [user]", value="Gets the profile of the user specified", inline=False)
        utilEmbed.add_field(name=">>avatar [user]", value="Gets the avatar of the user specified", inline=False)
        utilEmbed.add_field(name=">>guildinfo", value="Gets the info of the server", inline=False)
        utilEmbed.add_field(name=">>osustats [mode] [user]", value="Gets the mode stats of an OSU! player", inline=False)
        utilEmbed.add_field(name=">>myanimelist [manga/anime] [title]", value="Gets the info of a specified manga/anime", inline=False)
        utilEmbed.add_field(name=">>weather [city]", value="Gets the weather of a specified city (runs off OpenWeatherMap)", inline=False)

        funEmbed = Embed(title="Fun Commands", color=0x7afc60)
        funEmbed.set_thumbnail(url='https://cdn.discordapp.com/avatars/618633293121847317/de4c54a0d734ff7b9ff17c729ddb589f.webp?size=1024')
        funEmbed.add_field(name=">>8ball [question]", value="In a dillema? Get an answer from the magic 8-ball!", inline=False)
        funEmbed.add_field(name=">>flipacoin", value="Flips a coin. (NOTE: The UAC is not responsible for irresponsible gambling.)", inline=False)
        funEmbed.add_field(name=">>lovecalc [user1] [user2]", value="Calculates the love factor between two users.", inline=False)
        funEmbed.add_field(name=">>meme/animeme", value="Pulls random posts from r/dankmemes or r/animemes", inline=False)
        funEmbed.add_field(name=">>hug [user]", value="Hug another user!", inline=False)
        funEmbed.add_field(name=">>kiss [user]", value="Kiss another user!", inline=False)
        funEmbed.add_field(name=">>fuck [user]", value="uwu **(Only works in NSFW channels)**", inline=False)

        modEmbed = Embed(title="Moderation Commands", color=0xfc6060)
        modEmbed.set_thumbnail(url='https://cdn.discordapp.com/avatars/618633293121847317/de4c54a0d734ff7b9ff17c729ddb589f.webp?size=1024')
        modEmbed.add_field(name=">>clear [amnt]", value="Clears a specified amount of messages from the chat. Max is 500", inline=False)
        modEmbed.add_field(name=">>kick [user] *[reason]", value="Kicks a user from the server. Reason is optional.", inline=False)
        modEmbed.add_field(name=">>ban [user] *[reason]", value="Bans a user from the server. Reason is optional.", inline=False)
        modEmbed.add_field(name=">>softban [user]", value="Kicks a user from the server, but deletes their messages.", inline=False)
        modEmbed.add_field(name=">>config [var1] [newvar]", value="Changes parts of server configuration. An up-to-date list of server config vars can be found [here](https://gist.github.com/Zeexel/00c232be1dfdb6f3461ae927db56be22)", inline=False)

        nsfwEmbed = Embed(title="NSFW Commands", color=0x3b3b3b)
        nsfwEmbed.set_thumbnail(url='https://cdn.discordapp.com/avatars/618633293121847317/de4c54a0d734ff7b9ff17c729ddb589f.webp?size=1024')
        nsfwEmbed.add_field(name=">>rule34 [tag(s)]", value="Pulls an image from rule34.xxx based on the user's given tags", inline=False)
        nsfwEmbed.add_field(name=">>gelbooru [tag(s)]", value="Pulls an image from gelbooru.com based on the user's given tags", inline=False)
        nsfwEmbed.add_field(name=">>xbooru [tag(s)]", value="Pulls an image from xbooru.com based on the user's given tags", inline=False)
        nsfwEmbed.add_field(name=">>tits", value="It's pretty self-explanatory", inline=False)
        nsfwEmbed.add_field(name=">>ass", value="It's pretty self-explanatory", inline=False)
        nsfwEmbed.add_field(name=">>femboys", value="It's pretty self-explanatory", inline=False)

        if page == None:
            await ctx.send(embed=initEmbed)
        elif page == 'util' or page == 'utilities':
            await ctx.send(embed=utilEmbed)
        elif page == 'fun':
            await ctx.send(embed=funEmbed)
        elif page == 'admin' or page == 'moderation':
            await ctx.send(embed=modEmbed)
        elif page == 'nsfw' or page == 'adult':
            await ctx.send(embed=nsfwEmbed)




def setup(bot):
    bot.add_cog(Help(bot))