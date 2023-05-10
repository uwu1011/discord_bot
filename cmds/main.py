import discord
from discord.ext import commands
import json 
from core import Cog_Extension

class Main(Cog_Extension):
        
    @commands.command()
    async def Hello(self, ctx):
        await ctx.send("Hello, world")
    
    '''
    TODO
    Add the necessary bot commands here
    Consider using data.json to store some data such as url
    '''

async def setup(bot):
    await bot.add_cog(Main(bot))