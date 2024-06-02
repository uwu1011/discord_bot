import discord
from discord.ext import commands
import json 
from core import Cog_Extension
from function import isDateValid

import requests
from bs4 import BeautifulSoup


todos = {}
class Main(Cog_Extension):

    todos = {}
    @commands.command()
    async def Hello(self, ctx):
        await ctx.send("Hello, world")
    
    
    @commands.command()
    async def AddTodoList(self, ctx, item, date):
        user_id = str(ctx.author.id)
        if user_id not in todos:
            todos[user_id] = []
        result = isDateValid(date)
        if result == 1:
            await ctx.send('Please correctly type your date in the format of {YYYY/MM/DD}.')
        elif result == 2:
            await ctx.send('Please type a valid month.')
        elif result == 3:
            await ctx.send('Please type a valid day.')
        elif result == 4:
            todos[user_id].append(item)
            await ctx.send(f'Successfully added: {item} {date}')

    @commands.command()
    async def ShowTodoList(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in todos or not todos[user_id]:
            await ctx.send('You have no tasks in your to-do list.')
        else:
            tasks = '\n'.join(f'{idx + 1}. {task}' for idx, task in enumerate(todos[user_id]))
            await ctx.send(f'Your to-do list:\n{tasks}')

    @commands.command()
    async def ClearTodoList(self, ctx):
        user_id = str(ctx.author.id)
        todos[user_id] = []
        await ctx.send("Todo list cleared!")

    @commands.command()
    async def RemoveTodoList(self, ctx, item):
        user_id = str(ctx.author.id)
        try:
            todos[user_id].remove(item)
            await ctx.send(f"{item} cleared!")
        except:
            await ctx.send(f"{item} is not in todo list.")
        
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

