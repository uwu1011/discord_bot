import discord
from discord.ext import commands
import json 
from core import Cog_Extension

class Main(Cog_Extension):

    todos = {}
    @commands.command()
    async def Hello(self, ctx):
        await ctx.send("Hello, world")
    
    
    @commands.command()
    async def AddTodoList(self, ctx, item, todos):
        user_id = str(ctx.author.id)
        if user_id not in todos:
            todos[user_id] = []
        todos[user_id].append(item)

    @commands.command()
    async def ListTodoList(self, ctx, todos):
        user_id = str(ctx.author.id)
        if user_id not in todos or not todos[user_id]:
            await ctx.send('You have no tasks in your to-do list.')
        else:
            tasks = '\n'.join(f'{idx + 1}. {task}' for idx, task in enumerate(todos[user_id]))
            await ctx.send(f'Your to-do list:\n{tasks}')
    '''
    TODO
    Add the necessary bot commands here
    Consider using data.json to store some data such as url
    '''

async def setup(bot):
    await bot.add_cog(Main(bot))
