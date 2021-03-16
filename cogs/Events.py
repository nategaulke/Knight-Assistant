import discord
from discord.ext import commands
import datetime as dt

events = []

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['addevent'], help = "Adds event to the server's calendar")
    async def add_event(self, ctx, name = None, date = None, time = None):
        if ctx.author == bot.user:
            return
        if name == None:
            await ctx.send('Please redo command with the name of your event and the date')
            return
        if date == None:
            await ctx.send('Did you mean to add a task instead? Otherwise please redo command with a date')
            return
        
        # create a date object for storing the information, must use strftime when translating date to string to print to user
        date = dt.datetime.strptime(date, '%B %d, %Y')
        
        if time == None:
            events.append((name, date))
            embed = discord.Embed(title = 'Your event has been added to ' + ctx.message.guild.name, color = discord.Color(0xFFFF00))
            embed.add_field(name = events[-1][0], value = events[-1][1].strftime('%B %d, %Y'), inline=False)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/a/a2/Calendar_12.png")
            embed.set_footer(text = ctx.author.display_name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            events.append((name, date, time))
            embed = discord.Embed(title = 'Your event has been added to ' + ctx.message.guild.name, color = discord.Color(0xFFFF00))
            embed.add_field(name = events[-1][0], value = events[-1][1].strftime('%B %d, %Y') + " at " + events[-1][2], inline=False)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/a/a2/Calendar_12.png")
            embed.set_footer(text = ctx.author.display_name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed=embed)
        return
    
    @commands.command(aliases=['events', 'calendar'], help = "Shows the events on the server's calendar")
    async def show_events(self, ctx):
        if ctx.author == bot.user:
            return
        if not events:
            embed = discord.Embed(title = 'No Events are on ' + ctx.message.guild.name, color = discord.Color(0xFFFF00), timestamp = ctx.message.created_at)
            embed.add_field(name = 'To add events use !addevent and separate name, date, and time using "" ', value = 'Example: !addevent "name" "date" "time(optional)"',inline=False)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/a/a2/Calendar_12.png")
            await ctx.send(embed=embed)
            return
        events.sort(key = lambda x: x[1])
        embed = discord.Embed(title = 'Events on ' + ctx.message.guild.name, color = discord.Color(0xFFFF00), timestamp = ctx.message.created_at)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/a/a2/Calendar_12.png")
        
        # Some events have a time so we first try to add that field in. If an IndexError pops up because event[2] (the time)
        # does not exist, then we make an exception and instead add the name and date only
        for event in events:
            try:
                embed.add_field(name = event[0], value = event[1].strftime('%B %d, %Y') + ' at ' + event[2], inline=False)
            except IndexError:
                embed.add_field(name = event[0], value = event[1].strftime('%B %d, %Y'), inline=False)
        await ctx.send(embed=embed)
        return
    
    @commands.command(aliases=['delevent', 'delete_event', 'delevents'], help = "Deletes an event with the given name or all events")
    async def del_event(self, ctx, name = None):
        if ctx.author == bot.user:
            return
        if not events:
            embed = discord.Embed(title = 'No Events are on ' + ctx.message.guild.name, color = discord.Color(0xFFFF00), timestamp = ctx.message.created_at)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/a/a2/Calendar_12.png")
            await ctx.send(embed=embed)
            return
        if name == None:
            ctx.send('Please redo command with the name of the event you would like to delete')
            return
        if name.lower() == "all":
            events.clear()
            embed = discord.Embed(title = 'All events have been deleted from ' + ctx.message.guild.name, color = discord.Color(0xFFFF00), timestamp = ctx.message.created_at)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/a/a2/Calendar_12.png")
            embed.set_footer(text = ctx.author.display_name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        for event in events:
            if name.lower() == event[0].lower():
                embed = discord.Embed(title = 'Your event has been deleted from ' + ctx.message.guild.name, color = discord.Color(0xFFFF00))
                try:
                    embed.add_field(name = event[0], value = event[1].strftime('%B %d, %Y') + ' at ' + event[2], inline=False)
                except IndexError:
                    embed.add_field(name = event[0], value = event[1].strftime('%B %d, %Y'), inline=False)
                embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/a/a2/Calendar_12.png")
                embed.set_footer(text = ctx.author.display_name, icon_url = ctx.author.avatar_url)
                await ctx.send(embed=embed)
                events.remove(event)
                return
        embed = discord.Embed(title = 'Event is not listed in ' + ctx.message.guild.name, color = discord.Color(0xFFFF00))
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/a/a2/Calendar_12.png")
        await ctx.send(embed=embed)
        return

def setup(bot):
    bot.add_cog(Events(bot))
