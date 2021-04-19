import discord
from discord.ext import commands
import datetime as dt
import requests
import json

CALENDAR_LINK_KEY = 'https://calendar.ucf.edu/json/'

class Break(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['nextbreak', 'break'], help = "Shows what the next break at UCF is.")
    async def show_break(self, ctx):
        link = CALENDAR_LINK_KEY
        no_classes = []

        # Get current date, construct calendar link
        today = dt.datetime.now()
        month = today.month
        year = today.year

        link += str(year) + '/'
        if (month < 5):
            link += 'spring'
        elif (month < 8):
            link += 'summer'
        else:
            link += 'fall'

        # Request information from json
        response = requests.get(link)
        if response == False:
            print('404 Not Found Error')
            return

        # Sift through to get the list of events
        file = json.loads(response.text)
        try:
            events = file['terms'][0]['events']
        except IndexError:
            print('Looks like they may have reorganized the UCF Calendar JSON')
            return

        # Find all events tagged with 'no-classes'
        for event in events:
            if event['tags']:
                for tag in event["tags"]:
                    if tag == 'no-classes':
                        no_classes.append(event)

        # find first date after current date tagged with 'no-classes'
        for event in no_classes:
            start = dt.datetime.strptime(event['dtstart'], '%Y-%m-%d %H:%M:%SZ')
            if (event['dtend']):
                end = dt.datetime.strptime(event['dtend'], '%Y-%m-%d %H:%M:%SZ')
            else:
                end = today

            # Show the user when the break will end or when the next break will be
            if start.date() == today.date():
                await ctx.send(f"Today is {event['summary']}. There are no classes today.")
                await ctx.send(event['directUrl'])
                return
            elif end > today:
                await ctx.send('You are currently on break!')
                await ctx.send(f"{event['summary']} ends on {dt.datetime.strftime(end, '%B %-d')}.")
                await ctx.send(event['directUrl'])
                return
            elif start > today:
                await ctx.send(f"The next break is {event['summary']} on {dt.datetime.strftime(start, '%B %-d')}.")
                await ctx.send(event['directUrl'])
                return


        # If there is no break, then this will be communicated to user
        await ctx.send('Unfortunately, there are no more breaks this semester. :(')
        return

def setup(bot):
    bot.add_cog(Break(bot))
