from discord.ext import commands
import random
from discord.ext.commands import cooldown, BucketType
class Hello(commands.Cog):

  def __init__(self, client):
    self.client = client


  @commands.Cog.listener()
  async def on_ready(self):
    print("Hello!")

  @commands.Cog.listener()
  async def on_member_join(self, member):
    await member.create_dm()
    await member.dm_channel.send(f"Hey, {member.mention}! Welcome to our Discord server!")

  @commands.command(name="hello", help = "Responds with a greeting")
  async def Hello(self, ctx):
    Hi = ["Hi", "Hello", "Hey"]
    response = random.choice(Hi)
    await ctx.send(response)


def setup(client):
  client.add_cog(Hello(client))