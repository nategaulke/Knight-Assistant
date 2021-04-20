import datetime as dt
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from pymongo import MongoClient


load_dotenv()
MONGO_URL = os.getenv('MONGO_URL')

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['addevent'], help = "Adds event to the server's calendar.")
    async def add_event(self, ctx, name = None, date = None, time = None):
        if ctx.author == bot.user:
            return
        if name == None:
            await ctx.send('Please redo command with the name of your event and the date')
            return
        if date == None:
            await ctx.send('Did you mean to add a task instead? Otherwise please redo command with a date')
            return
        
        # Create a datetime object for storing the date
        date = dt.datetime.strptime(date, '%B %d, %Y')

        # Connect to MongoDB and to collection
        client = MongoClient(MONGO_URL)
        db = client["Database"]
        collection = db["Events"]

        if time == None:
            # Create Document & add to the collection
            event = {'Time': date, 'Name': name, 'UserID': ctx.author.display_name, 'Guild': ctx.message.guild.name}
            collection.insert_one(event)
            embed = discord.Embed(title = 'Your event has been added to ' + ctx.message.guild.name, color = discord.Color(0xFFFF00))
            embed.add_field(name = name, value = date.strftime('%B %d, %Y'), inline=False)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/a/a2/Calendar_12.png")
            embed.set_footer(text = ctx.author.display_name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            # Concatentate date with the specific time of the event
            time = dt.datetime.strptime(time, "%I:%M %p").time()
            date = dt.datetime.combine(date, time)

            # Create Document & add to the collection
            event = {'Time': date, 'Name': name, 'UserID': ctx.author.display_name, 'Guild': ctx.message.guild.name}
            collection.insert_one(event)
            embed = discord.Embed(title = 'Your event has been added to ' + ctx.message.guild.name, color = discord.Color(0xFFFF00))
            embed.add_field(name = name, value = date.strftime('%B %d, %Y at %I:%M %p'), inline=False)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/a/a2/Calendar_12.png")
            embed.set_footer(text = ctx.author.display_name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed=embed)
        return

    @commands.command(aliases=['events', 'calendar'], help = "Shows the events on the server's calendar.")
    async def show_events(self, ctx):
        if ctx.author == bot.user:
            return
        
        # Connect to MongoDB and to collection
        client = MongoClient(MONGO_URL)
        db = client["Database"]
        collection = db["Events"]

        # Check if there are any guild documents in the collection beforehand
        if collection.find({'Guild': ctx.message.guild.name}).count() == 0:
            embed = discord.Embed(title = 'No Events are on ' + ctx.message.guild.name, color = discord.Color(0xFFFF00), timestamp = ctx.message.created_at)
            embed.add_field(name = 'To add events use !addevent and separate name, date, and time using "" ', value = 'Example: !addevent "name" "date" "time(optional)"',inline=False)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/a/a2/Calendar_12.png")
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(title = 'Events on ' + ctx.message.guild.name, color = discord.Color(0xFFFF00), timestamp = ctx.message.created_at)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/a/a2/Calendar_12.png")
        # If there are events, print them sorted by their date/time
        for event in collection.find({'Guild': ctx.message.guild.name}).sort("Time"):
            embed.add_field(name = event["Name"], value = event["Time"].strftime('%B %d, %Y at %I:%M %p'), inline=False)
        await ctx.send(embed=embed)
        return

    @commands.command(aliases=['delevent', 'delete_event', 'delevents'], help = "Deletes an event with the given name or all events.")
    async def del_event(self, ctx, name = None):
        if ctx.author == bot.user:
            return

        # Connect to MongoDB and to collection
        client = MongoClient(MONGO_URL)
        db = client["Database"]
        collection = db["Events"]

        # Check if there are any guild documents in the collection beforehand
        if collection.find({'Guild': ctx.message.guild.name}).count() == 0:
            embed = discord.Embed(title = 'No Events are on ' + ctx.message.guild.name, color = discord.Color(0xFFFF00), timestamp = ctx.message.created_at)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/a/a2/Calendar_12.png")
            await ctx.send(embed=embed)
            return

        if name == None:
            ctx.send('Please redo command with the name of the event you would like to delete')
            return

        # If user says "all" then all documents from the guild will be deleted from the collection        
        if name.lower() == "all":
            collection.delete_many({'Guild': ctx.message.guild.name})
            embed = discord.Embed(title = 'All events have been deleted from ' + ctx.message.guild.name, color = discord.Color(0xFFFF00), timestamp = ctx.message.created_at)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/a/a2/Calendar_12.png")
            embed.set_footer(text = ctx.author.display_name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        
        # If user specifies a name, then collection is searched for the unique name
        for event in collection.find({'Guild': ctx.message.guild.name}):
            if name.lower() == event["Name"].lower():
                embed = discord.Embed(title = 'Your event has been deleted from ' + ctx.message.guild.name, color = discord.Color(0xFFFF00))
                embed.add_field(name = event["Name"], value = event["Time"].strftime('%B %d, %Y at %I:%M %p'), inline=False)
                embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/a/a2/Calendar_12.png")
                embed.set_footer(text = ctx.author.display_name, icon_url = ctx.author.avatar_url)
                await ctx.send(embed=embed)
                
                # Once the name is found, it is deleted from the collection
                collection.delete_one({'Time': event["Time"], 'Name': event["Name"], 'UserID': event["UserID"], 'Guild': event["Guild"]})
                return

        embed = discord.Embed(title = 'Event is not listed in ' + ctx.message.guild.name, color = discord.Color(0xFFFF00))
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/a/a2/Calendar_12.png")
        await ctx.send(embed=embed)
        return

def setup(bot):
    bot.add_cog(Events(bot))
