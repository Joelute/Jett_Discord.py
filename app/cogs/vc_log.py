import discord
from discord.ext import commands
import json
import os
import math
from datetime import datetime
import discord_components
from discord_components import Button, ButtonStyle

# Pepega Coding Adventure: Volume 1

class vc_log(commands.Cog):


  def __init__(self, bot):
    self.bot = bot

    self.board = {}
     


  @commands.command(name="vclog")
  async def vclog(self, ctx):
    with open("vclog_data.json", "r") as f:

      data = json.load(f)
      filter_data = len([i for i in reversed(data) if str(data[i]["server_id"]) == str(ctx.guild.id)])
      
      pages = math.ceil(filter_data/10)
      
      if pages > 0:
        pages -= 1
      
      self.board[ctx.author.id] = {"Message": None, "Page": 0, "Pages": pages, "server": ctx.guild.id}
      
      self.board[ctx.author.id]["Message"] = await ctx.send(embed=await self.board_embed(ctx.author, data), components = 
    [[
      Button(style = ButtonStyle.blue, label = "⬆", custom_id="up"),
      Button(style = ButtonStyle.blue, label = "⬇", custom_id = "down"), 
      
    ]])
  

  async def board_embed(self, user, data):
    
    joined_time, joined_user, activity =  [], [], [] 
    start_at = self.board[user.id]["Page"] * 10
    counter = 0
    end_at = start_at + 10
    
    for i in reversed(data):
      if str(data[i]["server_id"]) != str(self.board[user.id]["server"]):
        continue
      if counter >= start_at:
        get_time = str(data[i]["time"])
        joined_time.append(f"<t:{get_time}>")

        get_user = str(data[i]["user_id"])
        joined_user.append(f"<@{get_user}>")

        channel_name= str(data[i]["channel"])

        activity.append(data[i]["action"] + " " + channel_name)
      
      counter += 1

      if counter == end_at:
        break
    if not joined_time:
      embed = discord.Embed(
      title = "Voice Chat Audit Log",
      description = "❌ No voice chat activity has been recorded in this server.",
      color = discord.Color.green(),
      timestamp = datetime.utcnow()
    )

      embed.set_footer(text=f"Last Update: ")

      return embed

    embed = discord.Embed(
      title = "Voice Chat Audit Log",
      description = "Showing the voice chat audit log for this server.",
      color = discord.Color.green(),
      timestamp = datetime.utcnow()
    )
    
    embed.add_field(name="Time", value="\n".join(joined_time), inline=True)
    
    embed.add_field(name="User", value="\n".join(joined_user), inline=True)

    embed.add_field(name="Activity", value="\n".join(activity), inline=True)
    
    embed.set_footer(text=f"Last Update: ")

    return embed


  @commands.Cog.listener(name = "on_voice_state_update")
  async def on_voice_state_update(self, member, before, after) -> None:
    
    # Join a call from not being in a call previously
    if before.channel == None and after.channel != None:
      with open("vclog_data.json", "r") as f:
        data = json.load(f)
        slot = (len(data) + 1)
        time = math.floor(int(datetime.utcnow().timestamp()))  
        server = (await self.bot.fetch_channel(after.channel.id)).guild.id
        name = str(after.channel.name)
        if len(name) > 21:
          name = name[:20] + "..."    
        data[str(slot)] = {"time": str(time), "user_id": member.id, "channel": name, "action": "Joined", "server_id":server}

    # Leaving a call
    elif before.channel != None and after.channel == None:
      with open("vclog_data.json", "r") as f:
        data = json.load(f)
        slot = (len(data) + 1)
        time = math.floor(int(datetime.utcnow().timestamp()))     
        server = (await self.bot.fetch_channel(before.channel.id)).guild.id
        name = str(before.channel.name)
        if len(name) > 21:
          name = name[:20] + "..." 
        data[str(slot)] = {"time": str(time), "user_id": member.id, "channel": name, "action": "Left", "server_id":server}

    # Joining a call from another call
    elif before.channel != None and after.channel != None and before.channel.id != after.channel.id:
      with open("vclog_data.json", "r") as f:
        data = json.load(f)
        slot = (len(data) + 1)
        time = math.floor(int(datetime.utcnow().timestamp()))
        server = (await self.bot.fetch_channel(after.channel.id)).guild.id
        name = str(after.channel.name)
        if len(name) > 16:
          name = name[:15] + "..."  
        data[str(slot)] = {"time": str(time), "user_id": member.id, "channel": name, "action": "Moved to", "server_id":server}

    else:
      return
    
    with open("vclog_data.json", "w") as f:
      json.dump(data, f, indent = 4)
      print("Recorded Activity")    


  @commands.Cog.listener(name='on_button_click')
  async def on_button_click(self, interaction):
    try:
      if interaction.user.id not in self.board:
        return await interaction.respond(type=6)
        
      if interaction.component.id == 'up':
        if self.board[interaction.user.id]["Page"] <= 0:
          return
    
        self.board[interaction.user.id]["Page"] -= 1
        with open("vclog_data.json", "r") as f:
          data = json.load(f)
          await self.board[interaction.user.id]["Message"].edit(embed=await self.board_embed(interaction.user, data))

      elif interaction.component.id == 'down':
        if self.board[interaction.user.id]["Page"] >= self.board[interaction.user.id]["Pages"]:
          return
    
        self.board[interaction.user.id]["Page"] += 1
        with open("vclog_data.json", "r") as f:
          data = json.load(f)
          await self.board[interaction.user.id]["Message"].edit(embed=await self.board_embed(interaction.user, data))
    
    except discord.NotFound:
        return  

def setup(bot):
  bot.add_cog(vc_log(bot))