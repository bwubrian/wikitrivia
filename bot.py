
import discord
from discord.ext import commands
import asyncio
import time
import math
import os

import trivia_version_1_2_2

#client = discord.Client()
bot = commands.Bot(command_prefix = ["n!", "n1", "b2", "n2", "N!", "N1", "B2", "N2"] , description = "A super trivia bot that tries not to suck too much.")
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

@bot.command()
async def say(ctx, *, something = None):
	"""Prints the given string."""
	if something is not None:
		await ctx.send(something)
	else:
		await ctx.send("lol you're pretty bad at this, use the *say* command with argument, such as: **n!say ooglyoogly**")

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


async def check_trivia(reaction, user):
	print("progress 3")
	if str(reaction) == global_solution_reaction:
		await reaction.message.channel.send(user.mention + " >> :white_check_mark: " + "Congratulations! "+"**"+global_solution[3:]+"**"+" was the correct answer.")
	else:
		await reaction.message.channel.send(user.mention + " >> :x: " + "**" + global_answer_choices_list[reaction_to_number(str(reaction))][3:] + "**" + " was incorrect. " + "**"+ global_solution[3:]+"**"+" was the correct answer.")

@bot.event
async def on_reaction_add(reaction, user):
	

	#await reaction.message.channel.send(user.id)
	#await reaction.message.channel.send(trivia_user.id)
	'''
	print(user)
	print("on reaction added")
	print(doing_trivia)
	'''
	global doing_trivia
	
	
	#print(reaction.message.id)
	#print(msg.id)
	#print(global_trivia_user == user)
	#print(doing_trivia)
	#print(reaction.message.id == trivia_question_message.id)
	if global_trivia_user == user and doing_trivia and reaction.message.id == trivia_question_message.id:
		
		doing_trivia = False
		
		await check_trivia(reaction, user)
		'''
		await reaction.message.channel.send(reaction)
		await reaction.message.channel.send(str(reaction))
		await reaction.message.channel.send(solution)
		await reaction.message.channel.send(":regional_indicator_"+solution_letter+":")
		'''	




@bot.command(aliases = ["t", "question"])
async def trivia(ctx, *, category_name = None):
	"""Generates a trivia question.
	Can either take an argument to specify a category(ie. Video Games, Memes, History)
	or called without argument for random category
		
	"""
	potential_trivia_user = ctx.message.author
	global global_trivia_user
	global global_context
	global_context = ctx

	async def execute_trivia():
		global doing_trivia
		doing_trivia = True
		
		
		if category_name is None:		
			returned_question = trivia_version_1_2_2.get_question()
		else:
			returned_question = trivia_version_1_2_2.get_question_given_category(category_name)
			if returned_question is None:
				await ctx.channel.send(str(ctx.author.mention) + " >> " + "No trivia questions successfully generated for this category.")
				doing_trivia = False
				return None
		
		#await ctx.channel.send(returned_question[0])
		#await ctx.channel.send(returned_question[1])

		question = returned_question[0]

		answer_choices = ""
		for choice in returned_question[1]:
			answer_choices += choice
			answer_choices += "\n"
			answer_choices += "\n"

		answer_choices_list = returned_question[1]

		solution = returned_question[2]
		solution_letter = returned_question[4]
		solution_reaction = format_solution_reaction(solution_letter)

		global global_solution_reaction
		global_solution_reaction = solution_reaction
		global global_solution
		global_solution = solution
		global global_answer_choices_list
		global_answer_choices_list = answer_choices_list

		category = returned_question[3]
		category = "Category: " + category

		time_warning = "You have " + str(TRIVIA_TIMER) + " seconds to answer."

		color = discord.Colour(16579644)
		await ctx.channel.send(str(ctx.author.mention))
		#+"\n\n"+category
		embeded_question = discord.Embed(title="",description="**"+question+"**" + "\n\n" + answer_choices + "\n\n", colour=color)
		embeded_question.set_footer(text = time_warning)
		
		await ctx.channel.send(embed = embeded_question)




		users[global_trivia_user] = time.time()

		start_time = time.time()


		msg = await ctx.channel.history().get(author__name = "Super Trivia")
		global trivia_question_message
		trivia_question_message = msg
		await msg.add_reaction(regional_indicator_a)
		await msg.add_reaction(regional_indicator_b)
		await msg.add_reaction(regional_indicator_c)
		await msg.add_reaction(regional_indicator_d)

		async def run_trivia_clock():
			current_time = time.time()
			time_elapsed = round(current_time - start_time)
			time_remaining = TRIVIA_TIMER - time_elapsed

			time_warning = "You have " + str(time_remaining) + " seconds to answer."
			embeded_question = discord.Embed(title="",description="**"+question+"**" + "\n\n" + answer_choices + "\n\n", colour=color)
			embeded_question.set_footer(text = time_warning)
			await msg.edit(embed = embeded_question)

			for n in range(time_remaining):
				await asyncio.sleep(1)
				time_remaining -= 1
				global doing_trivia
				if doing_trivia:
					time_warning = "You have " + str(time_remaining) + " seconds to answer."
					embeded_question = discord.Embed(title="",description="**"+question+"**" + "\n\n" + answer_choices + "\n\n", colour=color)
					embeded_question.set_footer(text = time_warning)
					await msg.edit(embed = embeded_question)
				if time_remaining == 0:
					if doing_trivia:
						await asyncio.sleep(1)
						last_msg = await ctx.channel.history().get(author__name = "Super Trivia")
						#where >> is used in the message where the user already reacted on time
						if ">>" not in str(last_msg.content):
							await ctx.channel.send(str(ctx.author.mention) + " you took too long to answer. The correct answer was " + "**" + solution[3:] + "**")
							doing_trivia = False
		await run_trivia_clock()
		
	if doing_trivia == True:
		
		await ctx.channel.send(str(ctx.author.mention) + " >> " + str(global_trivia_user) + " is already doing trivia.")
		return None
	else:
		if potential_trivia_user in users:
			if time.time() - users[potential_trivia_user] > TRIVIA_COOLDOWN:				
				global_trivia_user = potential_trivia_user
				await execute_trivia()
			else:
				seconds_remaining = math.ceil(TRIVIA_COOLDOWN - (time.time() - users[potential_trivia_user]))
				if seconds_to_minutes(seconds_remaining) > 0:
					await ctx.channel.send(str(ctx.author.mention) + " >> " + str(seconds_to_minutes(seconds_remaining)) + " minutes remaining until next trivia.")
				else:
					await ctx.channel.send(str(ctx.author.mention) + " >> " + str(seconds_remaining) + " seconds remaining until next trivia.")
		else:		
			global_trivia_user = potential_trivia_user
			await execute_trivia()



@bot.event
async def on_ready():
	print("I am running on " + bot.user.name)
	print("With the ID: " + str(bot.user.id))

	await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "David stuck in Plat. [n!]"))




bot.run(str(os.environ.get("BOT_TOKEN")))


'''
bugs: cant handle multiple trivia calls at once
'''


