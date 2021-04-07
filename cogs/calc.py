#This script was written by Conroy

import discord
from discord.ext import commands

#inherit from commands.Cog
class Calc(commands.Cog):

    def __init__(self, bot):

        #reference the bot object from Main.py
        self.bot = bot


    @commands.command(help = "This command will do simple math. Type a simple math expression with only 1 operator after \"!calc\" and the bot will solve it for you!")
    async def calc(self, ctx, x, operator, y):

        channel = ctx.message.channel
        tempx = float(x)
        tempy = float(y)
        response = ""

        #check for all basic math calculations
        if operator == "+" or operator.lower() == "plus":

            response = f"The answer is {(tempx + tempy)}."

        elif operator == "-" or operator.lower() == "minus":

            response = f"The answer is {(tempx - tempy)}."

        elif operator == "/" or operator.lower() == "divide":

            response = f"The answer is {(tempx / tempy)}."

        elif operator == "*" or operator.lower() == "multiply":

            response = f"The answer is {(tempx * tempy)}."

        elif operator == "%" or operator.lower() == "mod" or operator.lower() == "modulo" or operator.lower() == "modulos":

            response = f"The answer is {(tempx % tempy)}."

        elif operator == "^" or operator.lower() == "power":

            response = f"The answer is {(tempx ** tempy)}."

        else:

            response = "Sorry, I do not recognize that oeprator yet."
        
        await channel.send(response)
    
    @commands.command(help = "This command will ")
    async def calc_tip(self, ctx, amount):

        channel = ctx.message.channel 

        standard_tip = amount * .20

        response = f"You should give a ${standard_tip} tip"

        await channel.send(response)

#this function connects this cog (via the Calc class) to the bot object
def setup(bot):
    bot.add_cog(Calc(bot))