import discord
from discord.ext import commands
import json 
from core import Cog_Extension

class Main(Cog_Extension):
        
    @commands.command()
    async def Hello(self, ctx):
        await ctx.send("Hello, world")
    
    @commands.command()
    async def Video(self,ctx):
        f = open("data.json")
        data = json.load(f)

        embed=discord.Embed(title="杰哥不要 the 音樂劇", url=data["title"], description="非常好影片", color=0xce1c1c)
        embed.set_author(name="杰哥", url=data["author"], icon_url=data["icon"])
        embed.set_thumbnail(url=data["thumbnail"])
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Main(bot))