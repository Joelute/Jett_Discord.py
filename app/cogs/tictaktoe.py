import discord
from discord.ext import commands
import discord_components
from discord_components import Button, ButtonStyle

class tictactoe(commands.Cog):

  def __init__(self, client):
    self.client = client

    self.session = {}
    self.times = []
    
  
  @commands.command(name="ttt", help = "")
  async def tttt(self, ctx):
   

    async def loadPlayers(self, ctx):
      Player1 = ctx.author
      duel = await ctx.send(f"{Player1.mention} has challenged you to a DUEL! React to play!")
      await duel.add_reaction("⚔")
      def check(reaction,user):
        return user != self.client.user and str(reaction.emoji) == ("⚔") and ctx.channel == reaction.message.channel
      reaction, user = await self.client.wait_for("reaction_add", timeout = 60.0 , check = check)
      Player2 = user
      await ctx.send(f"{Player2.mention} has accepted {Player1.mention}\'s challenge!")
      self.session[ctx.author.id] = {"1":ctx.author.id, "2": Player2.id, "message": None, "turn": 1, "board":[0,0,0,0,0,0,0,0,0]} 
      self.session[Player2.id] = self.session[ctx.author.id]
      return Player1,Player2

    Player1, Player2 = await loadPlayers(self, ctx)
    components = [[],[],[]]
    counter = 1
    board = self.session[ctx.author.id]["board"]
    for i in range(3):
      for j in range(3):
          if board[counter-1] == 0:
            components[i].append(Button(style = ButtonStyle.blue, label = "\u200b", custom_id = counter))
            counter += 1

          elif board[counter-1] == 1:
            components[i].append(Button(style = ButtonStyle.blue, label = "⭕", custom_id = counter, disabled = True))
            counter += 1
          elif board[counter-1] == 2:
            components[i].append(Button(style = ButtonStyle.blue, label = "❌", custom_id = counter, disabled = True))
            counter += 1
    components = [[
    Button(style = ButtonStyle.blue, label = "\u200b", custom_id = counti*3+countj+1) if board[counti*3+countj]==0 else 
    Button(style = ButtonStyle.blue, label = "⭕", custom_id = counti*3+countj+1, disabled = True) if board[counti*3+countj]==1 else 
    Button(style = ButtonStyle.blue, label = "❌", custom_id = counti*3+countj+1, disabled = True) for countj in range(3)]for counti in range(3)]
    
    self.session[ctx.author.id]["message"] = await ctx.send(f"{ctx.author.mention}, It's your turn!", components = components)

  
  @commands.Cog.listener(name='on_button_click')
  async def on_button_click(self, interaction):
    try:
      if interaction.user.id != self.session[interaction.user.id]["1"] and interaction.user.id != self.session[interaction.user.id]["2"]:
        return await interaction.respond(type=6)

      turn = self.session[interaction.user.id]["turn"]
      if interaction.user.id != self.session[interaction.user.id][str(turn)]:
        await interaction.send(content = "It is not your turn!")
        return
      board = self.session[interaction.user.id]["board"]
      
      for i in range(1, 10):
        if interaction.component.id == str(i):
          
          board[i-1] = turn

          for i in range(0, len(board), 3):

            if (board[i] == board[i + 1] == board[i + 2] and board[i] == turn):
              components = [[
                Button(style = ButtonStyle.blue, label = "\u200b", custom_id = counti*3+countj+1, disabled = True) if board[counti*3+countj]==0 else 
                Button(style = ButtonStyle.blue, label = "⭕", custom_id = counti*3+countj+1, disabled = True) if board[counti*3+countj]==1 else 
                Button(style = ButtonStyle.blue, label = "❌", custom_id = counti*3+countj+1, disabled = True) for countj in range(3)]for counti in range(3)]

              if turn == 1:
                player1 = await self.client.fetch_user(self.session[interaction.user.id][str(turn)])
                player2 = await self.client.fetch_user(self.session[interaction.user.id][str(turn+1)])
              elif turn == 2:
                player1 = await self.client.fetch_user(self.session[interaction.user.id][str(turn)])
                player2 = await self.client.fetch_user(self.session[interaction.user.id][str(turn-1)])

              await self.session[interaction.user.id]["message"].edit(f"{player1.mention} It is your turn!", components= components)
              await interaction.channel.send(f"{player1.mention} has won against {player2.mention}!")
              return await interaction.respond(type=6)
              
            
            
          for i in range(3):
            if (board[i] == board[3 + i] == board[6 + i] and board[i] == turn):
              components = [[
                Button(style = ButtonStyle.blue, label = "\u200b", custom_id = counti*3+countj+1, disabled = True) if board[counti*3+countj]==0 else 
                Button(style = ButtonStyle.blue, label = "⭕", custom_id = counti*3+countj+1, disabled = True) if board[counti*3+countj]==1 else 
                Button(style = ButtonStyle.blue, label = "❌", custom_id = counti*3+countj+1, disabled = True) for countj in range(3)]for counti in range(3)]
              if turn == 1:
                player1 = await self.client.fetch_user(self.session[interaction.user.id][str(turn)])
                player2 = await self.client.fetch_user(self.session[interaction.user.id][str(turn+1)])
              elif turn == 2:
                player1 = await self.client.fetch_user(self.session[interaction.user.id][str(turn)])
                player2 = await self.client.fetch_user(self.session[interaction.user.id][str(turn-1)])
              await self.session[interaction.user.id]["message"].edit(f"{player1.mention} It is your turn!", components= components)
              await interaction.channel.send(f"{player1.mention} has won against {player2.mention}!")
              return await interaction.respond(type=6)
          
          if (board[0] == board[4] == board[8] and board[4] == turn):
            components = [[
                Button(style = ButtonStyle.blue, label = "\u200b", custom_id = counti*3+countj+1, disabled = True) if board[counti*3+countj]==0 else 
                Button(style = ButtonStyle.blue, label = "⭕", custom_id = counti*3+countj+1, disabled = True) if board[counti*3+countj]==1 else 
                Button(style = ButtonStyle.blue, label = "❌", custom_id = counti*3+countj+1, disabled = True) for countj in range(3)]for counti in range(3)]
            if turn == 1:
                player1 = await self.client.fetch_user(self.session[interaction.user.id][str(turn)])
                player2 = await self.client.fetch_user(self.session[interaction.user.id][str(turn+1)])
            elif turn == 2:
                player1 = await self.client.fetch_user(self.session[interaction.user.id][str(turn)])
                player2 = await self.client.fetch_user(self.session[interaction.user.id][str(turn-1)])
            await self.session[interaction.user.id]["message"].edit(f"{player1.mention} It is your turn!", components= components)
            await interaction.channel.send(f"{player1.mention} has won against {player2.mention}!")
            return await interaction.respond(type=6)
            
          elif (board[2] == board[4] == board[6] and board[4] == turn):
            components = [[
                Button(style = ButtonStyle.blue, label = "\u200b", custom_id = counti*3+countj+1, disabled = True) if board[counti*3+countj]==0 else 
                Button(style = ButtonStyle.blue, label = "⭕", custom_id = counti*3+countj+1, disabled = True) if board[counti*3+countj]==1 else 
                Button(style = ButtonStyle.blue, label = "❌", custom_id = counti*3+countj+1, disabled = True) for countj in range(3)]for counti in range(3)]
            if turn == 1:
                player1 = await self.client.fetch_user(self.session[interaction.user.id][str(turn)])
                player2 = await self.client.fetch_user(self.session[interaction.user.id][str(turn+1)])
            elif turn == 2:
                player1 = await self.client.fetch_user(self.session[interaction.user.id][str(turn)])
                player2 = await self.client.fetch_user(self.session[interaction.user.id][str(turn-1)])
            await self.session[interaction.user.id]["message"].edit(f"{player1.mention} It is your turn!", components= components)
            await interaction.channel.send(f"{player1.mention} has won against {player2.mention}!")
            return await interaction.respond(type=6)
        #if no win condition are met, continue the game
          for i in board:
            if i == 0:
              components = [[
                Button(style = ButtonStyle.blue, label = "\u200b", custom_id = counti*3+countj+1) if board[counti*3+countj]==0 else 
                Button(style = ButtonStyle.blue, label = "⭕", custom_id = counti*3+countj+1, disabled = True) if board[counti*3+countj]==1 else 
                Button(style = ButtonStyle.blue, label = "❌", custom_id = counti*3+countj+1, disabled = True) for countj in range(3)]for counti in range(3)]
              if turn == 1:
                self.session[interaction.user.id]["turn"] += 1
                player1 = await self.client.fetch_user(self.session[interaction.user.id][str(turn+1)])
            
              elif turn == 2:
                self.session[interaction.user.id]["turn"] = 1
                player1 =  await self.client.fetch_user(self.session[interaction.user.id][str(turn-1)])
              
              await self.session[interaction.user.id]["message"].edit(f"{player1.mention} It is your turn!", components= components)
              return await interaction.respond(type=6)
          
          components = [[
                Button(style = ButtonStyle.blue, label = "\u200b", custom_id = counti*3+countj+1, disabled = True) if board[counti*3+countj]==0 else 
                Button(style = ButtonStyle.blue, label = "⭕", custom_id = counti*3+countj+1, disabled = True) if board[counti*3+countj]==1 else 
                Button(style = ButtonStyle.blue, label = "❌", custom_id = counti*3+countj+1, disabled = True) for countj in range(3)]for counti in range(3)]
          if turn == 1:
                player1 = await self.client.fetch_user(self.session[interaction.user.id][str(turn)])
                player2 = await self.client.fetch_user(self.session[interaction.user.id][str(turn+1)])
          elif turn == 2:
                player1 = await self.client.fetch_user(self.session[interaction.user.id][str(turn)])
                player2 = await self.client.fetch_user(self.session[interaction.user.id][str(turn-1)])
          await self.session[interaction.user.id]["message"].edit(f"{player1.mention} It is your turn!", components= components)
          await interaction.channel.send(f"{player1.mention} has tied against {player2.mention}!")
          return await interaction.respond(type=6)
    
    except discord.NotFound:
      return
    except:
      return
  
def setup(client):
  client.add_cog(tictactoe(client))



    