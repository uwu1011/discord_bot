import discord
from discord.ext import commands
from core import jdata
import json
import os
import youtube_dl

bot = commands.Bot(command_prefix="$")


@bot.event
async def on_ready():
    print(">>Bot is Online<<")


for filename in os.listdir("./cmds"):
    if filename.endswith(".py"):
        bot.load_extension(f"cmds.{filename[:-3]}")


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cmds.{extension}")
    await ctx.send(f"Loaded")


@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f"cmds.{extension}")
    await ctx.send(f"Reloaded")


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cmds.{extension}")
    await ctx.send(f"Unloaded")


if __name__ == "__main__":
    bot.run(jdata["TOKEN"])
