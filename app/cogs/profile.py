import discord
from discord.ext import commands


class Profile(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command(name = "av")
  async def getpfp(self, ctx, user: discord.User = None):
    print(user)
    if user == None:
      user = ctx.author
    else:
      user = await self.client.fetch_user(user.id)
      
    title = f"{user}\'s profile picture"
    embed = discord.Embed(
      title = title,
      description = "\ub200",
      colour = discord.Colour.green()
    )
    
  
    embed.set_image(url = user.avatar_url)
    
    await ctx.send(embed = embed)
  

def setup(client):
  client.add_cog(Profile(client))