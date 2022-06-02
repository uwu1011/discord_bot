import discord
from discord.ext import commands
from core import Cog_Extension,jdata
import json
import requests
from bs4 import BeautifulSoup

class Main(Cog_Extension):

    @commands.command()
    async def Hello(self, ctx):
        await ctx.send("Hello, world")
    
    @commands.command()
    async def Video(self,ctx):
        embed=discord.Embed(title="杰哥不要 the 音樂劇", url=jdata["title"], description="非常好影片", color=0xce1c1c)
        embed.set_author(name="杰哥", url=jdata["author"], icon_url=jdata["icon"])
        embed.set_thumbnail(url=jdata["thumbnail"])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Main(bot))