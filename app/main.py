import discord
import os
from datetime import datetime
from pytz import timezone
from dotenv import load_dotenv
from discord.ext import commands, tasks
from itertools import cycle
from discord_components import DiscordComponents
from database import database
import psycopg2

load_dotenv()
TOKEN = os.getenv("TOKEN")
RIOT_KEY = os.getenv("riot_key")

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(case_insensitive = True, command_prefix='/', intents = intents)
DiscordComponents(client)
client.remove_command('help')

status = cycle(["VALORANT", "Watch this!"])


#--------------------------------------------------------------------------------------


@client.event
async def on_ready():
  change_status.start()
  database_conn.start()
  

@client.command(name = "help")
async def help(ctx):
  embed = discord.Embed(
    title = "List of commands",
    description = "Here's everything I can do!",
    colour = discord.Colour.blue(),
    timestamp = datetime.utcnow()
  )

  embed.add_field(name = "Tic-Tac-Toe", value = "Play Tic-Tac-Toe with your friends. Join the fun and see who's the best.`/ttt`", inline = True)

  embed.add_field(name = "Hangman", value = "Play some good old hangman! Guess the word for a treat! `/hangman`", inline = True)

  embed.add_field(name = "Rock Paper Scissors", value = "Play rock, paper, scissors against Jett! Legend has it that Jett has a 66% winrate... `/rps`", inline = True)

  embed.add_field(name = "Roll dice", value = "Roll the dice to get a random number! `/roll [number of sides]`", inline = True)

  embed.add_field(name = "Spam Ping", value = "Spam ping someone and grab their attention **Not responible for what happens btw**.`/ping [@name] [# of pings]`", inline = True)

  embed.add_field(name = "Random Quote", value = "Get a random quote and have it read aloud by Discord.`/quote`", inline = True)

  embed.add_field(name = "Random Anime Quote", value = "Get a random Anime quote and have it read aloud by Discord.`/quote`", inline = True)

  await ctx.send(embed=embed)


#--------------------------------------------------------------------------------------


@client.command(name="del")
async def clear(ctx, amount: int):
  role = discord.utils.find(lambda r: r.name == 'Admin', ctx.message.guild.roles)
  adminuser = [231586823384596480, 289955808920338435, 332735027530170369]
  if role in ctx.author.roles or ctx.author.id in adminuser:
    if amount > 500:
      await ctx.send("Invaild Value")
      return
    await ctx.channel.purge(limit=amount+1)
  elif not role in ctx.author.roles:
    await ctx.send("You do not have permission to use this command!")


#--------------------------------------------------------------------------------------


@client.command(name="ping")
async def pingspam(ctx, user: discord.User, amount: int):
  role = discord.utils.find(lambda r: r.name == 'Admin', ctx.message.guild.roles)
  adminuser = [231586823384596480, 289955808920338435, 332735027530170369, 701996967500316742]
  Myid = f'<@{user.id}>'
  if role in ctx.author.roles or ctx.author.id in adminuser:
    if amount > 50: 
      await ctx.send("You can only spam ping someone a maximum of 50 times. Maybe go get a life.")
    else:
      await ctx.channel.purge(limit=1)
      deletelist = []
      for i in range(amount):
        pingmessage = await ctx.send(f'{Myid}')
        deletelist.append(pingmessage)
      for i in deletelist:
        await i.delete()

  elif not role in ctx.author.roles:
    await ctx.send("You do not have permission to use this command!")


#--------------------------------------------------------------------------------------


@client.command(name="load")
async def load(ctx, extension):
  role = discord.utils.find(lambda r: r.name == 'Admin', ctx.message.guild.roles)
  if not role in ctx.author.roles and ctx.author.id != 231586823384596480:
    await ctx.send("You do not have permission to use this command!")
    return
  client.load_extension(f'cogs.{extension}')
  await ctx.send(f"Loaded {extension}")

#--------------------------------------------------------------------------------------


@client.command(name="unload")
async def unload(ctx, extension):
  
  role = discord.utils.find(lambda r: r.name == 'Admin', ctx.message.guild.roles)
  if not role in ctx.author.roles and ctx.author.id != 231586823384596480:
    await ctx.send("You do not have permission to use this command!")
    return
  client.unload_extension(f'cogs.{extension}')
  await ctx.send(f"Unloaded {extension}")
  

@client.command(name="reload")
async def reload(ctx, extension):
  role = discord.utils.find(lambda r: r.name == 'Admin', ctx.message.guild.roles)
  if not role in ctx.author.roles and ctx.author.id != 231586823384596480 and ctx.author.id != 332735027530170369:
    await ctx.send("You do not have permission to use this command!")
    return
  client.unload_extension(f'cogs.{extension}')
  client.load_extension(f'cogs.{extension}')
  await ctx.send(f"Reloaded {extension}")


for filename in os.listdir('./app/cogs'):
  if filename.endswith("words.py" or ""):
    pass
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

@tasks.loop(minutes = 10)
async def change_status():
  await client.change_presence(activity= discord.Game(next(status)))

@tasks.loop(minutes = 4)
async def database_conn():
  try:
    conn = database.get_conn()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM "Joelute/Jett"."vclog" """)
    print("Connection Stable " + str(datetime.now(timezone("EST"))))
  except psycopg2.OperationalError:
    print("Connection to Database has been closed.\nAttempting to re-connect...")
    cursor, conn = database.try_connection()
    database.set_conn(cursor, conn)


client.run(TOKEN)

