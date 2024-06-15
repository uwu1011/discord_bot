import discord
from discord.ext import commands
import json 
from core import Cog_Extension
from function import isDateValid
import time
import random
import requests as rq
from bs4 import BeautifulSoup

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

todos = {}
response = rq.get("https://www.wordunscrambler.net/word-list/wordle-word-list")
raw = response.text
doc = BeautifulSoup(raw, "html.parser")
words = doc.select('h3.list-header + ul a')
word_list = [a.text for a in words]

class Main(Cog_Extension):

    todos = {}
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
        await ctx.send(word_list[0])
        
        
        
        
    '''
    TODO
    Add the necessary bot commands here
    Consider using data.json to store some data such as url
    '''

    @commands.command()
    async def nba(self, ctx):
        await ctx.send("今天需要什麼關於nba的資訊?")

    @commands.command()
    async def cominggames(self, ctx):
        url = "https://www.nba.com/schedule"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the section containing the games
        games_section = soup.find_all("div", class_="ScheduleDay_gameWrapper__FnoN3")

        if not games_section:
            await ctx.send("找不到比賽資訊。")
            return

        games_info = []
        count = 0
        for day in games_section:
            games = day.find_all("div", class_="Card_gameCard__nlHpI")
            for game in games:
                if count >= 5:
                    break
                teams = game.find_all("span", class_="MatchupCard_teamName__Z6ADd")
                time = game.find("span", class_="MatchupCard_gameTime__jbFiL")
                if teams and time:
                    team1 = teams[0].text.strip()
                    team2 = teams[1].text.strip()
                    game_time = time.text.strip()
                    games_info.append(f"{team1} vs {team2} at {game_time}")
                    count += 1
            if count >= 5:
                break

        await ctx.send("\n".join(games_info))

    @commands.command()
    async def news(self, ctx):
        url = "https://www.nba.com/news"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        news_section = soup.find_all("div", class_="ArticleCard_articleCard__hCOE6")
        
        if not news_section:
            await ctx.send("找不到新聞資訊。")
            return

        news_info = []
        for news in news_section[:5]:
            title = news.find("h2", class_="ArticleCard_title__ZnK9q").text.strip()
            link = news.find("a", href=True)["href"]
            news_info.append(f"{title} - https://www.nba.com{link}")

        await ctx.send("\n".join(news_info))

    @commands.command()
    async def stats(self, ctx):
        url = "https://www.nba.com/stats"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        categories = ["points", "rebounds", "assists", "steals", "blocks"]
        stats_info = []

        for category in categories:
            section = soup.find("a", href=f"/stats/players/{category}/")
            if section:
                leader = section.find("p", class_="LeaderBoardPlayer_playerName__kB48U").text.strip()
                value = section.find("p", class_="LeaderBoardPlayer_playerValue__ZW09H").text.strip()
                stats_info.append(f"{category.capitalize()}: {leader} - {value}")

        if not stats_info:
            await ctx.send("找不到統計數據。")
            return

        await ctx.send("\n".join(stats_info))

async def setup(bot):
    await bot.add_cog(Main(bot))

