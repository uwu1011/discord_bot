import json
import discord
from discord.ext import commands
from core import CogExtension, jdata


class Event(CogExtension):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        g_channel = self.bot.get_channel(int(jdata["general_channel"]))
        await g_channel.send(f"歡迎{member}加入!")

    @commands.Cog.listener()
    async def on_message(self, msg):
        words = ["Never", "gonna", "give", "up"]
        for i in words:
            if msg.content.find(i) >= 0 and msg.author != self.bot.user:
                await msg.channel.send("Never gonna give u up !")


def setup(bot):
    bot.add_cog(Event(bot))
