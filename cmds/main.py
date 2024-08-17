import discord
from discord.ext import commands
import json 
from core import Cog_Extension
from function import isDateValid, guess_word
import time
import random
import requests as rq
from bs4 import BeautifulSoup

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

todos = {}
wordle = {}
response = rq.get("https://www.wordunscrambler.net/word-list/wordle-word-list")
raw = response.text
doc = BeautifulSoup(raw, "html.parser")
words = doc.select('h3.list-header + ul a')
word_list = [a.text for a in words]

class Main(Cog_Extension):

    @commands.command()
    async def Hello(self, ctx):
        await ctx.send("Hello, world")
    
    @commands.command()
    async def AddTodoList(self, ctx, item, date):
        user_id = str(ctx.author.id)
        text = ""
        if user_id not in todos:
            todos[user_id] = []
        result = isDateValid(date)
        if result == 1:
            text = 'Please correctly type your date in the format of {YYYY/MM/DD}.'
        elif result == 2:
            text = "Please type a valid month."
        elif result == 3:
            text = "Please type a valid day."
        elif result == 4:
            final = (item, date)
            todos[user_id].append(final)
            text = (f'Successfully added: {item} {date}')
        embed=discord.Embed(title=text, color=0x2effe7)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def ShowTodoList(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in todos or not todos[user_id]:
            embed=discord.Embed(title='You have no tasks in your to-do list.', color=0x2effe7)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            works = todos[user_id]
            works.sort(key=lambda x:int(x[1].replace("/","")))
            embed=discord.Embed(title="Your to-do list:", description="sorted by date", color=0x2effe7)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            for idx, tasks in enumerate(works):
                embed.add_field(name=str(idx + 1) + ". " + tasks[0] + " " + tasks[1], value="", inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    async def ClearTodoList(self, ctx):
        user_id = str(ctx.author.id)
        todos[user_id] = []
        embed=discord.Embed(title="Todo list cleared!", color=0x2effe7)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def RemoveTodoList(self, ctx, item, date):
        user_id = str(ctx.author.id)
        text = ""
        try:
            whole = (item, date)
            todos[user_id].remove(whole)
            text = (f"{item} {date} cleared!")
        except:
            text = (f"Please type in the date or {item} is not in todo list.")
        embed=discord.Embed(title=text, color=0x2effe7)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def Play(self, ctx):
        random.shuffle(word_list)
        word = word_list[0]
        user_id = str(ctx.author.id)
        wordle[user_id] = [word,6]
        print(wordle[user_id])
        embed=discord.Embed(title="Start Playing", color=0x2effe7)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def Ask(self, ctx, guess):
        user_id = str(ctx.author.id)
        guess = guess.lower()
        text = ""
        if user_id not in wordle:
            text = "Please use the \"$Play\" command first."
        else:
            if guess.encode("utf-8").isalpha() == False:
                text = "Please type a valid word."
            elif len(guess) != 5:
                text = "Please type a 5-letter word."
            elif guess not in word_list:
                text = "The word is not in word list."
            else:
                word = wordle[user_id][0]
                wordle[user_id][1] -= 1
                text = guess_word(guess, word)
                if guess == word:
                    del wordle[user_id]
                    text = f"You guessed it right! Congrats! The word was {word}."
                elif wordle[user_id][1] == 0:
                    del wordle[user_id]
                    text = f"You didn't get the word :( The correct word was {word}."
            
        embed=discord.Embed(title=text, color=0x2effe7)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Main(bot))

