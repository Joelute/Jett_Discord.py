from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, CommandNotFound


class Emote_enlarge(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass
        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"{ctx.author.mention} You need to wait {int(exc.retry_after//60)} minutes and {int(exc.retry_after%60)} seconds!")
        else:
            pass
    
  
def setup(client):
  client.add_cog(Emote_enlarge(client))