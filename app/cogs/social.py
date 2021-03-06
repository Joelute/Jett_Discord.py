import discord
from discord.ext import commands
import aiohttp
from datetime import datetime
from discord.ext.commands import cooldown, BucketType

class Social(commands.Cog):

    def __init__(self, client):
        self.client = client
 

    @commands.command(name = "hug")
    @cooldown(1, 4, BucketType.user)
    async def hug(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.waifu.pics/sfw/hug') as response:
                api = await response.json()
                if response.status == 200:
                    url = api["url"]
                    print(url)
                else:
                    pass

        embed = discord.Embed(
            title = " ",
            description  = f"{ctx.author.name} hugs Jett",
            colour = discord.Color.green(),
            timestamp = datetime.utcnow()
        )
        embed.set_image(url = url)
        await ctx.send(embed = embed)
  
    @commands.command(name = "kiss")
    @cooldown(1, 4, BucketType.user)
    async def kiss(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.waifu.pics/sfw/kiss') as response:
                api = await response.json()
                if response.status == 200:
                    url = api["url"]
                else:
                    pass

        embed = discord.Embed(
            title = " ",
            description  = f"{ctx.author.name} kisses Jett",
            colour = discord.Color.green(),
            timestamp = datetime.utcnow()
        )
        embed.set_image(url = url)
        await ctx.send(embed = embed)
  
    @commands.command(name = "cry")
    @cooldown(1, 4, BucketType.user)
    async def cry(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.waifu.pics/sfw/cry') as response:
                api = await response.json()
                if response.status == 200:
                    url = api["url"]
                else:
                    pass

        embed = discord.Embed(
            title = " ",
            description  = f"{ctx.author.name} cries",
            colour = discord.Color.green(),
            timestamp = datetime.utcnow()
        )
        embed.set_image(url = url)
        await ctx.send(embed = embed)
  
    @commands.command(name = "bonk")
    @cooldown(1, 4, BucketType.user)
    async def bonk(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.waifu.pics/sfw/bonk') as response:
                api = await response.json()
                if response.status == 200:
                    url = api["url"]
                else:
                    pass

        embed = discord.Embed(
            title = " ",
            description  = f"{ctx.author.name} bonks Jett",
            colour = discord.Color.green(),
            timestamp = datetime.utcnow()
        )
        embed.set_image(url = url)
        await ctx.send(embed = embed)

    @commands.command(name = "yeet")
    @cooldown(1, 4, BucketType.user)
    async def yeet(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.waifu.pics/sfw/yeet') as response:
                api = await response.json()
                if response.status == 200:
                    url = api["url"]
                else:
                    pass

        embed = discord.Embed(
            title = " ",
            description  = f"{ctx.author.name} yeets Jett",
            colour = discord.Color.green(),
            timestamp = datetime.utcnow()
        )
        embed.set_image(url = url)
        await ctx.send(embed = embed)


    @commands.command(name = "kill")
    @cooldown(1, 4, BucketType.user)
    async def kill(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.waifu.pics/sfw/kill') as response:
                api = await response.json()
                if response.status == 200:
                    url = api["url"]
                else:
                    pass

        embed = discord.Embed(
            title = " ",
            description  = f"{ctx.author.name} kills Jett",
            colour = discord.Color.green(),
            timestamp = datetime.utcnow()
        )
        embed.set_image(url = url)
        await ctx.send(embed = embed)

    @commands.command(name = "slap")
    @cooldown(1, 4, BucketType.user)
    async def slap(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.waifu.pics/sfw/slap') as response:
                api = await response.json()
                if response.status == 200:
                    url = api["url"]
                else:
                    pass

        embed = discord.Embed(
            title = " ",
            description  = f"{ctx.author.name} slaps Jett",
            colour = discord.Color.green(),
            timestamp = datetime.utcnow()
        )
        embed.set_image(url = url)
        await ctx.send(embed = embed)

    @commands.command(name = "kick")
    @cooldown(1, 4, BucketType.user)
    async def kick(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.waifu.pics/sfw/kick') as response:
                api = await response.json()
                if response.status == 200:
                    url = api["url"]
                else:
                    pass

        embed = discord.Embed(
            title = " ",
            description  = f"{ctx.author.name} kicks Jett",
            colour = discord.Color.green(),
            timestamp = datetime.utcnow()
        )
        embed.set_image(url = url)
        await ctx.send(embed = embed)

    @commands.command(name = "dance")
    @cooldown(1, 4, BucketType.user)
    async def dance(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.waifu.pics/sfw/dance') as response:
                api = await response.json()
                if response.status == 200:
                    url = api["url"]
                else:
                    pass

        embed = discord.Embed(
            title = " ",
            description  = f"{ctx.author.name} dances with Jett",
            colour = discord.Color.green(),
            timestamp = datetime.utcnow()
        )
        embed.set_image(url = url)
        await ctx.send(embed = embed)

    


def setup(client):
  client.add_cog(Social(client))