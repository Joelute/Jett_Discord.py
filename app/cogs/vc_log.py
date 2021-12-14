import discord
from discord.ext import commands, tasks
import json
import os
import math
from datetime import datetime
import discord_components
from discord_components import Button, ButtonStyle
from database import database
import psycopg2
# Pepega Coding Adventure: Volume 1


class Vc_log(commands.Cog):


  def __init__(self, bot):
    self.bot = bot

    self.board = {}
     
    self.conn = database.get_conn()

    self.cursor = database.get_cursor()

    self.update_cursor.start()
    
  @commands.command(name="vclog")
  async def vclog(self, ctx):
      try:
        self.cursor.execute("""SELECT * FROM "Joelute/Jett"."vclog" WHERE server_id = %s""", (str(ctx.guild.id),))
      
        filter_data = self.cursor.fetchall()
      
      except psycopg2.OperationalError:

        print("Connection to Database has been closed.\nAttempting to re-connect...")
        cursor, conn = database.try_connection()
        database.set_conn(cursor, conn)
        self.cursor = cursor
        self.conn = conn
        self.cursor.execute("""SELECT * FROM "Joelute/Jett"."vclog" WHERE server_id = %s""", (str(ctx.guild.id),))
        filter_data = self.cursor.fetchall()

      pages = math.ceil(len(filter_data)/10)

      if pages > 0:
        pages -= 1
      
      self.board[ctx.author.id] = {"Message": None, "Page": 0, "Pages": pages, "server": ctx.guild.id}
      
      self.board[ctx.author.id]["Message"] = await ctx.send(embed=await self.board_embed(ctx.author, filter_data), components = 
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
      
      
      if counter >= start_at:
        get_time = str(i["timestamp"])
        joined_time.append(f"<t:{get_time}>")

        get_user = str(i["user_id"])
        joined_user.append(f"<@{get_user}>")

        channel_name= str(i["channel"])

        activity.append(i["action"] + " " + channel_name)
      
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

        time = math.floor(int(datetime.utcnow().timestamp()))  
        server = (await self.bot.fetch_channel(after.channel.id)).guild.id
        channel_name = str(after.channel.name)
        if len(channel_name) > 21:
          channel_name = channel_name[:20] + "..."    
        action = "Joined"

    # Leaving a call
    elif before.channel != None and after.channel == None:

        time = math.floor(int(datetime.utcnow().timestamp()))     
        server = (await self.bot.fetch_channel(before.channel.id)).guild.id
        channel_name = str(before.channel.name)
        if len(channel_name) > 21:
          channel_name = channel_name[:20] + "..." 
        action = "Left"

    # Joining a call from another call
    elif before.channel != None and after.channel != None and before.channel.id != after.channel.id:

        time = math.floor(int(datetime.utcnow().timestamp()))
        server = (await self.bot.fetch_channel(after.channel.id)).guild.id
        channel_name = str(after.channel.name)
        if len(channel_name) > 16:
          channel_name = channel_name[:15] + "..."  
        action = "Moved to"
    
    else:
      return

    # Possible ERROR: CURRENT TRANSACTION IS ABORTED, COMMANDS IGNORED UNTIL END OF TRANSACTION BLOCK
    try:
      self.cursor.execute("""INSERT INTO "Joelute/Jett"."vclog" (timestamp, user_id, channel, action, server_id) VALUES (%s,%s,%s,%s,%s)""", (time, member.id, channel_name, action, server))
      self.conn.commit()  

    except psycopg2.InterfaceError:
      print("Connection to Database has been closed.\nAttempting to re-connect...")
      cursor, conn = database.try_connection()
      database.set_conn(cursor, conn)
      self.cursor = cursor
      self.conn = conn
      self.cursor.execute("""INSERT INTO "Joelute/Jett"."vclog" (timestamp, user_id, channel, action, server_id) VALUES (%s,%s,%s,%s,%s)""", (time, member.id, channel_name, action, server))
      self.conn.commit()
      print("Recorded Activity")  

    except Exception as e:
      self.cursor.execute("""rollback;""")
      

  @commands.Cog.listener(name='on_button_click')
  async def on_button_click(self, interaction):
    try:
      if interaction.user.id not in self.board:
        return await interaction.respond(type=6)
        
      if interaction.component.id == 'up':
        if self.board[interaction.user.id]["Page"] <= 0:
          return
    
        self.board[interaction.user.id]["Page"] -= 1

      elif interaction.component.id == 'down':
        if self.board[interaction.user.id]["Page"] >= self.board[interaction.user.id]["Pages"]:
          return
    
        self.board[interaction.user.id]["Page"] += 1

      else:
        return

      try:
        self.cursor.execute("""SELECT * FROM "Joelute/Jett"."vclog" WHERE server_id = %s""", (str(self.board[interaction.user.id]["server"]),))
        filter_data = self.cursor.fetchall()
        await self.board[interaction.user.id]["Message"].edit(embed=await self.board_embed(interaction.user, filter_data))

      except psycopg2.OperationalError:
        print("Connection to Database has been closed.\nAttempting to re-connect...")
        cursor, conn = database.try_connection()
        database.set_conn(cursor, conn)
        self.cursor = cursor
        self.conn = conn
        self.cursor.execute("""SELECT * FROM "Joelute/Jett"."vclog" WHERE server_id = %s""", (str(self.board[interaction.user.id]["server"]),))
        filter_data = self.cursor.fetchall()
        await self.board[interaction.user.id]["Message"].edit(embed=await self.board_embed(interaction.user, filter_data))
    except discord.NotFound:
      return
  
  @tasks.loop(minutes = 1)
  async def update_cursor(self):
    self.cursor = database.get_cursor()
    self.conn = database.get_conn()

def setup(bot):
  bot.add_cog(Vc_log(bot))