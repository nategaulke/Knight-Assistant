import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import builtins

bot = commands.Bot(command_prefix='!')
builtins.bot = bot

load_dotenv()
TOKEN = os.getenv('TOKEN')

"""
The below function is a model for how we should define all command functions. Use the "help" decorator and put a description of the command there.
Whenever a user types "!help", a list of all command descriptions will show.
~Conroy
"""
@bot.command(help = "This command is an example of how to contribute information to the \"!help\" command.")
async def model_command(ctx):
    await ctx.channel.send("placeholder.")

@bot.event
async def on_ready():
    print(f"{bot.user.name} has entered the Bounce House!")

bot.run(TOKEN)
