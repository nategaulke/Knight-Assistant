import discord
import os 
from discord.ext import commands

tasklist = []  

class tasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    @commands.command(help="Adds a Task")
    async def add_task(self, ctx, arg1, arg2):


        if arg1 == None:
            await ctx.send('Please redo command with the name of your task.')
            return 
        
        tasks = [arg1, arg2]
        tasklist.append(tasks)
        embedVar = discord.Embed(title="Your task has been added.", color=0x00ff00)
        embedVar.add_field(name= tasks[0], value=tasks[1], inline=False)
        await ctx.channel.send(embed=embedVar)
    
    @commands.command(help="Shows all of your tasks")
    async def show_tasks(self, ctx):

      if len(tasklist) == 0:   
        embedVar = discord.Embed(title="You have no tasks.", color=0x00ff00)
      else: 
        embedVar = discord.Embed(title="Here are all of your tasks", color=0x00ff00)

      for i in range (0, len(tasklist)):

        taskTitle = str(i+1) + ". " + tasklist[i][0]
        embedVar.add_field(name=taskTitle, value=tasklist[i][1], inline=False)
        

      await ctx.channel.send(embed=embedVar)

    @commands.command(help="Deletes a task")
    async def del_task(self, ctx, arg:int):

      if arg <= len(tasklist): 
        task = tasklist[(arg-1)]
        embedVar = discord.Embed(title="Your task has been deleted.", color=0x00ff00)
        embedVar.add_field(name= task[0], value=task[1], inline=False)
        await ctx.channel.send(embed=embedVar)
        del tasklist[(arg-1)]
      

      else:
         await ctx.channel.send("There's something wrong.\n Please make sure that you are deleting a task that exists. \n Please try again using !del_task <integer>")

def setup(bot):
    bot.add_cog(tasks(bot))