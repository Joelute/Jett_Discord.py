import discord
import asyncio
from datetime import datetime, timedelta
from discord.ext import commands
from discord_components import Button, ButtonStyle
import math



class timer(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.sessions = {}

        self.timer_lists = {}
 

    @commands.command(name = "timer")
    async def timer(self, ctx):
        self.sessions[ctx.author.id] = {"message": None, "hours": None, "minutes":None, "seconds":None, "name":None, "ring_time":None, "page":0}
        self.sessions[ctx.author.id]["message"] = await ctx.send(embed = await self.timer_embed(ctx.author.id), components = 
            [[
            Button(style = ButtonStyle.blue, label = "▶", custom_id="next"),
            Button(style = ButtonStyle.blue, label = "❌", custom_id = "quit")
            ]])
        

    async def timer_embed(self, user_id):
        user = self.sessions[user_id]
        if user["page"] == 0:
            embed = discord.Embed(
                title = "Creating Timer",
                description = "Please enter the hour for the timer.",
                colour = discord.Colour.light_gray(),
                timestamp = datetime.utcnow()
            )
            return embed

        elif user["page"] == 1:
            embed = discord.Embed(
                title = "Creating Timer",
                description = "Please enter the minute for the timer.",
                colour = discord.Colour.light_gray(),
                timestamp = datetime.utcnow()
            )
            embed.add_field(name = "Hour", value= user["hours"], inline=True)
            return embed


        elif user["page"] == 2:
            embed = discord.Embed(
                title = "Creating Timer",
                description = "Please enter the second for the timer.",
                colour = discord.Colour.light_gray(),
                timestamp = datetime.utcnow()
            )
            embed.add_field(name = "Hour", value= user["hours"], inline=True)
            embed.add_field(name = "Minute", value= user["minutes"], inline=True)
            return embed
        
        elif user["page"] == 3:
            
            embed = discord.Embed(
                title = "Creating Timer",
                description = "Please enter the name of the timer.",
                colour = discord.Colour.light_gray(),
                timestamp = datetime.utcnow()
            )
            embed.add_field(name = "Hour", value= user["hours"], inline=True)
            embed.add_field(name = "Minute", value= user["minutes"], inline=True)
            embed.add_field(name = "Second", value= user["seconds"], inline=True)
            return embed

        elif user["page"] == 4:
            embed = discord.Embed(
                title = "Confirm Timer",
                description = "Does this timer look good?",
                colour = discord.Colour.light_gray(),
                timestamp = datetime.utcnow()
            )
            embed.add_field(name = "Hour", value= user["hours"], inline=True)
            embed.add_field(name = "Minute", value= user["minutes"], inline=True)
            embed.add_field(name = "Second", value= user["seconds"], inline=True)
            embed.add_field(name = "Name of Timer:", value = user["name"], inline = False)
            ring_time = str(user["ring_time"])
            embed.add_field(name = "Pings at: ", value= f"<t:{ring_time}>")
            return embed

        elif user["page"] == 5:
            
            embed = discord.Embed(
                title = "Created Timer",
                description = "Successfully created the timer!",
                colour = discord.Colour.green(),
                timestamp = datetime.utcnow()
            )
            embed.add_field(name = "Hour", value= user["hours"], inline=True)
            embed.add_field(name = "Minute", value= user["minutes"], inline=True)
            embed.add_field(name = "Second", value= user["seconds"], inline=True)
            embed.add_field(name = "Name of Timer:", value = user["name"], inline = False)
            ring_time = str(user["ring_time"])
            embed.add_field(name = "Pings at: ", value= f"<t:{ring_time}>", inline = False)
            return embed

        elif user["page"] == 400:
            embed = discord.Embed(
                title = "Failed to Create Timer",
                description = "❌ Hours can not be shorter than 0 hours or longer than 24 hours",
                colour = discord.Colour.red(),
                timestamp = datetime.utcnow()
            )
            return embed
        
        elif user["page"] == 401:
            embed = discord.Embed(
                title = "Failed to Create Timer",
                description = "❌ Minutes can not be shorter than 0 minutes or longer than 60 minutes",
                colour = discord.Colour.red(),
                timestamp = datetime.utcnow()
            )
            return embed

        elif user["page"] == 402:
            embed = discord.Embed(
                title = "Failed to Create Timer",
                description = "❌ Seconds can not be shorter than 0 seconds or longer than 60 seconds",
                colour = discord.Colour.red(),
                timestamp = datetime.utcnow()
            )
            return embed

        elif user["page"] == 450:
            embed = discord.Embed(
                title = " ",
                description = "❌ Cancelled timer creation",
                colour = discord.Colour.red(),
                timestamp = datetime.utcnow()
            )
            return embed
    @commands.Cog.listener(name = "on_button_click")
    async def on_button_click(self, interaction):
        try:
            if interaction.user.id not in self.sessions:
                return await interaction.respond(type=6)
            
            user = self.sessions[interaction.user.id]

            if interaction.component.id == 'next':
                if user["page"] == 0:
                    user["hours"] = 0
                    components = [[
                        Button(style = ButtonStyle.blue, label = "◀", custom_id = "back"),
                        Button(style = ButtonStyle.blue, label = "▶", custom_id="next"),
                        Button(style = ButtonStyle.blue, label = "❌", custom_id = "quit")
                    ]]
                elif user["page"] == 1:
                    user["minutes"] = 0
                    components = [[
                        Button(style = ButtonStyle.blue, label = "◀", custom_id = "back"),
                        Button(style = ButtonStyle.blue, label = "▶", custom_id="next"),
                        Button(style = ButtonStyle.blue, label = "❌", custom_id = "quit")
                    ]]
                elif user["page"] == 2:
                    user["seconds"] = 0
                    components = [[
                        Button(style = ButtonStyle.blue, label = "◀", custom_id = "back"),
                        Button(style = ButtonStyle.blue, label = "▶", custom_id="next"),
                        Button(style = ButtonStyle.blue, label = "❌", custom_id = "quit")
                    ]]
                elif user["page"] == 3:
                    user["name"] = "Timer"
                    user["ring_time"] = math.floor(int((datetime.utcnow() + timedelta(hours = user["hours"], minutes = user["minutes"], seconds=user["seconds"])).timestamp()))
                    components = [[
                        Button(style = ButtonStyle.blue, label = "◀", custom_id = "back"),
                        Button(style = ButtonStyle.blue, label = "✅", custom_id="finish"),
                        Button(style = ButtonStyle.blue, label = "❌", custom_id = "quit")
                    ]]

                else:
                    return

                user["page"] += 1
                
                await user["message"].edit(embed = await self.timer_embed(interaction.user.id), components = components)
                return await interaction.respond(type=6)

            elif interaction.component.id == 'back':
                if user["page"] == 1:
                    user["hours"] = None
                    components = [[
                        Button(style = ButtonStyle.blue, label = "▶", custom_id="next"),
                        Button(style = ButtonStyle.blue, label = "❌", custom_id = "quit")
                    ]]
                elif user["page"] == 2:
                    user["minutes"] = None
                    components = [[
                        Button(style = ButtonStyle.blue, label = "◀", custom_id = "back"),
                        Button(style = ButtonStyle.blue, label = "▶", custom_id="next"),
                        Button(style = ButtonStyle.blue, label = "❌", custom_id = "quit")
                    ]]
                elif user["page"] == 3:
                    user["seconds"] = None
                    components = [[
                        Button(style = ButtonStyle.blue, label = "◀", custom_id = "back"),
                        Button(style = ButtonStyle.blue, label = "▶", custom_id="next"),
                        Button(style = ButtonStyle.blue, label = "❌", custom_id = "quit")
                    ]]
                elif user["page"] == 4:
                    user["name"] = None
                    components = [[
                        Button(style = ButtonStyle.blue, label = "◀", custom_id = "back"),
                        Button(style = ButtonStyle.blue, label = "▶", custom_id="next"),
                        Button(style = ButtonStyle.blue, label = "❌", custom_id = "quit")
                    ]]

                else:
                    return

                user["page"] -= 1
                
                await user["message"].edit(embed = await self.timer_embed(interaction.user.id), components = components)
                return await interaction.respond(type=6)

            elif interaction.component.id == 'finish':
                user["page"] += 1
                await user["message"].edit(embed = await self.timer_embed(interaction.author.id), components = [])      
                countdown = (int(user["hours"])*3600) + (int(user["minutes"])*60) + int(user["seconds"])
                await asyncio.sleep(countdown)
                await interaction.channel.send("{} The timer \"{}\" is up!".format(interaction.author.mention, user["name"]))
                

            elif interaction.component.id == 'quit':
                user["page"] = 450
                await user["message"].edit(embed = await self.timer_embed(interaction.author.id), components = [])
                self.sessions.pop(interaction.author.id)

        except:
            return discord.NotFound
    
    @commands.Cog.listener(name = "on_message")
    async def on_message(self, ctx):

        if ctx.author == self.client.user:    
            return
        
        elif not ctx.author.id in self.sessions:
            return

        try:
            if ctx.author.id in self.sessions:
                
                user = self.sessions[ctx.author.id]
                if user["page"] == 0:
                    
                    assert int(ctx.content) >= 0
                    assert int(ctx.content) <= 24
                    await ctx.delete()
                    components = [[
                        Button(style = ButtonStyle.blue, label = "◀", custom_id = "back"),
                        Button(style = ButtonStyle.blue, label = "▶", custom_id="next"),
                        Button(style = ButtonStyle.blue, label = "❌", custom_id = "quit")
                    ]]
                    user["hours"] = int(ctx.content)

            
                elif user["page"] == 1:

                    assert int(ctx.content) >= 0
                    assert int(ctx.content) <= 60
                    await ctx.delete()
                    components = [[
                        Button(style = ButtonStyle.blue, label = "◀", custom_id = "back"),
                        Button(style = ButtonStyle.blue, label = "▶", custom_id="next"),
                        Button(style = ButtonStyle.blue, label = "❌", custom_id = "quit")
                    ]]
                    user["minutes"] = int(ctx.content)  
                    

                elif user["page"] == 2:
                    
                    assert int(ctx.content) >= 0
                    assert int(ctx.content) <= 60
                    await ctx.delete()
                    components = [[
                        Button(style = ButtonStyle.blue, label = "◀", custom_id = "back"),
                        Button(style = ButtonStyle.blue, label = "▶", custom_id="next"),
                        Button(style = ButtonStyle.blue, label = "❌", custom_id = "quit")
                    ]]
                    user["seconds"] = int(ctx.content)  


                elif user["page"] == 3:
                    await ctx.delete()
                    components = [[
                        Button(style = ButtonStyle.blue, label = "◀", custom_id = "back"),
                        Button(style = ButtonStyle.blue, label = "✅", custom_id="finish"),
                        Button(style = ButtonStyle.blue, label = "❌", custom_id = "quit")
                    ]]
                    user["name"] = str(ctx.content)
                    user["ring_time"] = math.floor(int((datetime.utcnow() + timedelta(hours = user["hours"], minutes = user["minutes"], seconds=user["seconds"])).timestamp()))                
                else:
                    return

                user["page"] += 1
                await user["message"].edit(embed = await self.timer_embed(ctx.author.id), components = components)
                    

        except ValueError:
            pass

        except KeyError:
            pass

        except AssertionError:
            user["page"] += 400
            await user["message"].edit(embed = await self.timer_embed(ctx.author.id))
            self.sessions.pop(ctx.author.id)
        

def setup(client):
  client.add_cog(timer(client))