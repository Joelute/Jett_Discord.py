import aiohttp
import discord
import math
import os
from discord.ext import commands, tasks 
from datetime import datetime

class Valorantlb(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

    self.leaderboard = {}

    self.emojis = ["🔼", "🔽"]

    self.data_cache = {}

    self.resetCache.start()

    self.riot_key = os.getenv("riot_key")

  @tasks.loop(minutes = 1)
  async def resetCache(self):
    self.data_cache = await self.getRequest()

  async def getRequest(self):
    async with aiohttp.ClientSession() as session:
      async with session.get(f'https://na.api.riotgames.com/val/ranked/v1/leaderboards/by-act/2a27e5d2-4d30-c9e2-b15a-93b8909a442c?size=200&startIndex=0&api_key={self.riot_key}') as resp:
        response = await resp.json(content_type=None)

        if response:
          return response

        return None


  @commands.command(name = "lb")
  async def leaderboardf(self,ctx):
    if not self.data_cache:
      embed = discord.embed(title = "API Responded Unexpectedly")
      return await ctx.send(embed=embed)

    pages = math.ceil(len(self.data_cache["players"])/10)

    if pages > 0:
      pages -= 1

    self.leaderboard[ctx.author.id] = {"Message": None, "Page": 0, "Pages": pages}
    self.leaderboard[ctx.author.id]["Message"] = await ctx.send(embed=await self.leaderboardEmbed(ctx.author))

    if pages > 0:
      for emoji in self.emojis:
        await self.leaderboard[ctx.author.id]["Message"].add_reaction(emoji)

  async def leaderboardEmbed(self, user):
    rankList, ratingList, numofWins = [], [], []
    start_at = self.leaderboard[user.id]["Page"] * 10
    counter = 0
    end_at = start_at + 10
  
    for i in self.data_cache["players"]:
      if counter >= start_at:
        try:
          rankList.append(str(i["leaderboardRank"])+ ". " + str(i["gameName"]))
        except:
          rankList.append(str(i["leaderboardRank"])+ ". Anonymous")

        ratingList.append(">  " + str(i["rankedRating"])+"RR")

        numofWins.append(">  " + str(i["numberOfWins"])+" GAMES WON")

      counter += 1

      if counter == end_at:
        break
    
    embed=discord.Embed(title="Valorant Leaderboard",url="https://playvalorant.com/en-us/leaderboards/", description="Showing Valorant Leaderboard for the current season", color=0xe70d0d, timestamp = datetime.utcnow())
    
    embed.add_field(name="RANK", value="\n".join(rankList), inline=True)
    embed.add_field(name="RATING", value="\n".join(ratingList), inline=True)
    embed.add_field(name="ONGOING", value="\n".join(numofWins), inline = True)

    embed.set_footer(text=f"Last Update: ")

    return embed


  @commands.Cog.listener()
  async def on_reaction_add(self, reaction, user):
    if user.id not in self.leaderboard:
      return
    if reaction.message.id != self.leaderboard[user.id]["Message"].id:
      return

    await reaction.remove(user)

    if str(reaction.emoji) == "🔽":
      if self.leaderboard[user.id]["Page"] >= self.leaderboard[user.id]["Pages"]:
        return
    
      self.leaderboard[user.id]["Page"] += 1
      await self.leaderboard[user.id]["Message"].edit(embed=await self.leaderboardEmbed(user))

    if str(reaction.emoji) == "🔼":
      if self.leaderboard[user.id]["Page"] <= 0:
        return
    
      self.leaderboard[user.id]["Page"] -= 1
      await self.leaderboard[user.id]["Message"].edit(embed=await self.leaderboardEmbed(user))

    
def setup(bot):
  bot.add_cog(Valorantlb(bot))