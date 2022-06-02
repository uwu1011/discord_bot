import discord
import json
from discord.ext import commands

class Cog_Extension(commands.Cog):
     def __init__(self,bot):
        self.bot = bot    

f = open("setting.json")
jdata = json.load(f)
f.close 