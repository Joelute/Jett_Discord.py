import discord
from discord.ext import commands
import aiohttp
from datetime import datetime

class Waifu(commands.Cog):

    def __init__(self, client):
        self.client = client
 

    @commands.command(name = "waifu")
    async def roll(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.waifu.pics/sfw/waifu') as response:
                api = await response.json()
                if response.status == 200:
                    url = api["url"]
                else:
                    pass

        embed = discord.Embed(
            title = " ",
            description  = "Here is your waifu",
            colour = discord.Color.green(),
            timestamp = datetime.utcnow()
        )
        embed.set_image(url = url)
        await ctx.send(embed = embed)
  
  

def setup(client):
  client.add_cog(Waifu(client))