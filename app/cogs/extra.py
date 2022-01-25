from discord.ext import commands
import random
import requests
import json

class Extra(commands.Cog):

  def __init__(self, client):
    self.client = client

  
 

  @commands.command(name= "stw")
  async def stw(self, ctx):
    await ctx.send("https://fortnitedb.com/")


#--------------------------------------------------------------------------------------


  @commands.command(name="Jett")
  async def AddJett(self, ctx):
    await ctx.send("Like the Jett bot? Get it in your server now! http://bit.ly/JettDiscord")


#--------------------------------------------------------------------------------------


  @commands.command(name="animeq")
  async def get_anime_quote(self, ctx):
    response = requests.get("https://animechan.vercel.app/api/random")
    json_data = json.loads(response.text)
    quote = str(json_data["quote"]) + " -" + str(json_data["character"]) + " from " + str(json_data["anime"])
    await ctx.send(quote)


#--------------------------------------------------------------------------------------


  @commands.command(name="quote")
  async def get_quote(self, ctx):
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0] ["q"] + " -" + json_data[0] ["a"]
    await ctx.send(quote)


#--------------------------------------------------------------------------------------


  @commands.command(name="roll")
  async def roll(self, ctx, number_of_side: int = 6):
    dice = str(random.choice(range(1, number_of_side + 1)))
    dices = await ctx.send(f"You rolled a {dice}! 🎲")
    await dices.add_reaction("🎲")
    def check(reaction,user):
      return user == ctx.author and str(reaction.emoji) in ("🎲")
    reaction, user = await self.client.wait_for("reaction_add", timeout = 30.0 , check = check)

    await self.roll(ctx, number_of_side)
  
  

def setup(client):
  client.add_cog(Extra(client))