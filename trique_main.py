from discord.ext import commands
import discord
import json
import os.path
import asyncio

intents = discord.Intents.default()                        
intents.message_content = True                           
client = commands.Bot(command_prefix='&', help_command=None, intents=intents)

botTitle = "Homework Bot"
#----------------- CALCULATIONS --------------------------

op = {'+': lambda x, y: x + y,
      '-': lambda x, y: x - y,
      '/': lambda x, y: x / y,
      '*': lambda x, y: x * y}

@client.command()
async def calc(ctx, num1, operator, num2):
  try:
    num1 = float(num1)
  except ValueError:
    await ctx.send(f"{num1} is not a number!")
    return

  try:
    num2 = float(num2)     
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
      
  await ctx.send(f"{num1} {operator} {num2} = {round(result,2)}")


#-------------------- SHOPPING LIST -------------------------

#------- Create Shopping List -------

@client.command()
async def createShoppingList(ctx):
  if os.path.exists(f"./profiles/{ctx.author.id}.json"):
    await ctx.send("You already have a shopping list!")
    return

  with open('initShoppingList.json', 'r') as initFile:
    data = json.load(initFile)

  with open(f"./profiles/{ctx.author.id}.json", "w") as userList:
    json.dump(data, userList)    

  await ctx.send("List created")

#------- Set Store -------

@client.command()
async def setStore(ctx):

  stores = {
      "1": "Walmart",
      "2": "Target",
      "3": "Costco",
      "4": "Other",
    }

  try: 
    with open(f"./profiles/{ctx.author.id}.json", "r") as readFile:
        userList = json.load(readFile)
  
    store_options = discord.Embed(title=botTitle, description="Please select your store\n" + "1. Walmart\n" + "2. Target\n" + "3. Costco\n" + "4. Other")           
    store_options.colour = discord.Colour.purple()   
    await ctx.send(embed=store_options)  

  except FileNotFoundError:
    file_not_found_error = discord.Embed(title=botTitle, description="You don't have a shopping list! do `-createShoppingList` to make one")           
    file_not_found_error.colour = discord.Colour.red()   
    await ctx.send(embed=file_not_found_error)              
    return

  try:
    msg = await client.wait_for("message", timeout=30)
    
  except asyncio.TimeoutError:                           
      time_out_error = discord.Embed(title=botTitle, description="You ran out of time. Try again!")           
      time_out_error.colour = discord.Colour.red()   
      await ctx.send(embed=time_out_error)              
      return

  if msg.content in stores:
    store = stores[msg.content]
    userList["STORE"] = store

    msg = discord.Embed(title=botTitle, description=f"Success! Your store is now {store}")           
    msg.colour = discord.Colour.purple()   
  
    with open(f"./profiles/{ctx.author.id}.json", "w") as writeFile:        
      json.dump(userList, writeFile)
  else:
    await ctx.send("Please select a number from the list. Command terminated")               
    return

  await ctx.send(embed=msg)  

#------ Add To List -----

@client.command()
async def addToList(ctx, *items):
  

  try:
    with open(f"./profiles/{ctx.author.id}.json", "r") as readFile:
      userList = json.load(readFile)

  except FileNotFoundError:
    file_not_found_error = discord.Embed(title=botTitle, description="You don't have a shopping list! do `-createShoppingList` to make one")           
    file_not_found_error.colour = discord.Colour.red()   
    await ctx.send(embed=file_not_found_error)              
    return

  if (len(items) == 0):
    type_error = discord.Embed(title=botTitle, description="Please type in the items you want to add after the command!")           
    type_error.colour = discord.Colour.red()   
    await ctx.send(embed=type_error)              
    return 
  

  curr_add_items = []

  for item in items:
    userList["LIST"].append(item)
    curr_add_items.append(item)

  msg = ', '.join(curr_add_items)
    
  list_msg = userList["LIST"]

  with open(f"./profiles/{ctx.author.id}.json", "w") as writeFile:        
      json.dump(userList, writeFile)
  
  item_list = discord.Embed(title=botTitle, description=f"Added the following items:\n {msg}")
  item_list.colour = discord.Colour.green()   
  await ctx.send(embed=item_list)                   

#------- Show List -------
@client.command()
async def showItems(ctx):
  try:
    with open(f"./profiles/{ctx.author.id}.json", "r") as readFile:
      userList = json.load(readFile)

    store = userList["STORE"]
    msg = ', '.join(userList["LIST"])

  except FileNotFoundError:
    file_not_found_error = discord.Embed(title=botTitle, description="You don't have a shopping list! do `-createShoppingList` to make one")           
    file_not_found_error.colour = discord.Colour.red()   
    await ctx.send(embed=file_not_found_error)              
    return

  user_list = discord.Embed(title=botTitle)
  user_list.description = f"**{ctx.author.name}#{ctx.author.discriminator}** list:\n **Store:** {store}\n **Items:** {msg}" 
  user_list.colour = discord.Colour.purple()   
  await ctx.send(embed=user_list) 

#------ Clear List --------
@client.command()
async def clearList(ctx):
  try: 
    with open(f"./profiles/{ctx.author.id}.json", "r") as readFile:
      userList = json.load(readFile)
  except FileNotFoundError:
    file_not_found_error = discord.Embed(title=botTitle, description="You don't have a shopping list! do `-createShoppingList` to make one")           
    file_not_found_error.colour = discord.Colour.red()   
    await ctx.send(embed=file_not_found_error)              
    return
  
  userList["LIST"].clear()

  with open(f"./profiles/{ctx.author.id}.json", "w") as writeFile:        
    json.dump(userList, writeFile)

  embed = discord.Embed(title=botTitle, description='Shopping list cleared')
  embed.colour = discord.Colour.green()   
  await ctx.send(embed=embed) 

with open("key.txt", "r") as readFile:
  botToken = readFile.readline() 
client.run(botToken)
