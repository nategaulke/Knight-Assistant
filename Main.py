import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import builtins

bot = commands.Bot(command_prefix='!')
builtins.bot = bot

load_dotenv()
TOKEN = os.getenv('TOKEN')

@bot.event
async def on_ready():
    print(f"{bot.user.name} has entered the Bounce House!")

bot.run(TOKEN)
