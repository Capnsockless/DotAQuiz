import random
import discord
import asyncio
import json
import ast
import time
import os
from fuzzywuzzy import fuzz
from mutagen.mp3 import MP3
from discord.ext import commands

os.chdir(r"D:\Discordbot\DotaQuizbot")

#importing all quizes from quizdata
import quizdata
#questdict is for quiz, blitz, duel, freeforall, shopkeepdict is for shopquiz, iconquizdict - iconquiz, audioquiz - audioquiz, scramblelist - scramble
questdict, shopkeepdict, iconquizdict, audioquizdict, scramblelist = quizdata.questdict, quizdata.shopkeepdict, quizdata.iconquizdict, quizdata.audioquizdict, quizdata.scramblelist
#getting their lengths for the indicies, hence the -1
questlen, shopkeeplen, iconquizlen, audioquizlen, scramblelen = len(questdict)-1, len(shopkeepdict)-1, len(iconquizdict)-1, len(audioquizdict)-1, len(scramblelist)-1
#getting all of their keys and values as seperate lists
questkeys, questvalues = list(questdict.keys()), list(questdict.values())
shopkeepkeys, shopkeepvalues = list(shopkeepdict.keys()), list(shopkeepdict.values())
iconquizkeys, iconquizvalues = list(iconquizdict.keys()), list(iconquizdict.values())
audioquizkeys, audioquizvalues = list(audioquizdict.keys()), list(audioquizdict.values())

#lists of Replies in case of right, wrong or no/late answers
rightansw, wrongansw, lateansw = quizdata.rightansw, quizdata.wrongansw, quizdata.lateansw
#for scramble
charemojies = quizdata.charemojies
#Prize percentages for 322 freeforall
prizeperc = {0:0.6, 1:0.2, 2:0.1, 3:0.05, 4:0.05}

def open_json(jsonfile):
	with open(jsonfile, "r") as fp:
		return json.load(fp)	#openfunc for jsonfiles

def save_json(jsonfile, name):	#savefunc for jsonfiles
	with open(jsonfile, "w") as fp:
		json.dump(name, fp)

def prepare_quiz(user, server):		#checks user and server to make sure they're on rngfix.json and user.json, if not they will be added
	users = open_json("users.json")			#user
	id = str(user.id)
	if id not in users.keys():
		users[id] = {"gold":10, "items":"[]", "cheese":0}
		save_json("users.json", users)
	rng = open_json("rngfix.json")		#server
	serv_id = str(server.id)
	if serv_id not in rng.keys():
		rng[serv_id] = {"questnumbers":"[]", "shopkeepnumbers":"[]", "iconquiznumbers":"[]", "audioquiznumbers":"[]", "scramblenumbers":"[]", "vacuumcd":16}
		save_json("rngfix.json", rng)
	return users, rng

def unique_int_randomizer(server, length, listkey: str, rng):		#unique_int_randomizer used in par with the rngfix.json file to avoid repeating numbers(questions)
	serv_id = str(server.id)
	numlist = ast.literal_eval(rng[serv_id][listkey])			#convert list string to list
	if len(numlist) > length*7/8:			#if amount of numbers surpass 5/6ths of the total amount delete a chunk of the numbers at the start
		del numlist[:round(length/7)]
		save_json("rngfix.json", rng)
	while True:
		n = random.randint(0, length)
		if n not in numlist:		#get a number that isn't already used and append it to the list of numbers in use
			numlist.append(n)
			rng[serv_id][listkey] = str(numlist)		#convert list back to string list
			save_json("rngfix.json", rng)
			return n

def strip_str(text):		#function to remove punctuations, spaces and "the" from string and make it lowercase,
	punctuations = ''' !-;:`'"\,/_?'''			# in order to compare bot answers and user replies
	text2 = ""
	text1 = text.lower().replace("the ", "")
	for char in text1:
		if char not in punctuations:
			text2 = text2 + char
	return text2

class CompareOutput():		#class for compare_strings() to contain the answer which the user put in and also if it's correct or not
    def __init__(self, answer, success):
        self.answer = answer
        self.success = success

def find_correct_answer(dictvalue):			#function to find the correct answer to a quiz, used for all quiz commands except shopquiz
	if type(dictvalue) == str:
		return dictvalue
	elif type(dictvalue) == tuple:
		return dictvalue[0]
	else:
		return random.choice([z for z in dictvalue if z[0].isupper()])

def calc_time(question, answer):			#Function to calculate time for each question according to its size(for blitz)
	queslen = len(question)
	if type(answer) == str:			#takes the length of the raw answer
		answlen = len(answer)
	else:						#takes the average length of all answers
		answlen = sum(map(len, answer))/len(answer)
	seconds = queslen/11 + answlen/4
	return seconds

class Player():
	def __init__(self, author, users):
		self.author = author
		self.users = users
		try:
			self.inventory = ast.literal_eval(users[str(author.id)]["items"])
		except KeyError:
			self.inventory = []

	def compare_strings(self, text, answer):			#function to compare user input and actual answer
		striptext = strip_str(text)		#first we use strip_str on both strings which removes spaces, "the" and unwanted symbols
		if type(answer) == str:
			stripanswer = strip_str(answer)
			ratio = fuzz.ratio(striptext, stripanswer)
		else:						#if there are multiple answers we pick out the answer that is most similar to the input
			stripanswers = [strip_str(x) for x in answer]
			ratios = []
			for i in stripanswers:			#fill a list with levenshtein ratios
				ratios.append(fuzz.ratio(striptext, i))
			ratio = max(ratios)				#take the max value, its index and the actual string by the index
			answerindex = ratios.index(ratio)
			stripanswer = stripanswers[answerindex]		#just use stripanswer
		if 4852 in self.inventory:		#if user has monkey king bar they get away with more mistakes
			bool = (ratio > 86)	#change bool to 1 if it's correct
		else:
			bool = (ratio > 97)
		return CompareOutput(stripanswer, bool)         ###USER MUST BE IN users.json

	def add_gold(self, newgold):		#add gold to users
		id = str(self.author.id)
		if 2200 in self.inventory:
			self.users[id]["gold"] = self.users[id]["gold"] + round(newgold*1.2)
			save_json("users.json", self.users)
			return round(newgold*1.2)
		else:
			self.users[id]["gold"] = self.users[id]["gold"] + round(newgold)
			save_json("users.json", self.users)
			return round(newgold)

	def shiva(self, duration):				#Set duration for quiz commands(30% more time if shiva is held)
		if 4850 in self.inventory:
			duration *= 1.3
		return round(duration)

	def aegis(self, lives):				#Set amount of lives(+1 if the user has aegis)
		if 8000 in self.inventory:
			lives += 1
		return lives

	def pirate_hat(self, plunder):		#Increase gold if user has pirate hat(used for duel)
		if 6500 in self.inventory:
			plunder += 10000
		return plunder

	def necronomicon(self, nquestions):		#Increase amount of questions if user has necronomicon(used for freeforall)
		if 4550 in self.inventory:
			nquestions += 10
		return nquestions

	def aeon_disk(self, ncorrectanswsinarow):		#only halve the amount of correct answers in a row instead of clearing them
		if 3100 in self.inventory:
			ncorrectanswsinarow = round(ncorrectanswsinarow / 2)
		else:
			ncorrectanswsinarow = 0
		return ncorrectanswsinarow

class Quizes(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(brief = "A single DotA related question for a bit of gold.")
	@commands.cooldown(1, 7, commands.BucketType.user)
	async def quiz(self, ctx):
		server, channel, author = ctx.guild, ctx.channel, ctx.author		#the server, channel and author of the command activator
		users, rng = prepare_quiz(author,server)
		player = Player(author, users)
		questn = unique_int_randomizer(server, questlen, "questnumbers", rng)			#Random number to give a random question
		correctansw = find_correct_answer(questvalues[questn])		#Find the correct answer to be displayed incase user gets it wrong
		if type(questkeys[questn]) == tuple:			#if the question comes with an image
			await ctx.send(f"**```{questkeys[questn][0]}```**", file=discord.File(f"./quizimages/{questkeys[questn][1]}"))
		else:											#for normal string questions
			await ctx.send(f"**```{questkeys[questn]}```**")
		def check(m):
			return m.channel == channel and m.author == author		#checks if the reply came from the same person in the same channel
		try:
			msg = await self.bot.wait_for("message", check=check, timeout=player.shiva(22.322))
		except asyncio.TimeoutError:		#If too late
			await channel.send(f"**{random.choice(lateansw)}** The correct answer was ``{correctansw}``")
		else:
			if player.compare_strings(msg.content, questvalues[questn]).success:
				g = player.add_gold(16)
				await channel.send(f"**{random.choice(rightansw)}** you got ``{g}`` gold.")
			else:
				if type(questvalues[questn]) == list:
					await channel.send(f"**{random.choice(wrongansw)}** One of the possible correct answer was ``{correctansw}``")
				else:
					await channel.send(f"**{random.choice(wrongansw)}** The correct answer was ``{correctansw}``")

	@commands.command(brief = "Endlessly sends DotA 2 ability icons to name.")
	@commands.cooldown(1, 50, commands.BucketType.user)
	async def iconquiz(self, ctx):
		server, channel, author = ctx.guild, ctx.channel, ctx.author	#the server, channel and author of the command activator
		users, rng = prepare_quiz(author,server)
		player = Player(author, users)
		lives = player.aegis(3)
		accumulated_g = 0
		ncorrectansws = 0
		ncorrectanswsinarow = 0
		while True:
			if lives < 0.4:		#ncorrectansws*(accumulated_g+ncorrectansws-1)
				g = player.add_gold(accumulated_g)		#((2a+d(n-1))/2)n a = accumulated_g d = 2  n = ncorrectansws
				await ctx.send(f"You ran out of lives, you got ``{ncorrectansws}`` correct answers and accumulated ``{g}`` gold.")
				break
			elif lives == 322:
				g = player.add_gold(accumulated_g)		#((2a+d(n-1))/2)n a = accumulated_g d = 2  n = ncorrectansws
				await ctx.send(f"You have stopped the iconquiz, you got ``{ncorrectansws}`` correct answers and accumulated ``{g}`` gold.")
				break
			iconn = unique_int_randomizer(server, iconquizlen, "iconquiznumbers", rng)	#Random number to give a random icon
			correctansw = find_correct_answer(iconquizvalues[iconn])	#Find the correct answer to be displayed incase user gets it wrong
			await ctx.send(f"**``Name the shown ability.``**", file=discord.File(f"./iconquizimages/{iconquizkeys[iconn]}"))
			def check(m):
				return m.channel == channel and m.author == author		#checks if the reply came from the same person in the same channel
			try:
				msg = await self.bot.wait_for("message", check=check, timeout=player.shiva(13.322))
			except asyncio.TimeoutError:			#If too late
				lives -= 1
				await channel.send(f"**{random.choice(lateansw)}** The correct answer was ``{correctansw}``, ``{lives}`` lives remaining.")
				accumulated_g -= 10
				ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
			else:
				if strip_str(msg.content) == "skip":
					lives -= 0.5
					ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
					await ctx.send(f"The correct answer was ``{correctansw}``, you have ``{lives}`` lives remaining.")
				elif strip_str(msg.content) == "stop":
					lives = 322
				elif player.compare_strings(msg.content, iconquizvalues[iconn]).success:
					await channel.send(f"**{random.choice(rightansw)}**")
					accumulated_g += 16 + 2*ncorrectanswsinarow
					ncorrectansws, ncorrectanswsinarow = ncorrectansws + 1, ncorrectanswsinarow + 1
				else:
					lives -= 1
					ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
					await channel.send(f"**{random.choice(wrongansw)}** The correct answer was ``{correctansw}``, ``{lives}`` lives remaining.")

	@commands.command(brief = "Recognize DotA2 words among scrambled letters.")
	@commands.cooldown(1, 8, commands.BucketType.user)
	async def scramble(self, ctx):
		server, channel, author = ctx.guild, ctx.channel, ctx.author		#the server, channel and author of the command activator
		users, rng = prepare_quiz(author,server)
		player = Player(author, users)
		scramblen = unique_int_randomizer(server, scramblelen, "scramblenumbers", rng)			#Random number to give a random question
		correctansw = scramblelist[scramblen]			#the correct answer
		scrambledworde = []			#empty list to .join() emojies onto
		charlist = list(correctansw.lower().replace("'", ""))			#converting string to list
		for char in random.sample(charlist, len(charlist)):		#shuffling the word list and looping through it
			scrambledworde.append(charemojies[char])		#picking up values of charemojies of the lowercase characters
		output = " ".join(scrambledworde)					#joining them to form a string of all emojies to output
		await ctx.send(f"**``Unscramble this word:``**\n{output}")
		def check(m):
			return m.channel == channel and m.author == author		#checks if the reply came from the same person in the same channel
		try:
			msg = await self.bot.wait_for("message", check=check, timeout=player.shiva(25.322))
		except asyncio.TimeoutError:		#If too late
			await channel.send(f"**{random.choice(lateansw)}** The correct answer was ``{correctansw}``")
		else:
			if player.compare_strings(msg.content, correctansw).success:
				g = player.add_gold(100)
				await channel.send(f"**{random.choice(rightansw)}** you got ``{g}`` gold.")
			else:
				await channel.send(f"**{random.choice(wrongansw)}** The correct answer was ``{correctansw}``")

	@commands.command(brief = "Endlessly sends DotA2 items to be assembled.")
	@commands.cooldown(1, 50, commands.BucketType.user)
	async def shopquiz(self, ctx):
		server, channel, author = ctx.guild, ctx.channel, ctx.author		#get users server, channel and author
		users, rng = prepare_quiz(author,server)
		player = Player(author, users)
		accumulated_g = 0			#gold that will be given to the user at the end
		lives = player.aegis(3)		#tries they have for the shopkeeperquiz
		ncorrectansws = 0			#number of items they completed
		ncorrectanswsinarow = 0
		while True:					#while lives are more than 0 it keeps sending new items to build once the previous item is completed/skipped
			if lives <= 0.4:		#ends the shopquiz
				g = player.add_gold(accumulated_g)		#a = accumulated_g, d = 10, n = ncorrectansws
				await ctx.send(f"**{author.display_name}** You're out of lives, You built ``{ncorrectansws}`` items and accumulated ``{g}`` gold during the Shopkeepers Quiz.")
				break
			elif lives == 322:		#if the quiz is stopped by command
				g = player.add_gold(accumulated_g)		#a = accumulated_g, d = 10, n = ncorrectansws
				await ctx.send(f"**{author.display_name}** You built ``{ncorrectansws}`` items and accumulated ``{g}`` gold during the Shopkeepers Quiz.")
				break
			shopkeepn = unique_int_randomizer(server, shopkeeplen, "shopkeepnumbers", rng)
			#create two lists of correct answers, itemanswers takes in stripped correct answers inside multiple lists while itemanswersmerged takes it all as one list
			itemanswers, itemanswersmerged = [], []
			if type(shopkeepvalues[shopkeepn][0]) == list:
				correctansw = "``, ``".join(shopkeepvalues[shopkeepn][0])			#creates a highlighted string of correct items
				for index, items in enumerate(shopkeepvalues[shopkeepn]):
					itemanswers.append([])			#to create a list within a list which gets appended later
					for answ in items:
						itemanswers[index].append(strip_str(answ))
						itemanswersmerged.append(strip_str(answ))
			else:
				correctansw = "``, ``".join(shopkeepvalues[shopkeepn])			#creates a highlighted string of correct items
				for k in shopkeepvalues[shopkeepn]:
					itemanswers.append(strip_str(k))
					itemanswersmerged.append(strip_str(k))

			await ctx.send("List the items that are required to assemble the shown item **One By One**.", file=discord.File(f"./shopkeepimages/{shopkeepkeys[shopkeepn]}"))
			while True:						#while item is yet to be completed it takes in answers, checks them and uses them
				if len(itemanswersmerged) == 0:			#stops the single item answer collecting
					accumulated_g += 40 + 11*ncorrectanswsinarow
					ncorrectansws, ncorrectanswsinarow = ncorrectansws + 1, ncorrectanswsinarow + 1
					await ctx.send("*Item complete.*")
					break
				elif lives == 322 or lives <= 0.4:
					await ctx.send(f"You could've built this item with ``{correctansw}``.")
					break

				def check(m):
					return m.channel == channel and m.author == author
				try:
					msg = await self.bot.wait_for("message", check=check, timeout=player.shiva(20.322))
				except asyncio.TimeoutError:					#If too late
					lives -= 1
					await channel.send(f"**{random.choice(lateansw)}**, you have ``{lives}`` lives remaining.")
					accumulated_g -= 10
					ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
				else:
					if strip_str(msg.content) == "stop":		#changes lives number to 322 and stops the quiz
						lives = 322
						break
					elif strip_str(msg.content) == "skip":		#skip a single item and lose 0.5 life for it
						lives -= 0.5
						ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
						await ctx.send(f"This item could've been built with ``{correctansw}``, you have ``{lives}`` lives remaining.")
						break
					elif type(itemanswers[0]) == list:					#if itemanswers has lists of correct answers it checks the correct answ in
						if player.compare_strings(msg.content, itemanswersmerged).success:			#itemanswersmerged, gives reward
							await ctx.send(f"**{random.choice(rightansw)}**")
							accumulated_g += 2
							itemstopop = []					#create a new list of items that must be removed from itemanswersmerged
							for itemlist in itemanswers:
								result = player.compare_strings(msg.content, itemlist)
								if result.success:					#check index of correct answer to remove from all lists of itemanswers
									n = itemlist.index(result.answer)
							for index, itemlist in enumerate(itemanswers):
								itemstopop.append(itemanswers[index][n])
								itemanswers[index].pop(n)			#pop answered item out of all lists of the itemanswers
							for item in itemstopop:				#loop through itemstopop and remove each item of it from itemanswersmerged
								itemanswersmerged.remove(item)
						else:
							lives -= 1
							ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
							await ctx.send(f"**{random.choice(wrongansw)}** you have ``{lives}`` lives remaining.")
					else:
						result = player.compare_strings(msg.content, itemanswersmerged)
						if result.success:			#if itemanswers is just a list of strings, remove answered item from both lists.
							await ctx.send(f"**{random.choice(rightansw)}**")
							accumulated_g += 3
							itemanswers.remove(result.answer)
							itemanswersmerged.remove(result.answer)
						else:
							lives -= 1
							ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
							await ctx.send(f"**{random.choice(wrongansw)}** you have ``{lives}`` lives remaining.")

	@commands.command(brief = "Plays DotA2 sound effects to recognize.")
	@commands.cooldown(1, 50, commands.BucketType.user)
	async def audioquiz(self, ctx):
		server, channel, author = ctx.guild, ctx.channel, ctx.author		#get users server, channel and author
		users, rng = prepare_quiz(author,server)
		player = Player(author, users)
		timeout = time.time() + player.shiva(37)						#timeout set
		accumulated_g = 0													#gold that will be given to the user at the end
		ncorrectansws = 0													#number of sounds they answered
		if author.voice is None:								#if user not in a vc
			await ctx.send("You must be in a visible voice channel to use this command.")
			self.audioquiz.reset_cooldown(ctx)
		else:
			voicechannel = await author.voice.channel.connect()
			await ctx.send(f"""You have base ``{player.shiva(37)}`` seconds for the audioquiz each correct answer grants you 3 more seconds, answer which **item** or **spell** makes the played sound effect, don't forget to type in **skip** to entirely skip the sound effect.""")
			time.sleep(2.4)
			while True:
				if time.time() > timeout:			#stop the quiz, add accumulated gold to user.
					g = player.add_gold(ncorrectansws*(accumulated_g+(2*ncorrectansws)-2))		#((2a+d(n-1))/2)n a = 0 d = 4  n = ncorrectanswsers
					await ctx.send(f"**{author.display_name}** you got ``{ncorrectansws}`` correct answers and accumulated ``{g}`` gold during the audioquiz.")
					await ctx.voice_client.disconnect()
					break
				time.sleep(0.3)
				audion = unique_int_randomizer(server, audioquizlen, "audioquiznumbers", rng)		#Random number to give a random audioion
				correctansw = find_correct_answer(audioquizvalues[audion])	#find correct answer to display later
				duration = round(MP3(f".\soundquizaudio\{audioquizkeys[audion]}").info.length+3)   #duration of the audiofile in seconds
				source = await discord.FFmpegOpusAudio.from_probe(f".\soundquizaudio\{audioquizkeys[audion]}")	#convert audio to opus
				ctx.voice_client.stop()			#stop audio to make sure next sound can play
				ctx.voice_client.play(source)
				def check(m):
					return m.channel == channel and m.author == author		#checks if the reply came from the same person in the same channel
				try:					#vvvv calc_time() takes strings as arguments so duration is converted to a string by multiplying "a"
					msg = await self.bot.wait_for("message", check=check, timeout=player.shiva(calc_time("a"*7*duration, audioquizvalues[audion])))
				except asyncio.TimeoutError:			#If too late
					await channel.send(f"**{random.choice(lateansw)}**, The correct answer was ``{correctansw}``.")
					accumulated_g -= 10
				else:
					if strip_str(msg.content) == "skip":		#if user wants to move onto the next audioion
						accumulated_g -= 4
						if type(audioquizvalues[audion]) == str or type(audioquizvalues[audion]) == tuple:
							await channel.send(f"The correct answer was ``{correctansw}``.")
						else:
							await channel.send(f"One of the possible answers was ``{correctansw}``.")
					elif strip_str(msg.content) == "stop" or strip_str(msg.content) == "stfu":		#if user stops the quiz
						timeout = 35
					elif player.compare_strings(msg.content, audioquizvalues[audion]).success:	#If there is one correct answer
						await ctx.send(f"**{random.choice(rightansw)}**")
						timeout += 3.2							#add time before timeout for every correct answer
						accumulated_g += 14
						ncorrectansws += 1
					else:
						accumulated_g -= 4
						if type(audioquizvalues[audion]) == list:
							await channel.send(f"**{random.choice(wrongansw)}** One of the possible answers was ``{correctansw}``")
						else:
							await channel.send(f"**{random.choice(wrongansw)}** The correct answer was ``{correctansw}``.")

	@commands.command(brief = "Rapid questions that give more gold but with a risk.")
	@commands.cooldown(1, 52, commands.BucketType.channel)
	async def blitz(self, ctx):
		server, channel, author = ctx.guild, ctx.channel, ctx.author
		users, rng = prepare_quiz(author,server)
		player = Player(author, users)
		timeout = time.time() + player.shiva(50)		#full time for blitz round
		accumulated_g = 0
		ncorrectansws = 0
		await ctx.send(f"""You have ``{player.shiva(48)}`` seconds for the blitz, don't forget to type in **skip** if you don't know the answer to minimize the gold and time you lose.""")
		time.sleep(3.7)
		while True:
			time.sleep(0.3)
			if time.time() > timeout:			#stop the blitz, add accumulated gold to user.
				g = player.add_gold(ncorrectansws*(accumulated_g+(2*ncorrectansws)-2))		#((2a+d(n-1))/2)n a = 0 d = 4  n = ncorrectanswsers
				await ctx.send(f"**{author.display_name}** you got ``{ncorrectansws}`` correct answers and accumulated ``{g}`` gold during the blitz.")
				break
			questn = unique_int_randomizer(server, questlen, "questnumbers", rng)		#Random number to give a random question
			correctansw = find_correct_answer(questvalues[questn])
			if type(questkeys[questn]) == tuple:		#if the question comes with an image
				await ctx.send(f"**```{questkeys[questn][0]}```**", file=discord.File(f"./quizimages/{questkeys[questn][1]}"))
				giventime = player.shiva(calc_time(questkeys[questn][0], questvalues[questn]))
			else:										#for normal string questions
				await ctx.send(f"**```{questkeys[questn]}```**")
				giventime = player.shiva(calc_time(questkeys[questn], questvalues[questn]))
			def check(m):
				return m.channel == channel and m.author == author		#checks if the reply came from the same person in the same channel
			try:
				msg = await self.bot.wait_for("message", check=check, timeout=giventime)
			except asyncio.TimeoutError:			#If too late
				await channel.send(f"**{random.choice(lateansw)}**, The correct answer was ``{correctansw}``.")
				accumulated_g -= 21
			else:
				if strip_str(msg.content) == "skip":		#if user wants to move onto the next question
					accumulated_g -= 4
					if type(questvalues[questn]) == str or type(questvalues[questn]) == tuple:
						await channel.send(f"The correct answer was ``{correctansw}``.")
					else:
						await channel.send(f"One of the possible answers was ``{correctansw}``.")
				elif player.compare_strings(msg.content, questvalues[questn]).success:		#If there is one correct answer
					accumulated_g += 14
					ncorrectansws += 1
				else:
					accumulated_g -= 12
					if type(questvalues[questn]) == list:
						await channel.send(f"**{random.choice(wrongansw)}** One of the possible answers was ``{correctansw}``")
					else:
						await channel.send(f"**{random.choice(wrongansw)}** The correct answer was ``{correctansw}``.")

	@commands.command(brief = "Duel another user for gold.")
	@commands.cooldown(1, 45, commands.BucketType.channel)
	async def duel(self, ctx, opponent: discord.Member, wager:int):
		server, channel, author = ctx.guild, ctx.channel, ctx.author			#the server, channel and author of the command activator
		users, rng = prepare_quiz(author,server)
		player1 = Player(author, users)
		maxwager = player1.pirate_hat(10000)
		if str(opponent.id) not in users.keys():
			await ctx.send("That user doesn't have any gold to duel.")
			self.duel.reset_cooldown(ctx)
		elif author == opponent:
			await ctx.send("Why are you trying to duel yourself?")
			self.duel.reset_cooldown(ctx)
		elif wager < 300:
			await ctx.send("The minimum wager of a duel is 300 gold.")
			self.duel.reset_cooldown(ctx)
		elif wager > maxwager:
			await ctx.send(f"The maximum wager you can set is {maxwager} gold.")
			self.duel.reset_cooldown(ctx)
		elif users[str(ctx.author.id)]["gold"] < wager:
			await ctx.send("You don't have enough gold to start a duel.")
			self.duel.reset_cooldown(ctx)
		elif users[str(opponent.id)]["gold"] < wager:
			await ctx.send("Your chosen opponent doesn't have enough gold to start a duel.")
			self.duel.reset_cooldown(ctx)
		else:
			await ctx.send(f"{opponent.mention} Do you wish to duel {author.display_name} for {wager} gold? Write **Accept** in chat if you wish to duel or **Decline** if otherwise.")
			def check(m):
				return m.channel == channel and m.author == opponent		#checks if the reply came from the same person in the same channel
			try:
				msg = await self.bot.wait_for("message", check=check, timeout=25)
			except asyncio.TimeoutError:	#If too late
				await channel.send("The opponent didn't accept the duel.")
			else:
				if strip_str(msg.content) == "accept":
					player2 = Player(opponent, users)
					questionsasked = 0
					questionsanswered1 = 0
					questionsanswered2 = 0
					await ctx.send("The opponent has accepted the duel, ``15`` questions will be asked and the one to get the most amount of correct answers wins!")
					time.sleep(3.25)
					while True:
						time.sleep(0.75)
						if questionsasked == 15:
							if questionsanswered1 > questionsanswered2:
								winner = author
								loser = opponent
								g_win = player1.add_gold(wager-200)
								g_lose = player2.add_gold(-wager)
							else:
								winner = opponent
								loser = author
								g_win = player2.add_gold(wager-200)
								g_lose = player1.add_gold(-wager)
							await ctx.send(f"The winner is {winner.display_name}! {winner.display_name} you won ``{g_win}`` gold and {loser.display_name} lost ``{g_lose}``...")
							break

						questn = unique_int_randomizer(server, questlen, "questnumbers", rng)		#Random number to give a random question
						correctansw = find_correct_answer(questvalues[questn])	#Find the correct answer to be displayed incase user gets it wrong
						if type(questkeys[questn]) == tuple:			#if the question comes with an image
							await ctx.send(f"**```{questkeys[questn][0]}```**", file=discord.File(f"./quizimages/{questkeys[questn][1]}"))
							questionsasked += 1
						else:						#for normal string questions
							await ctx.send(f"**```{questkeys[questn]}```**")
							questionsasked += 1
						def check(m):
							return m.channel == channel and (m.author == author or opponent)		#checks if the reply came from the same person in the same channel
						try:
							msg = await self.bot.wait_for("message", check=check, timeout=20.322)
						except asyncio.TimeoutError:		#If too late
							await channel.send(f"**{random.choice(lateansw)}** The correct answer was ``{correctansw}``")
						else:
							if msg.author == author:
								if player1.compare_strings(msg.content, questvalues[questn]).success:		#If there is one correct answer
									await channel.send(f"**{random.choice(rightansw)}**")
									questionsanswered1 += 1
								else:
									if type(questvalues[questn]) == list:
										await channel.send(f"**{random.choice(wrongansw)}** One of the corrects answer was ``{correctansw}``")
									else:
										await channel.send(f"**{random.choice(wrongansw)}** The correct answer was ``{correctansw}``")
									questionsanswered1 -= 1
							else:
								if player2.compare_strings(msg.content, questvalues[questn]).success:		#If there is one correct answer
									await channel.send(f"**{random.choice(rightansw)}**")
									questionsanswered2 += 1
								else:
									if type(questvalues[questn]) == list:
										await channel.send(f"**{random.choice(wrongansw)}** One of the corrects answer was ``{correctansw}``")
									else:
										await channel.send(f"**{random.choice(wrongansw)}** The correct answer was ``{correctansw}``")
									questionsanswered2 -= 1

				else:
					await ctx.send("The opponent has declined the offer.")

	@commands.command(brief = "Set of quizes multiple people can answer.")
	@commands.cooldown(1, 80, commands.BucketType.channel)
	async def freeforall(self, ctx):
		server, channel, author = ctx.guild, ctx.channel, ctx.author		#the server, channel and author of the command activator
		users, rng = prepare_quiz(author, server)
		player = Player(author, users)
		usersdict = {author:0}			#dictionary that consists of all the participants and their points
		nquestions = player.necronomicon(25)		#number of questions that will be asked
		ncorrectansws = 0			#number of correctly answered questions by everyone
		while True:
			if nquestions <= 0:				#stop the quiz
				prizepool = 56*(ncorrectansws*(len(usersdict)**2))
				sortedusersdict = {k: v for k, v in sorted(usersdict.items(), key=lambda item: item[1], reverse=True)}	#sorting users according to
				sortedkeys, sortedvalues = list(sortedusersdict.keys()), list(sortedusersdict.values())	#their points and getting the keys and values
				basestr = "Participant: 		          Points:	    	Prize:\n"		#base of the ending message
				for i in range(0, len(sortedusersdict)):		#same here happens here as above but it only displays <5 users
					userprize = round(prizepool * prizeperc[i])
					if sortedvalues[i] > 0:
						tempplayer = Player(sortedkeys[i], users)
						g = tempplayer.add_gold(userprize)
					else:
						break
					multiplier1 = 35 - len(sortedkeys[i].display_name)
					multiplier2 = 15 - len(str(sortedvalues[i]))
					basestr = basestr + str(i + 1) + ")" + sortedkeys[i].display_name + " "*multiplier1 + str(sortedvalues[i]) + " "*multiplier2 + str(g) + " gold\n"
				await ctx.send(f"```{basestr}```")
				break
			time.sleep(0.35)
			nquestions -= 1
			decider = random.randint(0, 1)
			if decider == 0:			#regular questions
				questn = unique_int_randomizer(server, questlen, "questnumbers", rng)		#Random number to give a random question
				correctansw = find_correct_answer(questvalues[questn])
				if type(questkeys[questn]) == tuple:		#if the question comes with an image
					await ctx.send(f"**```{questkeys[questn][0]}```**", file=discord.File(f"./quizimages/{questkeys[questn][1]}"))
					giventime = calc_time(questkeys[questn][0], questvalues[questn])
				else:										#for normal string questions
					await ctx.send(f"**```{questkeys[questn]}```**")
					giventime = calc_time(questkeys[questn], questvalues[questn])
				def check(m):
					return m.channel == channel and m.author != self.bot.user		#checks if the reply came from the same channel
				counter = 0				#counter to allow only 3 incorrect answers before moving on
				while True:
					if counter >= 3:		#stopping the current one question
						if type(questvalues[questn]) == list:
							await channel.send(f"One of the possible answers was ``{correctansw}``")
						else:
							await channel.send(f"The correct answer was ``{correctansw}``")
						break
					try:
						msg = await self.bot.wait_for("message", check=check, timeout=giventime+6)
					except asyncio.TimeoutError:			#If too late instantly moves to next question
						await channel.send(f"**{random.choice(lateansw)}**, The correct answer was ``{correctansw}``.")
						break
					else:
						currentauthor = msg.author
						users1, rng1 = prepare_quiz(currentauthor, server)
						currentplayer = Player(currentauthor, users1)
						if currentplayer.compare_strings(msg.content, questvalues[questn]).success:		#If there is one correct answer
							await channel.send(f"**{random.choice(rightansw)}**")
							if currentauthor in list(usersdict.keys()):		#if user is already listed in the dict increment the correct answers
								usersdict[currentauthor] += 1
							else:											#if not set the new user as a key and set 1 correct answer
								usersdict.update({currentauthor:1})
							ncorrectansws += 1
							break
						else:			#if there are multiple answers
							await channel.send(f"**{random.choice(wrongansw)}**")
							if currentauthor in list(usersdict.keys()):		#if user is already listed in the dict increment the correct answers
								usersdict[currentauthor] -= 1			#take a point away if answer is wrong
							counter += 1
			else:
				iconn = unique_int_randomizer(server, iconquizlen, "iconquiznumbers", rng)	#Random number to give a random icon
				correctansw = find_correct_answer(iconquizvalues[iconn])	#Find the correct answer to be displayed incase user gets it wrong
				await ctx.send(f"**``Name the shown ability.``**", file=discord.File(f"./iconquizimages/{iconquizkeys[iconn]}"))
				def check(m):
					return m.channel == channel and m.author != self.bot.user		#checks if the reply came from the same channel
				counter = 0				#counter to allow only 3 incorrect answers before moving on
				while True:
					if counter >= 3:		#stopping the current one question
						if type(questvalues[questn]) == list:
							await channel.send(f"One of the possible answers was ``{correctansw}``")
						else:
							await channel.send(f"The correct answer was ``{correctansw}``")
						break
					try:
						msg = await self.bot.wait_for("message", check=check, timeout=10.322)
					except asyncio.TimeoutError:			#If too late
						await channel.send(f"**{random.choice(lateansw)}** The correct answer was ``{correctansw}``")
						break
					else:
						currentauthor = msg.author
						users1, rng1 = prepare_quiz(currentauthor, server)
						currentplayer = Player(currentauthor, users1)
						if currentplayer.compare_strings(msg.content, iconquizvalues[iconn]).success:
							await channel.send(f"**{random.choice(rightansw)}**")
							if currentauthor in list(usersdict.keys()):		#if user is already listed in the dict increment the correct answers
								usersdict[currentauthor] += 1
							else:											#if not set the new user as a key and set 1 correct answer
								usersdict.update({currentauthor:1})
							ncorrectansws += 1
							break
						else:
							await channel.send(f"**{random.choice(wrongansw)}**")
							if currentauthor in list(usersdict.keys()):		#if user is already listed in the dict increment the correct answers
								usersdict[currentauthor] -= 1			#take a point away if answer is wrong
							counter += 1

	@commands.command(brief = "Endless mix of questions, items and icons.")
	@commands.cooldown(1, 400, commands.BucketType.user)
	async def endless(self, ctx):
		server, channel, author = ctx.guild, ctx.channel, ctx.author		#the server, channel and author of the command activator
		users, rng = prepare_quiz(author,server)
		player = Player(author, users)
		try:
			if 4200 in ast.literal_eval(users[str(author.id)]["items"]):
				accumulated_g = 0		#accumulated gold during the quiz
				ncorrectansws = 0		#number of correct answers
				ncorrectanswsinarow = 0
				lives = player.aegis(5)
				while True:			#keeps asking questions till it breaks
					if lives < 0.4:		#break the whole command if lives are 0 or 322(which means the command was stopped by user)
						g = player.add_gold(accumulated_g)	#((2a+d(n-1))/2)n a = accumulated_g d = 2  n = ncorrectansws
						await ctx.send(f"You ran out of lives and you accumulated ``{g}`` gold by getting ``{ncorrectansws}`` correct answers.")
						break
					if lives == 322:
						g = player.add_gold(accumulated_g)	#((2a+d(n-1))/2)n a = accumulated_g d = 2  n = ncorrectansws
						await ctx.send(f"You have stopped the endless quiz, you accumulated ``{g}`` gold by getting ``{ncorrectansws}`` correct answers.")
						break
					decider = random.randint(0, 3)
					await ctx.send(decider)
					if decider == 0:		#if random number is 0 the question will be quiz
							questn = unique_int_randomizer(server, questlen, "questnumbers", rng)			#Random number to give a random question
							correctansw = find_correct_answer(questvalues[questn])		#obtaining the correct answer to display later
							if type(questkeys[questn]) == tuple:		#if the question comes with an image
								await ctx.send(f"**```{questkeys[questn][0]}```**", file=discord.File(f"./quizimages/{questkeys[questn][1]}"))
							else:					#for normal string questions
								await ctx.send(f"**```{questkeys[questn]}```**")
							def check(m):
								return m.channel == channel and m.author == author	#checks if the reply came from the same person in the same channel
							try:
								msg = await self.bot.wait_for("message", check=check, timeout=player.shiva(16.322))
							except asyncio.TimeoutError:	#If too late
								lives -= 1
								await channel.send(f"**{random.choice(lateansw)}**, the correct answer was ``{correctansw}``, ``{lives}`` lives left.")
								accumulated_g -= 15
								ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
							else:
								if strip_str(msg.content) == "skip":	#if user skips a question
									lives -= 0.5
									ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
									await ctx.send(f"The correct answer was ``{correctansw}``, you have ``{lives}`` remaining.")
								elif strip_str(msg.content) == "stop":	#if user stops the "endless" quiz
									lives = 322
								elif player.compare_strings(msg.content, questvalues[questn]).success:	#If there is only one correct answer
									accumulated_g += 14 + 2*ncorrectansws
									ncorrectansws, ncorrectanswsinarow = ncorrectansws + 1, ncorrectanswsinarow + 1
								else:
									lives -= 1
									ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
									if type(questvalues[questn]) == list:
										await ctx.send(f"**{random.choice(wrongansw)}** One of the possible answer was ``{correctansw}``, ``{lives}`` lives remaining.")
									else:
										await channel.send(f"**{random.choice(wrongansw)}** The correct answer was ``{correctansw}``, ``{lives}`` lives remaining.")

					elif decider == 1:	#if random integer is 1 the question is a single shopquiz
						shopkeepn = unique_int_randomizer(server, shopkeeplen, "shopkeepnumbers", rng)
						#create two lists of correct answers, itemanswers takes in stripped correct answers inside multiple lists while itemanswersmerged takes it all as one list
						itemanswers, itemanswersmerged = [], []
						if type(shopkeepvalues[shopkeepn][0]) == list:
							correctansw = "``, ``".join(shopkeepvalues[shopkeepn][0])	#creating string of highlighted correct answers
							for index, items in enumerate(shopkeepvalues[shopkeepn]):
								itemanswers.append([])	#to create a list within a list which gets appended later
								for answ in items:
									itemanswers[index].append(strip_str(answ))
									itemanswersmerged.append(strip_str(answ))
						else:
							correctansw = "``, ``".join(shopkeepvalues[shopkeepn])	#creating string of highlighted correct answers
							for k in shopkeepvalues[shopkeepn]:
								itemanswers.append(strip_str(k))
								itemanswersmerged.append(strip_str(k))

						await ctx.send("List the items that are required to assemble the shown item **One By One**.", file=discord.File(f"./shopkeepimages/{shopkeepkeys[shopkeepn]}"))
						while True:		#while item is yet to be completed it takes in answers, checks them and uses them
							if len(itemanswersmerged) == 0:		#stops the individual item answer collecting
								ncorrectansws, ncorrectanswsinarow = ncorrectansws + 1, ncorrectanswsinarow + 2
								accumulated_g += 48 + 2*ncorrectanswsinarow
								break
							elif lives < 0.4:
								await ctx.send(f"You could've built this item with ``{correctansw}``.")
								break

							def check(m):
								return m.channel == channel and m.author == author
							try:
								msg = await self.bot.wait_for("message", check=check, timeout=player.shiva(15.322))
							except asyncio.TimeoutError:
								lives -= 1#If too late
								await channel.send(f"**{random.choice(lateansw)}**, you have ``{lives}`` lives remaining.")
								accumulated_g -= 18
								ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
							else:
								if strip_str(msg.content) == "skip":	#to skip an item
									lives -= 0.5
									ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
									await ctx.send(f"You have ``{lives}`` lives remaining, this item is built with ``{correctansw}``.")
									break
								elif strip_str(msg.content) == "stop":	#to stop the endless quiz
									lives = 322
									break
								elif type(itemanswers[0]) == list:		#if itemanswers has lists of correct answers it checks the correct answ in
									if player.compare_strings(msg.content, itemanswersmerged).success:		#itemanswersmerged, gives reward
										await ctx.send(f"**{random.choice(rightansw)}**")
										accumulated_g += 3
										itemstopop = []			#create a new list of items that must be removed from itemanswersmerged
										for itemlist in itemanswers:
											result = player.compare_strings(msg.content, itemlist)
											if result.success:				#check index of correct answer to remove from all lists of itemanswers
												n = itemlist.index(result.answer)
										for index, itemlist in enumerate(itemanswers):
											itemstopop.append(itemanswers[index][n])
											itemanswers[index].pop(n)		#pop answered item out of all lists of the itemanswers
										for item in itemstopop:		#loop through itemstopop and remove each item of it from itemanswersmerged
											itemanswersmerged.remove(item)
									else:
										lives -= 1
										ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
										await ctx.send(f"**{random.choice(wrongansw)}** you have ``{lives}`` lives remaining.")
								else:
									result = player.compare_strings(msg.content, itemanswers)
									if result.success:	#if itemanswers is just a list of strings, remove answered item from both lists.
										await ctx.send(f"**{random.choice(rightansw)}**")
										accumulated_g += 4
										itemanswers.remove(result.answer)
										itemanswersmerged.remove(result.answer)
									else:
										lives -= 1
										ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
										await ctx.send(f"**{random.choice(wrongansw)}** you have ``{lives}`` lives remaining.")

					elif decider == 2:
						iconn = unique_int_randomizer(server, iconquizlen, "iconquiznumbers", rng)		#Random number to give a random icon
						correctansw = find_correct_answer(iconquizvalues[iconn])		#Find the correct answer to be displayed incase user gets it wrong
						await ctx.send(f"**``Name the shown ability.``**", file=discord.File(f"./iconquizimages/{iconquizkeys[iconn]}"))
						def check(m):
							return m.channel == channel and m.author == author	#checks if the reply came from the same person in the same channel
						try:
							msg = await self.bot.wait_for("message", check=check, timeout=player.shiva(12.322))
						except asyncio.TimeoutError:	#If too late
							lives -= 1
							await channel.send(f"**{random.choice(lateansw)}** The correct answer was ``{correctansw}``, ``{lives}`` lives remaining.")
							accumulated_g -= 15
							ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
						else:
							if strip_str(msg.content) == "skip":
								lives -= 0.5
								ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
								await ctx.send(f"The correct answer was ``{correctansw}``, you have ``{lives}`` lives remaining.")
							elif strip_str(msg.content) == "stop":
								lives = 322
							elif player.compare_strings(msg.content, iconquizvalues[iconn]).success:
								accumulated_g += 12 + 2*ncorrectanswsinarow
								ncorrectansws, ncorrectanswsinarow = ncorrectansws + 1, ncorrectanswsinarow + 1
							else:
								lives -= 1
								ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
								await channel.send(f"**{random.choice(wrongansw)}** The correct answer was ``{correctansw}``, ``{lives}`` lives remaining.")
					else:
						scramblen = unique_int_randomizer(server, scramblelen, "scramblenumbers", rng)			#Random number to give a random question
						correctansw = scramblelist[scramblen]			#the correct answer
						scrambledworde = []			#empty list to .join() emojies onto
						charlist = list(correctansw.lower().replace("'", ""))			#converting string to list
						for char in random.sample(charlist, len(charlist)):		#shuffling the word list and looping through it
							scrambledworde.append(charemojies[char])		#picking up values of charemojies of the lowercase characters
						output = " ".join(scrambledworde)					#joining them to form a string of all emojies to output
						await ctx.send(f"**``Unscramble this word:``**\n{output}")
						def check(m):
							return m.channel == channel and m.author == author		#checks if the reply came from the same person in the same channel
						try:
							msg = await self.bot.wait_for("message", check=check, timeout=player.shiva(20.322))
						except asyncio.TimeoutError:		#If too late
							await channel.send(f"**{random.choice(lateansw)}** The correct answer was ``{correctansw}``")
							ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
						else:
							if strip_str(msg.content) == "skip":	#if user skips a question
								lives -= 0.5
								ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
								await ctx.send(f"The correct answer was ``{correctansw}``, you have ``{lives}`` remaining.")
							elif strip_str(msg.content) == "stop":	#if user stops the "endless" quiz
								lives = 322
							elif player.compare_strings(msg.content, correctansw).success:
								accumulated_g += 130
								ncorrectansws += 1
								ncorrectanswsinarow += 2
								await channel.send(f"**{random.choice(rightansw)}**")
							else:
								await channel.send(f"**{random.choice(wrongansw)}** The correct answer was ``{correctansw}``")
								ncorrectanswsinarow = player.aeon_disk(ncorrectanswsinarow)
			else:
				self.endless.reset_cooldown(ctx)
				await ctx.send("You don't have an **Aghanim's Scepter** to use Endless. Try 322 store to see all items.")
		except KeyError:
			pass

	@quiz.error
	async def quizerror(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			users = open_json("users.json")
			if 5000 in ast.literal_eval(users[str(ctx.message.author.id)]["items"]):
				if error.retry_after < 3:		#if user has octarine and the remaining time of the cooldown is Less
					await ctx.reinvoke()		#than the time octarine saves the user just bypasses the cooldownerror
					return
				else:
					await ctx.send("**Quiz** is on **cooldown** at the moment. Try again in a few seconds")
			else:
				await ctx.send("**Quiz** is on **cooldown** at the moment. You can buy an Octarine Core in the store to decrease command cooldowns.")

	@iconquiz.error
	async def iconquizerror(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			users = open_json("users.json")
			if 5000 in ast.literal_eval(users[str(ctx.message.author.id)]["items"]):
				if error.retry_after < 13:
					await ctx.reinvoke()
					return
				else:
					await ctx.send("**IconQuiz** is on **cooldown** at the moment.")
			else:
				await ctx.send("**IconQuiz** is on **cooldown** at the moment. You can buy an Octarine Core in the store to decrease command cooldowns.")

	@scramble.error
	async def scrambleerror(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			users = open_json("users.json")
			if 5000 in ast.literal_eval(users[str(ctx.message.author.id)]["items"]):
				if error.retry_after < 3:
					await ctx.reinvoke()
					return
				else:
					await ctx.send("**Scramble** is on **cooldown** at the moment.")
			else:
				await ctx.send("**Scramble** is on **cooldown** at the moment. You can buy an Octarine Core in the store to decrease command cooldowns.")

	@shopquiz.error
	async def shopquizerror(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			users = open_json("users.json")
			if 5000 in ast.literal_eval(users[str(ctx.message.author.id)]["items"]):
				if error.retry_after < 12.5:
					await ctx.reinvoke()
					return
				else:
					await ctx.send("**Shopkeepers quiz** is on **cooldown** at the moment.")
			else:
				await ctx.send("**Shopkeepers quiz** is on **cooldown** at the moment. You can buy an Octarine Core in the store to decrease command cooldowns.")

	@audioquiz.error
	async def audioquizerror(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send("**Audioquiz** is currently on cooldown. You can purchase an Octarine Core to decrease command cooldowns.")

	@blitz.error
	async def blitzerror(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send("**Blitz** is on being used in this channel at the moment, wait a bit or play on a different channel.")

	@duel.error
	async def duelerror(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send("**Duel** is currently on cooldown in this channel, try another channel or wait a bit.")
		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("You need to specify who you're duelling and how much gold the wager is, like this: 322 duel @user gold")
			self.duel.reset_cooldown(ctx)
		elif isinstance(error, commands.BadArgument):
			await ctx.send("That user doesn't exist or isn't in this server, try duelling someone else.")
			self.duel.reset_cooldown(ctx)

	@freeforall.error
	async def freeforallerror(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send("**Freeforall** is currently on cooldown in this channel, try another channel or wait a bit.")

	@endless.error
	async def endlesserror(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			users = open_json("users.json")
			if 5000 in ast.literal_eval(users[str(ctx.message.author.id)]["items"]):
				if error.retry_after < 100:
					await ctx.reinvoke()
					return
				else:
					await ctx.send("**Endless** is on **cooldown** at the moment.")
			else:
				await ctx.send("**Endless** is on **cooldown** at the moment. You can buy an Octarine Core in the store to decrease command cooldowns.")

	async def cog_command_error(self, ctx, error):
		#Errors to be ignored
		if isinstance(error, (commands.CommandOnCooldown, commands.MissingRequiredArgument, commands.BadArgument)):
			pass
		else:
			raise error

def setup(bot):
	bot.add_cog(Quizes(bot))
