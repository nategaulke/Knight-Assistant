import discord
from discord.ext import commands
import datetime as dt

class add_event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['addevent'])
    async def add_event(self, ctx, name = None, date = None, time = None):
        if ctx.author == bot.user:
            return
        if name == None:
            await ctx.send('Please redo command with the name of your event and the date')
            return
        if date == None:
            await ctx.send('Did you mean to add a reminder instead? Otherwise please redo command with a date')
            return
        if time == None:
            date = dt.datetime.strptime(date, '%B %d, %Y')
            date_string = date.strftime('%B %d, %Y')
            await ctx.send('Your event "' + name + '" has been added on ' + date_string)
        return

def setup(bot):
    bot.add_cog(add_event(bot))
