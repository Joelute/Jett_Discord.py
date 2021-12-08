import discord
from discord.ext import commands
import random
import discord_components
from discord_components import Button, ButtonStyle

class Rps(commands.Cog):

  def __init__(self, client):
    self.client = client

    self.sessions = {}

  def choice_generator(self):

    comp = random.randint(1,3)

    if comp == 1:
      comp_choice = "Rock"
      types = "✊"
    if comp == 2:
      comp_choice = "Paper"
      types = "✋"
    if comp == 3:
      comp_choice = "Scissors"
      types = "✌"
    
    return comp_choice, types


  def result(self, user, comp_choice):
    user_choice = self.sessions[user.id]["Player_choice"]
    if user_choice == comp_choice:
      return ("It's a tie! Both chose {}".format(user_choice)), "tie"

    elif user_choice == "Scissors" and comp_choice == "Paper":
      return(f"{user} won! Good job! 🍬"), "win"
    elif user_choice == "Paper" and comp_choice == "Rock":
      return(f"{user} won! Good job! 🍬"), "win"
    elif user_choice == "Rock" and comp_choice == "Scissors":
      return(f"{user} won! Good job! 🍬"), "win"
    else:
      return (f"{user} lost... Try again!"), "lose"


  @commands.command(name = "rps", help = "Rock Paper Scissors!")
  async def rps(self, ctx):
    
    self.sessions[ctx.author.id] = {"Message": None , "Player_choice": None, "Player_type": None}
    self.sessions[ctx.author.id]["Message"] = await ctx.send(embed = await self.rpsembed(ctx.author), components = 
    [[
      Button(style = ButtonStyle.blue, label = "✊", custom_id="rock"),
      Button(style = ButtonStyle.blue, label = "✋", custom_id = "paper"), 
      Button(style = ButtonStyle.blue, label = "✌", custom_id = "scissors")
    ]])
  

  async def rpsembed(self, user):

    if self.sessions[user.id]["Player_choice"] == None:

      embed = discord.Embed(
        title = "Rock, Paper, Scissors!",
        description = "React with a emoji to play!",
        colour = discord.Colour.light_grey()
      )
      
      embed.set_footer(text = f"Invoked by {user}")
      embed.set_thumbnail(url = user.avatar_url)

      return embed

    elif self.sessions[user.id]["Player_choice"] != None:
      comp_choice, types = self.choice_generator()
      message, condition = self.result(user, comp_choice)
      if condition == "win":
        embed = discord.Embed(
          title = "rock, paper, scissors!",
          description = "React with a emoji to play!",
          colour = discord.Colour.green()
        )
        embed.add_field(name = "You:", value = self.sessions[user.id]["Player_type"],inline = True)
        embed.add_field(name = "\u200b", value = "vs", inline = True)
        embed.add_field(name = "Jett:", value = f"{types}", inline = True)
        embed.add_field (name = message, value = "\u200b", inline = False)

      elif condition == "lose":
        embed = discord.Embed(
          title = "rock, paper, scissors!",
          description = "React with a emoji to play!",
          colour = discord.Colour.red()
        )
        embed.add_field(name = "You:", value = self.sessions[user.id]["Player_type"],inline = True)
        embed.add_field(name = "\u200b", value = "vs", inline = True)
        embed.add_field(name = "Jett:", value = f"{types}", inline = True)
        embed.add_field (name = message, value = "\u200b", inline = False)

      elif condition == "tie":
        embed = discord.Embed(
          title = "rock, paper, scissors!",
          description = "React with a emoji to play!",
          colour = discord.Colour.gold()
        )
        embed.add_field(name = "You:", value = self.sessions[user.id]["Player_type"],inline = True)
        embed.add_field(name = "\u200b", value = "vs", inline = True)
        embed.add_field(name = "Jett:", value = f"{types}", inline = True)
        embed.add_field (name = message, value = "\u200b", inline = False)

      embed.set_footer(text = f"Invoked by {user}")
      embed.set_thumbnail(url = user.avatar_url)

      return embed
      

  @commands.Cog.listener(name='on_button_click')
  async def on_button_click(self, interaction):
    try:
      if interaction.user.id not in self.sessions:
        return await interaction.respond(type=6)
        
      if interaction.component.id == 'rock':
        self.sessions[interaction.user.id]["Player_choice"] = "Rock"
        self.sessions[interaction.user.id]["Player_type"] = "✊"
        await self.sessions[interaction.user.id]["Message"].edit(embed = await self.rpsembed(interaction.user), components = [])
        self.sessions[interaction.user.id] = {}
        return await interaction.respond(type=6)

      elif interaction.component.id == 'paper':
        self.sessions[interaction.user.id]["Player_choice"] = "Paper"
        self.sessions[interaction.user.id]["Player_type"] = "✋"
        await self.sessions[interaction.user.id]["Message"].edit(embed = await self.rpsembed(interaction.user), components = [])
        self.sessions[interaction.user.id] = {}
        return await interaction.respond(type=6)

      elif interaction.component.id == 'scissors':
        self.sessions[interaction.user.id]["Player_choice"] = "Scissors"
        self.sessions[interaction.user.id]["Player_type"] = "✌"
        await self.sessions[interaction.user.id]["Message"].edit(embed = await self.rpsembed(interaction.user), components = [])
        self.sessions[interaction.user.id] = {}
        return await interaction.respond(type=6)
      
      
    
    except discord.NotFound:
        return  

def setup(client):
  client.add_cog(Rps(client))