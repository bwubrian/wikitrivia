#import dbl
import discord
from discord.ext import commands
import asyncio
import time
import math
import os


import aiohttp
import asyncio
import logging

import trivia_version_1_2_2
#import leaguebot_version_0

#client = discord.Client()
bot = commands.Bot(command_prefix = ["n!", "n1", "b2", "n2", "N!", "N1", "B2", "N2"] , description = "A super trivia bot that tries not to suck too much.")

dbl_token = str(os.environ.get("DBL_TOKEN"))
servers_data = open("servers_data.txt", "w", encoding='utf-8')
'''
class DiscordBotsOrgAPI:
    """Handles interactions with the discordbots.org API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = dbl_token  #  set this to your DBL token
        self.dblpy = dbl.Client(self.bot, self.token)
        self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""

        while True:
        	if self.bot.is_ready():
	            logger.info('attempting to post server count')
	            print("in the loop")
	            try:
	                await self.dblpy.post_server_count()
	                logger.info('posted server count ({})'.format(len(self.bot.guilds)))
	                print("posted")
	            except Exception as e:
	                logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
	                print("failed to post")
	            await asyncio.sleep(1800)
	        else:
	        	print("not ready")


def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(DiscordBotsOrgAPI(bot))
'''
client_id = str(os.environ.get("CLIENT_ID"))
url = "https://discordbots.org/api/bots/"+client_id+"/stats"
headers = {"Authorization" : dbl_token}

"""
def setup(bot):
    global logger
    #logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    #setattr(bot, "logger", logging.getLogger("kewl_name"))
    logger = logging.getLogger('bot')
    bot.add_cog(DiscordBotsOrgAPI(bot))
"""

'''
regional_indicator_a = "\U0001F1E6"
regional_indicator_b = "\U0001F1E7"
regional_indicator_c = "\U0001F1E8"
regional_indicator_d = "\U0001F1E9"
'''
regional_indicator_a = "🇦"
regional_indicator_b = "🇧"
regional_indicator_c = "🇨"
regional_indicator_d = "🇩"




"""

users = {}
#Minimum time between trivia questions, in seconds
TRIVIA_COOLDOWN = 20
#Maximum time to answer trivia questions, in seconds
TRIVIA_TIMER = 10

doing_trivia = False
trivia_question_message = None

global_trivia_user = None
global_context = None
global_solution_reaction = None
global_solution = None
global_answer_choices_list = None

nsfw_filter = True
"""
class Server:
	users = {}
	trivia_cooldown = 20
	trivia_timer = 10

	doing_trivia = False
	trivia_question_message = None

	trivia_user = None
	context = None
	solution_reaction = None
	solution = None
	answer_choices_list = None

	nsfw_filter = True

	guild = None

	def __init__(self, guild):
		self.guild = guild

servers = {}

known_servers = ["test bot", "Lemon Tree"]

@bot.command(aliases = ["say"])
async def echo(ctx, *, something = None):
	"""Prints the given message."""
	#if ctx.guild.name in known_servers:
	#	await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "David stuck in Plat. [n!]"))
	if something is not None:
		await ctx.send(something)
	else:
		await ctx.send("Use the *echo* command with an argument, such as: **n!echo hello**")

@bot.command()
async def lemontree(ctx, *, name = None):
	"""n/a"""
	region = 'na1'
	if ctx.guild.name in known_servers:
		if name is not None:
			if name == "davidrank":
				data = leaguebot_version_0.get_summoner_rank("Later Tonight", region)
				if data is not None:
					if len(data[1])>=9 and data[1][:7] == "DIAMOND":
						await ctx.channel.send(data[0] + " has been carried to " + data[1] + " " + data[2] + " with " + str(data[3]) + "LP")
					else:
						await ctx.channel.send(data[0] + " is " + data[1] + " " + data[2] + " with " + str(data[3]) + "LP" + ", though he claims he was diamond once.")
			elif name == "davidrealrank":
				data = leaguebot_version_0.get_summoner_rank("Later Tonight", region)
				await ctx.channel.send(data[0] + " is " + "PLATINUM" + " " + "I" + " with " + str(data[3]) + "LP" + ", though he claims he was diamond once.")
			elif name == "joerank":
				data = leaguebot_version_0.get_summoner_rank("Joe Joe Joe Joe", region)
				if data is not None:
					await ctx.channel.send(data[0] + " is " + data[1] + " " + data[2] + " with " + str(data[3]) + "LP" + "")
			elif name == "brucerank":
				data = leaguebot_version_0.get_summoner_rank("Extreme A", region)
				if data is not None:
					await ctx.channel.send(data[0] + " is " + data[1] + " " + data[2] + " with " + str(data[3]) + "LP" + "")
			elif name == "ericrank":
				data = leaguebot_version_0.get_summoner_rank("Eric Vu", region)
				if data is not None:
					await ctx.channel.send(data[0] + " is " + data[1] + " " + data[2] + " with " + str(data[3]) + "LP" + "")
			elif name == "jamesrank":
				data = leaguebot_version_0.get_summoner_rank("Krandino", region)
				if data is not None:
					await ctx.channel.send(data[0] + " is " + data[1] + " " + data[2] + " with " + str(data[3]) + "LP" + "")
				else:
					await ctx.channel.send("this dude only play a:ascam:")
			elif name == "brianrank":
				data = leaguebot_version_0.get_summoner_rank("Ooglyoogly", region)
				if data is not None:
					await ctx.channel.send(data[0] + " is " + data[1] + " " + data[2] + " with " + str(data[3]) + "LP" + "")
				else:
					await ctx.channel.send("Up and coming talent, silver II hopeful, shows much promise.")
			else:
				await ctx.channel.send("This is not a lemon.")
	else:
		await ctx.send("That command is currently not available here.")
		
	

#hard coded... i give up
def format_solution_reaction(solution_letter):
	if solution_letter == "a":
		return "🇦"
	if solution_letter == "b":
		return "🇧"
	if solution_letter == "c":
		return "🇨"
	if solution_letter == "d":
		return "🇩"
def reaction_to_number(reaction):
	if str(reaction) == regional_indicator_a:
		return 0
	if str(reaction) == regional_indicator_b:
		return 1
	if str(reaction) == regional_indicator_c:
		return 2
	if str(reaction) == regional_indicator_d:
		return 3
	else:
		return None
def seconds_to_minutes(num_sec):
	return num_sec//60
def bolded_string(string_to_bold):
	return "**"+string_to_bold+"**"


async def check_trivia(reaction, user, s):
	print("progress 3")
	if str(reaction) == s.solution_reaction:
		await reaction.message.channel.send(user.mention + " >> :white_check_mark: " + "Congratulations! "+"**"+s.solution[3:]+"**"+" was the correct answer.")
	else:
		await reaction.message.channel.send(user.mention + " >> :x: " + "**" + s.answer_choices_list[reaction_to_number(str(reaction))][3:] + "**" + " was incorrect. " + "**"+ s.solution[3:]+"**"+" was the correct answer.")

@bot.event
async def on_reaction_add(reaction, user):

	#await reaction.message.channel.send(user.id)
	#await reaction.message.channel.send(trivia_user.id)
	'''
	print(user)
	print("on reaction added")
	print(doing_trivia)
	'''
	if reaction.message.guild in servers:
		s = servers[reaction.message.guild]
		if s.trivia_user == user and s.doing_trivia and reaction.message.id == s.trivia_question_message.id:
			s.doing_trivia = False
			await check_trivia(reaction, user, s)
	else:
		print("Error, guild not in server list.")
	
	#print(reaction.message.id)
	#print(msg.id)
	#print(global_trivia_user == user)
	#print(doing_trivia)
	#print(reaction.message.id == trivia_question_message.id)
		'''
		await reaction.message.channel.send(reaction)
		await reaction.message.channel.send(str(reaction))
		await reaction.message.channel.send(solution)
		await reaction.message.channel.send(":regional_indicator_"+solution_letter+":")
		'''	

@bot.event
async def on_guild_join(guild):
	servers[guild] = Server(guild)
	print("Added a new guild to server list.")

@bot.command(aliases = ["t", "question"])
async def trivia(ctx, *, category_name = None):
	"""Generates a trivia question.
	
	Without additional arguments, a random question is generated.

	A category can be passed generate a question somewhat related to the given category.
	(ie. Video Games, Food, History)
	
	"[ - - - - - - - ]" is sometimes used in the question to hide info that would give away the answer.
		
	"""
	potential_trivia_user = ctx.message.author
	print("Guild: "+ctx.guild.name.encode("utf-8").decode("utf-8"))
	print("User: " +ctx.message.author.name+ctx.message.author.discriminator)

	#global global_trivia_user
	#global global_context
	#global_context = ctx

	async def execute_trivia(s):
		s.doing_trivia = True
		
		if category_name is None:		
			returned_question = trivia_version_1_2_2.get_question()
		else:
			if s.nsfw_filter == True:
				contents = []
				with open('Assets/full-list-of-bad-words-text-file_2018_03_26.txt') as file:
				    for line in file:
				    	contents.append(line.rstrip())
				    #print(contents)
				    if category_name.lower() in contents:
				    	await ctx.channel.send(str(ctx.author.mention) + " >> " + "[NSFW]" + " No trivia questions successfully generated for this category.")
				    	s.doing_trivia = False
				    	return None
			returned_question = trivia_version_1_2_2.get_question_given_category(category_name)
			if returned_question is None:
				await ctx.channel.send(str(ctx.author.mention) + " >> " + "No trivia questions successfully generated for this category.")
				s.doing_trivia = False
				return None
		
		#await ctx.channel.send(returned_question[0])
		#await ctx.channel.send(returned_question[1])

		question = returned_question[0]

		answer_choices = ""
		for choice in returned_question[1]:
			answer_choices += choice
			answer_choices += "\n"
			answer_choices += "\n"

		s.answer_choices_list = returned_question[1]

		s.solution = returned_question[2]
		
		solution_letter = returned_question[4] #solution letter is just intermediate step
		s.solution_reaction = format_solution_reaction(solution_letter)

		category = returned_question[3]
		category = "Category: " + category

		time_warning = "You have " + str(s.trivia_timer) + " seconds to answer."

		color = discord.Colour(16579644)
		await ctx.channel.send(str(ctx.author.mention))
		#+"\n\n"+category
		embeded_question = discord.Embed(title="",description="**"+question+"**" + "\n\n" + answer_choices + "\n\n", colour=color)
		embeded_question.set_footer(text = time_warning)
		
		await ctx.channel.send(embed = embeded_question)




		s.users[s.trivia_user] = time.time()

		start_time = time.time()

		await asyncio.sleep(1)
		msg = await ctx.channel.history().get(author__name = bot.user.name)
		
		#s.trivia_question_message = msg
		await msg.add_reaction(regional_indicator_a)
		await msg.add_reaction(regional_indicator_b)
		await msg.add_reaction(regional_indicator_c)
		await msg.add_reaction(regional_indicator_d)
		s.trivia_question_message = msg

		async def run_trivia_clock():
			current_time = time.time()
			time_elapsed = round(current_time - start_time)
			time_remaining = s.trivia_timer - time_elapsed

			time_warning = "You have " + str(time_remaining) + " seconds to answer."
			embeded_question = discord.Embed(title="",description="**"+question+"**" + "\n\n" + answer_choices + "\n\n", colour=color)
			embeded_question.set_footer(text = time_warning)
			await msg.edit(embed = embeded_question)

			for n in range(time_remaining):
				await asyncio.sleep(1)
				time_remaining -= 1
				if s.doing_trivia:
					time_warning = "You have " + str(time_remaining) + " seconds to answer."
					embeded_question = discord.Embed(title="",description="**"+question+"**" + "\n\n" + answer_choices + "\n\n", colour=color)
					embeded_question.set_footer(text = time_warning)
					await msg.edit(embed = embeded_question)
				if time_remaining <= 0:
					if s.doing_trivia:
						#await asyncio.sleep(1)
						await ctx.channel.send(str(ctx.author.mention) + " you took too long to answer. The correct answer was " + "**" + s.solution[3:] + "**")
						s.doing_trivia = False
						"""
						last_msg = await ctx.channel.history().get(author__name = bot.user.name)

						#where >> is used in the message where the user already reacted on time
						if ">>" not in str(last_msg.content):
							await ctx.channel.send(str(ctx.author.mention) + " you took too long to answer. The correct answer was " + "**" + s.solution[3:] + "**")
							s.doing_trivia = False
						"""
						#s.trivia_question_message use this to check instead
		await run_trivia_clock()
	
	if ctx.guild in servers:	
		s = servers[ctx.guild]
		if s.doing_trivia == True:
			await ctx.channel.send(str(ctx.author.mention) + " >> " + str(s.trivia_user) + " is already doing trivia.")
		else:
			if potential_trivia_user in s.users:
				if time.time() - s.users[potential_trivia_user] > s.trivia_cooldown:				
					s.trivia_user = potential_trivia_user
					await execute_trivia(s)
				else:
					seconds_remaining = math.ceil(s.trivia_cooldown - (time.time() - s.users[potential_trivia_user]))
					if seconds_to_minutes(seconds_remaining) > 0:
						await ctx.channel.send(str(ctx.author.mention) + " >> " + str(seconds_to_minutes(seconds_remaining)) + " minutes remaining until next trivia.")
					else:
						await ctx.channel.send(str(ctx.author.mention) + " >> " + str(seconds_remaining) + " seconds remaining until next trivia.")
			else:		
				s.trivia_user = potential_trivia_user
				await execute_trivia(s)
	else:
		print("fdsafds")

@bot.command(aliases = ["filter"])
async def nsfw(ctx, *, nsfw_filter_status = None):
	"""Toggles the Not Safe For Work filter to be on or off. 

	Use "False" or "Off" to turn off filter, "True" or "On" to turn back on. Needs administrator permission. 
		
	"""
	#print(ctx.message.author.permissions_in(ctx.channel))
	#print(ctx.message.author.guild_permissions.administrator)
	s = servers[ctx.guild]
	if ctx.message.author.guild_permissions.administrator:
		if ctx.channel.is_nsfw():
			if nsfw_filter_status == None:
				s.nsfw_filter =  not s.nsfw_filter
				await ctx.channel.send("Trivia NSFW filter set to " + str(s.nsfw_filter))
			else:
				if nsfw_filter_status.lower() == "false" or nsfw_filter_status.lower() == "off":
					s.nsfw_filter = False
					await ctx.channel.send("Trivia NSFW filter set to " + str(s.nsfw_filter))
				else:
					s.nsfw_filter = True
					await ctx.channel.send("Trivia NSFW filter set to " + str(s.nsfw_filter))
		else:
			await ctx.channel.send(str(ctx.author.mention) + " this is NOT a NSFW channel.")
	else:
		await ctx.channel.send(str(ctx.author.mention) + " you do not have administrator permission to do this.")

'''
@bot.command()
async def help(ctx, *, something = None):
	"""This is the help command."""
	embed discord.Embed(title="",description="**"+question+"**" + "\n\n" + answer_choices + "\n\n", colour=color)
	await ctx.channel.send(embed = embeded_question)
'''

@bot.command(aliases = ["setcooldown"])
async def set_cooldown(ctx, *, cooldown = None):
	"""Changes trivia cooldown time(default 20 seconds). 

	Use with a number as argument(eg. "n!set_cooldown 30" to set to 30 seconds. Needs administrator permission. 
		
	"""
	#print(ctx.message.author.permissions_in(ctx.channel))
	#print(ctx.message.author.guild_permissions.administrator)
	if ctx.message.author.guild_permissions.administrator:	
		if cooldown is not None:
			if ctx.guild in servers:
				s = servers[ctx.guild]
				if cooldown.isdigit():
					s.trivia_cooldown =  int(cooldown)
					await ctx.channel.send("Trivia cooldown set to " + str(s.trivia_cooldown) + " seconds.")
				else:
					await ctx.channel.send("Trivia cooldown must be set to an integer")
			else:
				print("Error, guild not in server list.")
		else:
			await ctx.channel.send("Use with a number as argument(eg. \"n!set_cooldown 30\" to set the cooldown between questions to 30 seconds.)")
	else:
		await ctx.channel.send(str(ctx.author.mention) + " you do not have administrator permission to do this.")

@bot.command(aliases = ["settimelimit"])
async def set_time_limit(ctx, *, time_limit = None):
	"""Changes questions time limit(default 10 seconds). 

	Use with a number as argument(eg. "n!set_time_limit 30" to set to 30 seconds.) Needs administrator permission.
		
	"""
	#print(ctx.message.author.permissions_in(ctx.channel))
	#print(ctx.message.author.guild_permissions.administrator)
	if ctx.message.author.guild_permissions.administrator:
		if time_limit is not None:
			if ctx.guild in servers:
				s = servers[ctx.guild]
				if time_limit.isdigit():
					s.trivia_timer =  int(time_limit)
					await ctx.channel.send("Trivia time limit set to " + str(s.trivia_timer) + " seconds.")
				else:
					await ctx.channel.send("Trivia time limit must be set to an integer")
			else:
				print("Error, guild not in server list.")
		else:
			await ctx.channel.send("Use with a number as argument(eg. \"n!set_time_limit 30\" to set the time limit for each trivia question to 30 seconds.)")
	else:
		await ctx.channel.send(str(ctx.author.mention) + " you do not have administrator permission to do this.")

@bot.event
async def on_ready():
	print("I am running on " + bot.user.name)
	print("With the ID: " + str(bot.user.id))
	for x in bot.guilds:
		
		print(x.name.encode("utf-8"))
		print("Region: " + str(x.region) + " Members: " + str(len(x.members)))
		servers_data.write("Name: ")
		servers_data.write(x.name.encode("utf-8").decode("utf-8"))
		servers_data.write(" Region: " + str(x.region) + " Members: " + str(len(x.members)) + "\n")


		servers[x] = Server(x)
		#print(x.name)
	print("Total Number of Servers: "+ str(len(bot.guilds)) + "\n")
	print("Total Number of Members: " + str(len(list(bot.get_all_members())))+ "\n")
	servers_data.write("Total Number of Servers: "+ str(len(bot.guilds)) + "\n")
	servers_data.write("Total Number of Members: " + str(len(list(bot.get_all_members()))) + "\n")
	await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "[n!help]"))
	
	servers_data.close()

	payload = {"server_count"  : len(bot.guilds)}
	async with aiohttp.ClientSession() as aioclient:
		await aioclient.post(url, data=payload, headers=headers)
	
	#setup(bot)
	#setup(bot)



bot.run(str(os.environ.get("BOT_TOKEN")))


#PLEASE USE THESE DOCS PLEASE PLEASE I'VE WASTED SO MUCH TIME
#https://discordpy.readthedocs.io/en/rewrite/


