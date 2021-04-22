from discord.ext import commands
import datetime as dt
import requests
import json

CALENDAR_LINK_KEY = 'https://calendar.ucf.edu/json/'


class Break(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['nextbreak', 'break'], help="Shows what the next break at UCF is.")
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
        if not response:
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
                await ctx.send((f"The next break is {event['summary']} "
                                f"on {dt.datetime.strftime(start, '%B %-d')}."))
                await ctx.send(event['directUrl'])
                return

        # If there is no break, then this will be communicated to user
        await ctx.send('Unfortunately, there are no more breaks this semester. :(')
        return

    # This command was written by Conroy
    @commands.command(help=("Shows the next upcoming US national holiday "
                            "(of the 10 most common in the US)."))
    async def show_holiday(self, ctx):

        # this dictionary relates a (numerical) month to the next upcoming holiday
        upcoming_holidays = {

            1: "Valentine's Day (February 14th)",
            2: ("Saint Patrick's Day (March 17th) and "
                "Easter (the first Sunday after the first full moon on or after March 21st)"),
            3: "Mother's Day (the second Sunday of May)",
            4: "Mother's Day (the second Sunday of May)",
            5: "Father's Day (the third Sunday of June)",
            6: "Independence Day (July 4th)",
            7: "Halloween (October 31st)",
            8: "Halloween (October 31st)",
            9: "Halloween (October 31st)",
            10: "Thanksgiving (the fourth Thursday of November)",
            11: "Christmas (December 25th)",
            12: "New Years (January 1st)"
        }

        # this dictionary relates a (numerical) month to a holiday inside of that month
        current_holidays = {

            1: "New Years (January 1st)",
            2: "Valentine's Day (February 14th)",
            3: ("Saint Patrick's Day (March 17th) and "
                "Easter (the first Sunday after the first full moon on or after March 21st)"),
            4: "Easter (the first Sunday after the first full moon on or after March 21st)",
            5: "Mother's Day (the second Sunday of May)",
            6: "Father's Day (the third Sunday of June)",
            7: "Independence Day (July 4th)",
            8: "",
            9: "",
            10: "Halloween (October 31st)",
            11: "Thanksgiving (the fourth Thursday of November)",
            12: "Christmas (December 25th)"
        }

        # cM is short for "Current Month"
        cM = dt.date.today().month

        response = f"{upcoming_holidays[cM]} is coming soon!"

        # skip August and September since they do not contain a common holiday
        if cM != 8 and cM != 9:

            response = (f"I hope you did not forget about {current_holidays[cM]}! "
                        f"Also, {upcoming_holidays[cM]} is coming soon.")

        await ctx.send(response)


def setup(bot):
    bot.add_cog(Break(bot))
