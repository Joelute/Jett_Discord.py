import asyncio
import discord
from discord.ext import commands,tasks
from discord.ext.commands import BucketType, cooldown
import aiohttp
from datetime import datetime
import numpy
import psycopg2
from database import database
from discord_components import Button, ButtonStyle


class Waifu(commands.Cog):

    def __init__(self, client):
        self.client = client
        
        self.cursor = database.get_cursor()

        self.conn = database.get_conn()

        self.update_cursor.start()

        self.drops = {}

        self.collection = {}

    @commands.command(name = "waifu")
    @cooldown(1, 600, BucketType.user)
    async def waifu(self, ctx):
        
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.waifu.pics/sfw/waifu') as response:
                api = await response.json()
                if response.status == 200:
                    url = api["url"]
                else:
                    pass
        
            check = None
            check = await self.try_select(query = """SELECT * FROM "Joelute/Jett"."waifu" WHERE waifu_url = %s""", value = (url))
        

        if check == None:
            drop = await ctx.send(embed = await self.waifu_embed(url, False))
            self.drops[drop.id] = {"message" : drop, "waifu_url": url, "claimed": False, "dropper": ctx.author.id}

        elif check:
            drop = await ctx.send(embed = await self.waifu_embed(url, True))
            self.drops[drop.id] = {"message" : drop, "waifu_url": url, "claimed": True, "dropper": ctx.author.id}
        
    @commands.command(name = "waifus")
    @cooldown(1, 10, BucketType.user)
    async def waifus(self, ctx):
        data = await self.try_select_all(query = """SELECT * FROM "Joelute/Jett"."waifu" WHERE user_id = %s""", value = (str(ctx.author.id),))
        pages = len(data)

        if pages > 0:
            pages -= 1
        
        self.collection[ctx.author.id] = {"Message": None, "Page": pages, "Pages": pages}
        self.collection[ctx.author.id]["Message"] = await ctx.send(embed=await self.waifus_embed(ctx.author, data), components = 
        [[
            Button(style = ButtonStyle.blue, label = "◀", custom_id="previous"),
            Button(style = ButtonStyle.blue, label = "▶", custom_id = "next"), 
        
        ]])



    @commands.Cog.listener(name = "on_reaction_add")
    async def on_reaction_add(self, reaction, user):
        if user.id != self.drops[reaction.message.id]["dropper"]:
            await asyncio.sleep(7)

        if not reaction.message.id in self.drops:
            return

        if reaction.message.id in self.drops:
            if self.drops[reaction.message.id]["claimed"] == True:
                return
            elif self.drops[reaction.message.id]["claimed"] == False:
                while True:
                    uid = ''.join(map(str,numpy.random.randint(0,9,6)))
                    check = await self.try_select(query = """SELECT * FROM "Joelute/Jett"."waifu" WHERE id = %s""", value = (str(uid),))
                    if not check:
                        break

                    if check:
                        continue

                await self.try_insert(query = """INSERT INTO "Joelute/Jett"."waifu" (user_id, waifu_url, id) VALUES (%s,%s,%s)""", value = (user.id, self.drops[reaction.message.id]["waifu_url"], uid))
                await self.drops[reaction.message.id]["message"].edit(embed = await self.waifu_embed(self.drops[reaction.message.id]["waifu_url"], True))
                self.drops.pop(reaction.message.id)

    @commands.Cog.listener(name = "on_button_click")
    async def on_button_click(self, interaction):
        try:
            if not interaction.user.id in self.collection:
                return await interaction.respond(type=6)
            
            if interaction.component.id == 'previous':
                if self.collection[interaction.user.id]["Page"] >= self.collection[interaction.user.id]["Pages"]:
                    return
        
                self.collection[interaction.user.id]["Page"] += 1

            elif interaction.component.id == 'next':
                if self.collection[interaction.user.id]["Page"] <= 0:
                    return
        
                self.collection[interaction.user.id]["Page"] -= 1

            else:
                return

            data = await self.try_select_all(query="""SELECT * FROM "Joelute/Jett"."waifu" WHERE user_id = %s""", value = (str(interaction.user.id),))
            await self.collection[interaction.user.id]["Message"].edit(embed=await self.waifus_embed(interaction.user, data))
        except:
            discord.NotFound

    @tasks.loop(minutes = 1)
    async def update_cursor(self):
        self.cursor = database.get_cursor()
        self.conn = database.get_conn()


    async def waifu_embed(self, url, claimed):  
        if claimed == False:          
            embed = discord.Embed(
                title = " ",
                description  = "Here's your waifu!",
                colour = discord.Color.red(),
                timestamp = datetime.utcnow()
            )
            embed.set_image(url = url)
            return embed

        if claimed == True:
            embed = discord.Embed(
                title = " ",
                description  = "Here's your waifu!",
                colour = discord.Color.green(),
            )
            embed.set_image(url = url)
            owner = await self.try_select(query = """SELECT * FROM "Joelute/Jett"."waifu" where waifu_url = %s""", value = (str(url),))
            user = await self.client.fetch_user(owner["user_id"])
            footer_message = f"Owned by {user.name}"
            embed.set_footer(text = footer_message, icon_url = user.avatar_url)
            return embed

    async def waifus_embed(self, user, data):
        embed = discord.Embed(
                title = " ",
                description  = "Here's your waifu collection!",
                colour = discord.Color.green(),
            )
        page = self.collection[user.id]["Page"]
        embed.set_image(url = data[page]["waifu_url"])
        footer_message = f"Owned by {user.name}"
        embed.set_footer(text = footer_message, icon_url = user.avatar_url)
        return embed
        
    async def try_select_all(self, query, value):
        try:
            self.cursor.execute(query,value)
            return self.cursor.fetchall()

        except psycopg2.OperationalError:
            print("Connection to Database has been closed.\nAttempting to re-connect...")
            cursor, conn = database.try_connection()
            database.set_conn(cursor, conn)
            self.cursor = cursor
            self.conn = conn
            self.cursor.execute(query,value)
            return self.cursor.fetchall()

        except:
            pass


    async def try_select(self, query, value):
        try:
            self.cursor.execute(query,value)
            return self.cursor.fetchone()

        except psycopg2.OperationalError:
            print("Connection to Database has been closed.\nAttempting to re-connect...")
            cursor, conn = database.try_connection()
            database.set_conn(cursor, conn)
            self.cursor = cursor
            self.conn = conn
            self.cursor.execute(query,value)
            return self.cursor.fetchone()

        except:
            pass

    async def try_insert(self,query, value):
        try:
            self.cursor.execute(query,value)
            self.conn.commit()

        except psycopg2.OperationalError:
            print("Connection to Database has been closed.\nAttempting to re-connect...")
            cursor, conn = database.try_connection()
            database.set_conn(cursor, conn)
            self.cursor = cursor
            self.conn = conn
            self.cursor.execute(query,value)
            self.conn.commit()

        except psycopg2.InterfaceError:
            print("Connection to Database has been closed.\nAttempting to re-connect...")
            cursor, conn = database.try_connection()
            database.set_conn(cursor, conn)
            self.cursor = cursor
            self.conn = conn
            self.cursor.execute(query,value)
            self.conn.commit()

        except:
            self.cursor.execute("""rollback;""")

def setup(client):
  client.add_cog(Waifu(client))