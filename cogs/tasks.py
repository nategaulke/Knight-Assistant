import discord
import os 
from discord.ext import commands

tasklist = []  

class tasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    @commands.command(help="Adds a Task", aliases = ["addtask", 'addt'] )
    async def add_task(self, ctx, arg1 = None, arg2 = None):


        if arg1 == None:
            await ctx.send('Please redo command with this format: !add_task "TaskTitle" "TaskDescription" (quotes included).')
            return 
        
        tasks = [arg1, arg2]
        tasklist.append(tasks)
        embedVar = discord.Embed(title="Your task has been added.", color=0x00ff00)
        embedVar.add_field(name= tasks[0], value=tasks[1], inline=False)
        await ctx.channel.send(embed=embedVar)

    @commands.command(help="Adds a Task", aliases = ["edittask", 'editt'] )
    async def edit_task(self, ctx, arg: int, arg1 = None, arg2 = None):


        if arg1 == None:
            await ctx.send('Please redo command with this format: !edit_task <integer> "TaskTitle" "TaskDescription" (quotes included).')
            return 
        
        tasks = [arg1, arg2]
        tasklist[arg-1] = tasks
        embedVar = discord.Embed(title="Your task has been edited.", color=0x00ff00)
        embedVar.add_field(name= tasks[0], value=tasks[1], inline=False)
        await ctx.channel.send(embed=embedVar)


    @commands.command(help="Shows all of your tasks", aliases = ["showtasks", "showt"])
    async def show_tasks(self, ctx):

      if len(tasklist) == 0:   
        embedVar = discord.Embed(title="You have no tasks.", color=0x00ff00)
      else: 
        embedVar = discord.Embed(title="Here are all of your tasks", color=0x00ff00)

      for i in range (0, len(tasklist)):

        taskTitle = str(i+1) + ". " + tasklist[i][0]
        embedVar.add_field(name=taskTitle, value=tasklist[i][1], inline=False)
        

      await ctx.channel.send(embed=embedVar)

    @commands.command(help="Checks off a task", aliases = ["checktask", "checkt"])
    async def check_task(self, ctx, arg: int):

      if arg <= len(tasklist): 

        if tasklist[arg-1][0][0] == "~":
          await ctx.channel.send("This task has already been checked off.")
          return

        else: 
          task = tasklist[(arg-1)]
          tasklist[arg-1][0] = "~~"+task[0]+"~~"

          if tasklist[arg-1][1] != None:
            tasklist[arg-1][1] = "~~"+task[1]+"~~"
          embedVar = discord.Embed(title="Your task has been checked off.", color=0x00ff00)
          embedVar.add_field(name= task[0], value=task[1], inline=False)
          await ctx.channel.send(embed=embedVar)     

      else:
        await ctx.channel.send("There's something wrong.\n Please make sure that you are checking off a task that exists. \n Please try again using !checkoff_task <integer>")
      

    @commands.command(help="Unchecks a task", aliases = ["unchecktask", "uncheckt"])
    async def uncheck_task(self, ctx, arg: int):
      
      if arg <= len(tasklist): 
        task = tasklist[(arg-1)]

        if tasklist[arg-1][0][0] != "~":
          await ctx.channel.send("This task hasn't been checked off.")
        else:
          tasklist[arg-1][0] = tasklist[arg-1][0][2:(len(tasklist[arg-1][0])-2)]
          if tasklist[arg-1][1] != None:
            tasklist[arg-1][1] = tasklist[arg-1][1][2:(len(tasklist[arg-1][1])-2)]  
          
          embedVar = discord.Embed(title="Your task has been unchecked.", color=0x00ff00)
          embedVar.add_field(name= task[0], value=task[1], inline=False)
          await ctx.channel.send(embed=embedVar)     

      else:
        await ctx.channel.send("There's something wrong.\n Please make sure that you are checking off a task that exists. \n Please try again using !checkoff_task <integer>")
      

    @commands.command(help="Deletes a task", aliases = ["deltask", "delt", "deletet", "deletetask"])
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