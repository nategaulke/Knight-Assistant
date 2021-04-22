import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Script by Christine Stevens

# Change DATABASE and COLLECTION to your Cluster and Database names
load_dotenv()
MONGO_URL = os.getenv('MONGO_URL')
DATABASE = "Database"
COLLECTION = "Tasks"


class Tasks(commands.Cog):

    # Sets Up Bot
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    # Add Task
    @commands.command(help="Adds a task. Please type a title and description surrounded by quotes.",
                      aliases=["addtask", 'addt'])
    async def add_task(self, ctx, arg1=None, arg2=None):

        # Grabs database information
        client = MongoClient(MONGO_URL)
        db = client[DATABASE]
        collection = db[COLLECTION]

        # Check that user wrote a task
        if arg1 is None:

            await ctx.send(('Please redo command with this format: !add_task '
                            '"TaskTitle" "TaskDescription" (quotes included).'))
            return

        # Create Task for the Database
        task = {'Title': arg1, 'Desc': arg2, 'checked': False,
                'UserID': ctx.author.display_name, 'Guild': ctx.message.guild.name}

        # Fill out Discord Embeded Message
        embedVar = discord.Embed(title="Your task has been added.", color=0x00ff00)
        embedVar.set_thumbnail(url=("https://publicdomainvectors.org/"
                                    "photos/sheikh_tuhin_To-Do_List.png"))
        embedVar.add_field(name=task["Title"], value=task["Desc"], inline=False)

        # Add task to database
        collection.insert_one(task)

        # Send Confirmation Message
        await ctx.channel.send(embed=embedVar)

    # Edit Task
    @commands.command(help="Edits a task. 'TitleYouWantToChange' 'NewTitle' 'NewDescription'",
                      aliases=["edittask", 'editt'])
    async def edit_task(self, ctx, arg1=None, arg2=None, arg3=None):

        # Grabs Database Information
        client = MongoClient(MONGO_URL)
        db = client[DATABASE]
        collection = db[COLLECTION]

        # Check if user filled out the forms
        if arg1 is None:
            await ctx.send(('Please redo command with this format: !edit_task '
                            '"TitleYouWantToChange" "NewTaskTitle" '
                            '"NewTaskDescription" (quotes included).'))
            return

        # Make sure task user wants to edit exists in the server they are using the bot in.
        if (collection.find({"$and": [{'Guild': ctx.message.guild.name},
                            {"Title": arg1}]}).count() == 0):
            await ctx.send("The task you are trying to edit does not exist.")
            return

        # Update the task with new information
        collection.update_one({"Title": arg1}, {"$set": {"Title": arg2, "Desc": arg3}})

        # Create embeded confirmation message and send through Discord
        embedVar = discord.Embed(title="Your task has been edited.", color=0x00ff00)
        embedVar.set_thumbnail(url=("https://publicdomainvectors.org/"
                                    "photos/sheikh_tuhin_To-Do_List.png"))
        embedVar.add_field(name=arg2, value=arg3, inline=False)
        await ctx.channel.send(embed=embedVar)

    # Delete Task
    @commands.command(help=("Deletes a task. "
                            "Write the Title of the task you wish to delete in quotes."),
                      aliases=["deltask", "delt", "deletet", "deletetask"])
    async def del_task(self, ctx, arg1=None):

        # Grab information from Database
        client = MongoClient(MONGO_URL)
        db = client[DATABASE]
        collection = db[COLLECTION]

        # Make Sure user specified title to delete
        if arg1 is None:
            await ctx.send(('Please redo command with this format: !del_task '
                            '"Title of Task You Wish to Delete" (Quotes included).'))
            return

        # Make sure the task the user wants to delete exists in the server they are using the bot in
        if (collection.find({'Guild': ctx.message.guild.name}, {"Title": arg1}).count() == 0):
            await ctx.send("The task you are trying to edit does not exist.")
            return

        # Grab information from the database for the confirmation message
        task = collection.find_one({"Title": arg1})

        # Create the embedded message and send
        embedVar = discord.Embed(title="Your task has been deleted.", color=0x00ff00)
        embedVar.set_thumbnail(url=("https://publicdomainvectors.org/"
                                    "photos/sheikh_tuhin_To-Do_List.png"))
        embedVar.add_field(name=task["Title"], value=task["Desc"], inline=False)

        await ctx.channel.send(embed=embedVar)

        # Delete from the database
        collection.delete_one({"Title": arg1})

    # Check Off Task
    @commands.command(help=("Checks off a task. "
                            "Write the Title of the task you wish to check off in quotes."),
                      aliases=["checktask", "checkt"])
    async def check_task(self, ctx, arg1=None):

        # Grab information from Database
        client = MongoClient(MONGO_URL)
        db = client[DATABASE]
        collection = db[COLLECTION]

        # Make Sure User wrote a title
        if arg1 is None:
            await ctx.send(('Please redo command with this format: !check_task '
                            '"Title of Task You Wish to Check off" (Quotes included).'))
            return

        # Make sure task that user wants to check off exists in the server
        if (collection.find({"$and": [{'Guild': ctx.message.guild.name},
                            {"Title": arg1}]}).count() == 0):
            await ctx.send("The task you are trying to edit does not exist.")
            return
        # Grab task from database
        task = collection.find_one({"Title": arg1})

        # Make sure it hasn't already been checked off
        if task["checked"]:
            await ctx.send("This task has already been checked off.")
            return
        # If not checked off, mark it as checked
        collection.update_one({"Title": arg1}, {"$set": {"checked": True}})

        # This is necessary for the description, makes sure it isn't None.
        desc = task["Desc"]

        if desc is not None:
            desc = "~~"+task["Desc"]+"~~"

        # Create Message for Discord and Send with crossed off formatting
        embedVar = discord.Embed(title="Your task has been checked off.", color=0x00ff00)
        embedVar.set_thumbnail(url=("https://publicdomainvectors.org/"
                                    "photos/sheikh_tuhin_To-Do_List.png"))
        embedVar.add_field(name=("~~"+task["Title"]+"~~"), value=(desc), inline=False)
        await ctx.channel.send(embed=embedVar)

    # Uncheck task
    @commands.command(help=("Unchecks a task. "
                            "Write the Title of the task you wish to uncheck in quotes."),
                      aliases=["unchecktask", "uncheckt"])
    async def uncheck_task(self, ctx, arg1=None):

        # Grab information from Database
        client = MongoClient(MONGO_URL)
        db = client[DATABASE]
        collection = db[COLLECTION]

        # Make sure user wrote a title
        if arg1 is None:
            await ctx.send(('Please redo command with this format: !uncheck_task '
                            '"Title of Task You Wish to Uncheck" (Quotes included).'))
            return

        # Make sure the task exists in the server
        if (collection.find({"$and": [{'Guild': ctx.message.guild.name},
                            {"Title": arg1}]}).count() == 0):
            await ctx.send("The task you are trying to edit does not exist.")
            return

        # Grab the task from the database
        task = collection.find_one({"Title": arg1})

        # Make sure it has already been checked off
        if not task["checked"]:
            await ctx.send("This task has not been checked off.")
            return

        # Update task in database
        collection.update_one({"Title": arg1}, {"$set": {"checked": False}})

        # Create confirmation message and send
        embedVar = discord.Embed(title="Your task has been checked off.", color=0x00ff00)
        embedVar.set_thumbnail(url=("https://publicdomainvectors.org/"
                                    "photos/sheikh_tuhin_To-Do_List.png"))
        embedVar.add_field(name=(task["Title"]), value=(task["Desc"]), inline=False)
        await ctx.channel.send(embed=embedVar)

    # Show Tasks
    @commands.command(help="Shows all of your tasks.", aliases=["showtasks", "showt"])
    async def show_tasks(self, ctx):

        # Grab database
        client = MongoClient(MONGO_URL)
        db = client[DATABASE]
        collection = db[COLLECTION]

        # Check if there are any tasks in the database
        if collection.find({'Guild': ctx.message.guild.name}).count() == 0:
            embedVar = discord.Embed(title="You have no tasks.", color=0x00ff00)
        else:
            embedVar = discord.Embed(title="Here are all of your tasks", color=0x00ff00)

        # Grab the collection of tasks
        tasks = collection.find({'Guild': ctx.message.guild.name})
        embedVar.set_thumbnail(url=("https://publicdomainvectors.org/"
                                    "photos/sheikh_tuhin_To-Do_List.png"))

        # For each task, check if its checked off and add field to embedded message
        for task in tasks:

            if task["checked"]:
                desc = task["Desc"]

                if desc is not None:
                    desc = "~~"+task["Desc"]+"~~"
                embedVar.add_field(name=("~~"+task["Title"]+"~~"), value=desc, inline=False)
            else:
                embedVar.add_field(name=task["Title"], value=task["Desc"], inline=False)
        # Send the list of tasks
        await ctx.channel.send(embed=embedVar)


# Adds cog to bot
def setup(bot):
    bot.add_cog(Tasks(bot))
