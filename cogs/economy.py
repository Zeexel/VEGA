import sqlite3
import random
import discord
import utils.checks as checks
from discord.ext import commands

jobs = ['uac engineer','demon slayer','space marine']

db = sqlite3.connect('SQL/main.sqlite')     # Connect to main SQLite Database
cursor = db.cursor()

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def openacc(self, ctx):
        """ Opens a global bank account for a user """
        sender = ctx.message.author

        # Execute some SQL to check if the user already has a bank account
        cursor.execute(f"SELECT user_id FROM economy WHERE user_id = '{sender.id}'")
        result = cursor.fetchone()
        print(result)
        if result is None:
            await ctx.send(f"Opening a UAC bank account for you, {sender.mention}..\nPlease give me a moment..")
            
            async with ctx.typing():
                # Make a bank account using the user's ID
                sql = ("INSERT INTO economy(user_id, money, job) VALUES(?, ?, ?)")
                vals = (sender.id, 100, None)
                cursor.execute(sql, vals)

                db.commit()

                print(f"Added {sender.name}#{sender.discriminator} to the Economy SQL database.")

            await ctx.send(f"There you go, {sender.mention}! You now have a UAC bank account.")

        else:
            await ctx.send(f"It seems you already have a bank account with the UAC, {sender.mention}..")


    @commands.command(aliases=['balance'])
    async def bal(self, ctx, user: discord.Member = None):
        """ Check a user's balance """
        sender = ctx.message.author

        if user is None:    # Default to showing the user's balance
            cursor.execute(f"SELECT user_id, money, job FROM economy WHERE user_id = '{sender.id}'")
            result = cursor.fetchone()

            if result is not None:
                embed = discord.Embed(title=f"Balance for {sender.name}",
                                    description=f"ID: {sender.id}",
                                    color=sender.top_role.colour)
                embed.set_thumbnail(url=sender.avatar_url)
                embed.add_field(name="Money", value=f"${str(result[1])}")
                embed.add_field(name="Job", value=result[2])

                await ctx.send(embed=embed)
            else:
                 await ctx.send(f"{sender.mention}, you need to open a bank account first!\nType ``>>openacc`` to open a bank account with the UAC.")
 
        else:   # Otherwise, show them another user's balance
            cursor.execute(f"SELECT user_id, money, job FROM economy WHERE user_id = '{user.id}'")
            result = cursor.fetchone()

            if result is not None:
                embed = discord.Embed(title=f"Balance for {user.name}",
                                    description=f"ID: {user.id}",
                                    color=user.top_role.colour)
                embed.set_thumbnail(url=user.avatar_url)
                embed.add_field(name="Money", value=f"${str(result[1])}")
                embed.add_field(name="Job", value=result[2])

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"{sender.mention}, {user.name} doesn't have an account with the UAC banking system.")


    @commands.command()
    async def give(self, ctx, user: discord.Member, amnt):
        """ Give other users money """
        # TODO: Make a check to prevent users from giving others ALL their money
        sender = ctx.message.author

        # Check if the user has a bank account
        cursor.execute(f"SELECT user_id, money FROM economy where user_id = '{sender.id}'")
        res = cursor.fetchone()
        if res is None: await ctx.send(f"You need a bank account opened to do that, {sender.mention}, use ``>>openacc`` to open one!")

        if user != sender:
            # Check if the user has enough cash
            if int(res[1]) < int(amnt):
                await ctx.send(f"You don't have enough cash for that, {sender.mention}.")
            else:
                cursor.execute(f"SELECT user_id, money FROM economy where user_id = '{user.id}'")
                res1 = cursor.fetchone()
                
                if res1 is not None:
                    sndr_bal = int(res[1])
                    user_bal = int(res1[1])

                    cursor.execute(f"UPDATE economy SET money = '{int(sndr_bal - int(amnt))}' where user_id = '{sender.id}'")    # Subtract money from the sender
                    cursor.execute(f"UPDATE economy SET money = '{int(user_bal + int(amnt))}' where user_id = '{user.id}'")     # Add money to the recipient

                    user_bal = int(user_bal + int(amnt))    # New user balance, done lasily
                    db.commit()

                    await ctx.send(f"{sender.mention} || Done. {user.mention} now has ${str(user_bal)}.")
                else:
                    await ctx.send(f"{user.mention} doesn't have a bank account, {sender.mention}..")

        else: await ctx.send(f"You can't give money to yourself, {sender.mention}.")

        """ Shop Stuff """
        
    @checks.is_owner()
    @commands.command()
    async def additem(self, ctx, id, price, *, name):
        """         [BOT OWNER ONLY]
            Create buyable items in the shop """

        # Check if the item exists
        cursor.execute(f"SELECT item_id FROM store where item_id = '{id}'")
        res = cursor.fetchone()
        if res is None:
            await ctx.send(f"Item ``{id}`` does not exist in the store.. Creating it now.")

            async with ctx.typing():
                sql = ("INSERT INTO store(item_id, item_name, price) VALUES(?, ?, ?)")
                val = (id, name, price)
                cursor.execute(sql, val)
                db.commit()

                await ctx.send(f"Item ``{id}`` created.")
        else:
            await ctx.send(f"{ctx.message.author.mention}, item ``{id}`` already exists.")

    @checks.is_owner()
    @commands.command()
    async def delitem(self, ctx, id):
        """    [BOT OWNER ONLY]
        Create buyable items in the shop """
        
        cursor.execute(f"SELECT item_id FROM store where item_id = '{id}'")
        res = cursor.fetchone()
        
        if res is not None:
            await ctx.send(f"Removing item ``{id}`` from the store..")

            async with ctx.typing():
                cursor.execute(f"DELETE FROM store WHERE item_id = '{id}'")
                db.commit()
            
            await ctx.send(f"Deleted ``{id}`` from the store.")
        
        else:
            await ctx.send(f"Item ``{id}`` does not exist.")

    @commands.command()
    async def shop(self, ctx):
        cursor.execute("SELECT * FROM store")
        res = cursor.fetchall()
        print(res)

        embed = discord.Embed(title="UAC Item shop",
                              color=0x47acff)
        for item in res:
            cursor.execute(f"SELECT item_name FROM store WHERE item_id = '{item[0]}'")
            name = cursor.fetchone()
            cursor.execute(f"SELECT price FROM store WHERE item_id = '{item[0]}'")
            price = cursor.fetchone()
            embed.add_field(name=name, value=f"💴 {price}", inline=False)

        # TODO: Clean this up, make pages for shop

        await ctx.send(embed=embed)

    
    @commands.command()
    async def buy(self, ctx, *, name):
        print("BUYyyyeyeybe")
            


def setup(bot):
    bot.add_cog(Economy(bot))