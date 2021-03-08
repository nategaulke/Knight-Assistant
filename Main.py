import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import builtins

bot = commands.Bot(command_prefix='!')
builtins.bot = bot

load_dotenv()
TOKEN = os.getenv('TOKEN')

@bot.command(help = "This command will load a cog. Type the cog's name after the command.")
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command(help = "This command will unload a cog. Type the cog's name after the command.")
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

@bot.command(help = "This command will reload a cog. Type the cog's name after the command.")
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

#this for loop will load all cogs as soon as the bot starts running
#loop through all files in the cogs folder
for filename in os.listdir("./cogs"):

    #check for a python file
    if filename.endswith(".py"):

        #load the python file as a cog (be sure to splice the file name in order to not inlcude ".py")
        bot.load_extension("cogs." + filename[:-3])


@bot.event
async def on_ready():
    print(f"{bot.user.name} has entered the Bounce House!")

bot.run(TOKEN)
