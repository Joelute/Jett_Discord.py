import discord
from discord.ext import commands


class profile(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command(name = "av")
  async def getpfp(self, ctx, *user: discord.User):
    if not user:
      user = ctx.author
    
    embed = discord.Embed(
      title = f"{user}\'s profile picture",
      description = "\ub200",
      colour = discord.Colour.green()
    )
    
    embed.set_image(url = user.avatar_url)
    await ctx.send(embed = embed)
  

def setup(client):
  client.add_cog(profile(client))