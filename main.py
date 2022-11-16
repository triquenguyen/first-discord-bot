import discord
from discord.ext import commands

intents = discord.Intents.default()                        
intents.message_content = True                           
client = commands.Bot(command_prefix='.', help_command=None, intents=intents)

op = {'+': lambda x, y: x + y,
      '-': lambda x, y: x - y,
      '/': lambda x, y: x / y,
      '*': lambda x, y: x * y}

@client.command()
async def calc(ctx, num1, operator, num2):
  try:
    num1 = int(num1)
  except ValueError:
    await ctx.send(f"{num1} is not a number!")
    return

  try:
    num2 = int(num2)     
  except ValueError:
    await ctx.send(f"{num2} is not a number!")
    return

  try:
    result = op[operator](num1, num2)
  except ZeroDivisionError: 
    await ctx.send("You can't divide by zero!")
    return
  except:
    await ctx.send("You must use '+', '-', '*', or '/'!")
    return
      
  await ctx.send(f"{num1} {operator} {num2} = {result}")

with open("key.txt", "r") as readFile:
  botToken = readFile.readline() 
client.run(botToken)
