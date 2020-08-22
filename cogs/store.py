import discord
import ast
import os
import json
from discord.ext import commands

os.chdir(r"D:\Discordbot\DotaQuizbot")

#The store system:
store_items = {"Hand of Midas":2200, "Octarine Core":5000, '''Shiva's guard''':4850,
"Aegis of the Immortal":8000, "Cheese":30000,}
store_descriptions = {"Hand of Midas":"Earn bonus gold.", "Cheese":"Waste of money.", "Octarine Core":"Lower cooldowns for commands.",
'''Shiva's guard''':"Have more time during time based commands.", "Aegis of the Immortal":"One extra life on Shopquiz and Endless."}
storekeys, storevalues = list(store_items.keys()), list(store_items.values())

#with open("users.json", "r") as fp:      #load the users.json file
#        users = json.load(fp)

def open_json(jsonfile):
    with open(jsonfile, "r") as fp:      #load the users.json file
        return json.load(fp)       #openfunc for jsonfiles

def save_json(jsonfile, name):                         #savefunc for jsonfiles
    with open(jsonfile, "w") as fp:
        json.dump(name, fp)

def add_gold(user: discord.User, newgold: int):           #add gold to users
    id = str(user.id)
    if id not in users.keys():                  #if user not already in users.json add user
        users[id] = {"gold" : 10, "items":"[]"}
        users[id]["gold"] = users[id]["gold"] + round(newgold)
        return round(newgold)
        save_json("users.json", users)
    else:
        if 2200 in ast.literal_eval(users[id]["items"]):
            users[id]["gold"] = users[id]["gold"] + round(newgold*1.25)
            return round(newgold*1.25)
            save_json("users.json", users)
        else:
            users[id]["gold"] = users[id]["gold"] + round(newgold)
            return round(newgold)
            save_json("users.json", users)

def strip_str(text):                 #function to remove punctuations spaces from string and make it lowercase
    punctuations = ''' !-;:'`"\,/_?'''
    text2 = ""
    for char in text:
       if char not in punctuations:
           text2 = text2 + char
    return text2.lower().replace("the", "")

def take_index(l1, l2):               #Function to find the index of items in a list that are available in another list
    indexi = []
    for index, item in enumerate(l1):
        if item in l2:
            indexi.append(index)
    return indexi

class Store(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #store commands
    @commands.command(brief = "Check how much gold you own.")
    async def gold(self, ctx):
        users = open_json("users.json")
        if str(ctx.author.id) in users.keys():
            authorgold = users[str(ctx.author.id)]["gold"]
            await ctx.send(f"**{ctx.author.display_name}** you currently have **``{authorgold}``** gold.")
        else:
            await ctx.send("""You haven't got any gold yet, try "322 help" and use Quiz commands to earn some.""")

    @commands.command(brief = "Buy an item from the store.")
    async def buy(self, ctx, *, purchase):
        users = open_json("users.json")
        id = str(ctx.author.id)
        if id not in users.keys():                  #if user not already in users.json add user
            users[id] = {"gold":10, "items":"[]"}
            save_json("users.json", users)

        purchasestr = strip_str(purchase)
        if purchasestr not in [strip_str(x) for x in storekeys]:
            await ctx.send("That item doesn't exist.")             #<<
        else:                                                      #list of user items is stored as the item prices in json file
            user_items = ast.literal_eval(users[id]["items"])    #turn string of list into list
            user_gold = users[id]["gold"]
            itemindex = [strip_str(x) for x in storekeys].index(purchasestr)  #get the index of the item being purchased
            if storevalues[itemindex] in user_items:               #if item is already bought
                await ctx.send("You already have that item.")
            elif storevalues[itemindex] > user_gold:               #if item is too expensive
                await ctx.send(f"You don't have enough gold, this item costs {storevalues[itemindex]} gold.")
            else:                                              #item being purchased
                user_items.append(storevalues[itemindex])       #new item price is appended to users item list
                users[id]["items"] = str(user_items)          #update the list back as a string of a list
                users[id]["gold"] = users[id]["gold"] - storevalues[itemindex] #take away gold
                await ctx.send("You have purchased the item.")
                save_json("users.json", users)

    @commands.command(brief = "Sell an item from your inventory.")
    async def sell(self, ctx, *, itemtosell):
        users = open_json("users.json")
        id = str(ctx.author.id)
        soldstr = strip_str(itemtosell)                      #stripped item to be sold
        user_items = ast.literal_eval(users[id]["items"])       #user inventory
        strippeditems = [strip_str(x) for x in storekeys]        #list of stripped store items
        if soldstr in strippeditems:                        #if item exists
            itemindex = strippeditems.index(soldstr)      #gets index to get item's cost
            itemcost = storevalues[itemindex]
            if itemcost in user_items:                #if item is inside user inventory
                user_items.remove(itemcost)           #remove the item from inventory, add half the gold in
                save_json("users.json", users)
                users[id]["items"] = str(user_items)
                users[id]["gold"] = users[id]["gold"] + int(itemcost/2)
                await ctx.send(f"You sold the item for {int(itemcost/2)} gold.")
                save_json("users.json", users)
            else:                             #if item exists but isn't in the inventory
                await ctx.send("You don't have that item in your inventory in order to sell it.")
        else:                         #if item doesn't exist at all
            await ctx.send("That item doesn't exist in the store.")

    @commands.command(brief = "Check your inventory.")
    async def inventory(self, ctx):             #check inventory
        users = open_json("users.json")
        id = str(ctx.author.id)
        str_itemlist = ast.literal_eval(users[id]["items"])       #get list of items the user has(they're integers)
        if len(str_itemlist) == 0:                 #if inventory is empty
            await ctx.send("Your inventory is empty, try 322 buy to purchase items.")
        else:
            indexes = take_index(storevalues, str_itemlist)         #take the indexes the available items inside the list of all store items
            inventory = [storekeys[i] for i in indexes]          #create the actual list of strings of available inventory items
            items_listed = "``, ``".join(inventory)              #create a string to be put into the message
            await ctx.send(f"You have ``{items_listed}`` in your inventory.")

    @commands.command(brief = "See what items are available.")
    async def store(self, ctx):
        artifacts = ""
        for item in store_items:               #concatenates all the names and prices together to form a list of store items
            multiplier = 22 - len(item)
            multiplier2 = 9 - len(str(store_items[item]))
            artifacts = artifacts + item + (multiplier * " ") + str(store_items[item]) + (multiplier2 * " ") + store_descriptions[item] + " \n"
        await ctx.send(f"``` Item:             Price:   Description: \n{artifacts}```")

    @buy.error
    async def buyerror(self, ctx, error):
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send("""You need to specify what item you're purchasing, try "322 store" to see available items.""")


    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            pass
        else:
            raise error

def setup(bot):
    bot.add_cog(Store(bot))