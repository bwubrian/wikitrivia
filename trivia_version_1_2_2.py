"""
TRIVIA VERSION 1_2_2
Decently functional, many bugs from version 1 have been removed
#considerably faster than v0
#quite efficient, but a lot of room for improvement
#uses page category and subcategory
#badly written spagetti code atttemped to be fixed, might have made it worse
#this is 1_2_1 but without print statements
"""
from mediawiki import MediaWiki
import random
import math
import re
import string

wikipedia = MediaWiki()
ALPHABET = string.ascii_uppercase
NUMBER_OF_ANSWER_CHOICES = 4
NUMBER_OF_SENTENCES = 1

replace_bolded_expression = "[ - - - - - - - ] "
number_of_spaces = 16
spaces_in_replacement = replace_bolded_expression.count(" ")

def remove_parentheses(s):
	"""Returns a string with parentheses and content within removed from given string"""
	
	#all_parenthesis = re.findall(' \(.*?\)',s)
	#for parenthesis in all_parenthesis:
	#	s = s.replace(parenthesis, "")
	#return s

	new_string = ""
	number_of_left_paren = 0
	for n in range(len(s)):

		if s[n:n+1] == "(":
			number_of_left_paren += 1
			new_string = new_string[:-1]
		elif s[n:n+1] == ")":
			number_of_left_paren -= 1
		elif number_of_left_paren == 0:
			new_string += s[n:n+1]
	return new_string

def find_bolded(s):
	"""Returns a list with all bolded(signified by <b> and </b>) subtrings in given string
		
		Also purges of italics
	"""
	assert s.count("<p>") == 1, "if you see this i messed up my extract method"
	bbeg = -1
	bend = -1
	bolded = []
	while True:
		bbeg = s.find("<b>", bbeg+1)
		if bbeg == -1:
			break
		bend = s.find("</b>", bbeg)
		bolded.append(s[bbeg+3:bend]) #content bolded without tags

	for n in range(len(bolded)):
		bolded[n] = bolded[n].replace("<i>", "")
		bolded[n] = bolded[n].replace("</i>", "")

	return bolded

#this just doesn't work well enough
def find_title_words(chosen_choice_title):
	words = []
	last_index = 0
	for n in range(len(chosen_choice_title)):
		if n == len(chosen_choice_title)-1 or chosen_choice_title[n:n+1] == " ":
			if chosen_choice_title[last_index:last_index+1].isupper():
				words.append(chosen_choice_title[last_index:n+1])
			last_index = n+1
	print(words)
	return words

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_person(chosen_choice_page_categories):
	for n in range(len(chosen_choice_page_categories)):
		if chosen_choice_page_categories[n] == "Living people" or chosen_choice_page_categories[n][4:] == " births" or chosen_choice_page_categories[n][5:] == " births":
			return True
		if n >= 3:
			return False
	return False


def print_answer_choices(answer_choices):
	for n in range(len(answer_choices)):
		displayed_answer = ALPHABET[n]+") "+remove_parentheses(answer_choices[n])
		print(displayed_answer)

def format_answer_choices(answer_choices):
	new_answer_choices = []
	for n in range(len(answer_choices)):
		displayed_answer = ALPHABET[n]+") "+remove_parentheses(answer_choices[n])
		new_answer_choices.append(displayed_answer)
	return new_answer_choices

def select_summary_sentences(chosen_choice_summary, category = None):
	
	rearranged_summary = ""
	bold_location = chosen_choice_summary.find(replace_bolded_expression)
	rearranged_summary = "Which of the following" + chosen_choice_summary[bold_location + len(replace_bolded_expression) : ]
	if rearranged_summary[22:23] == '"':
		print("removed a quote")
		rearranged_summary = rearranged_summary[:22] + rearranged_summary[23:]

	rearranged_summary = rearranged_summary.replace("\n", " ")

	global number_of_spaces
	if category == "League of Legends":
		print('LOLSFDFS')
		number_of_spaces = 24



	period_location = -1
	periods_found = 0
	all_period_found = False
	period_indexes = []
	summary = ""
	while not all_period_found:
		period_location = rearranged_summary.find(". ", period_location+1)
		if period_location == -1:
			break
		summary = rearranged_summary[:period_location+1]
		periods_found += 1
		period_indexes.append(period_location)
		if summary.count(" ") - (spaces_in_replacement*summary.count(replace_bolded_expression) + 1) > number_of_spaces:
			all_period_found = True
			
	if all_period_found:
		for n in range(len(period_indexes)):
			if n == 0 and n == (len(period_indexes) - 1):
				summary = summary[:period_indexes[n]] + "?"
			elif n == 0:
				summary = summary[:period_indexes[n]] + "? (" + summary[period_indexes[n]+2:]
			elif n == (len(period_indexes) - 1):
				summary = summary[:period_indexes[n] + 1] + ")"
		summary = summary.replace(" him " , " him/her ")
		summary = summary.replace(" Him " , " Him/her ")
		summary = summary.replace(" her " , " him/her ")
		summary = summary.replace(" Her " , " Him/her ")

		summary = summary.replace(" he " , " he/she ")
		summary = summary.replace(" He ", " He/she ")
		summary = summary.replace(" she " , " he/she ")
		summary = summary.replace(" She " , " He/she ")

		summary = summary.replace(" his " , " his/her ")
		summary = summary.replace(" His " , " His/her ")
		summary = summary.replace(" her " , " his/her ")
		summary = summary.replace(" Her " , " His/her ")
		return summary
	return None


def get_question():
	starting_point = wikipedia.categorymembers("Main topic classifications", results = None, subcategories = True) #([pages],[subcategories])

	random_starting_point_index = random.randrange(0,len(starting_point[1]))
	

	print("Second Category: "+starting_point[1][random_starting_point_index])
	#second point is a tuple of pages and subcategories
	second_point = wikipedia.categorymembers(starting_point[1][random_starting_point_index], results = None, subcategories = True)


	finished = False
	while not finished:
		try:
			#random index in the range of number of subcategories in second category
			random_second_point_index = random.randrange(0,len(second_point[1]))
			

			#assign the subcategory page in the second category corresponding to the random index to point
			point = wikipedia.categorymembers(second_point[1][random_second_point_index], results = None, subcategories = True)
			
			final_category = ""
			#while there are still subcategories in point, keep assigning point to a random subcategory of the current category
			while len(point[1])>0:
				#random index in the range of number of subcategories in current point category
				random_point_index = random.randrange(0,len(point[1]))
				

				#print the subcategory corresponding to the random index
				
				final_category = str(point[1][random_point_index])
				#reassign the subcategory page in the point category corresponding to the random index to point
				point = wikipedia.categorymembers(point[1][random_point_index],results = None, subcategories = True)

				#print the point category
				

				

			#assign the list of pages in point to point_pages list
			point_pages = point[0]
			
			final_category_lower_name = final_category.lower()
			purged_point_pages = []
			purged_point_pages_without_parentheses = []
			complaints = 0
			#bad_words = ["template", "list", "portal:", "timeline", ] 
			
			#for every page(entry) in point_pages check if the conditions for a valid page names
			for entry in point_pages:
				#creates a version of entry title in all lower case for more flexible comparisons
				entry_lower_name = entry.lower()
				if "template:" not in entry_lower_name and "list" not in entry_lower_name and "portal:" not in entry_lower_name and "timeline" not in entry_lower_name and "glossary" not in entry_lower_name and "example" not in entry_lower_name:
					if entry_lower_name not in final_category_lower_name:
						if remove_parentheses(entry_lower_name) not in purged_point_pages_without_parentheses:
							purged_point_pages.append(entry)
							purged_point_pages_without_parentheses.append(remove_parentheses(entry_lower_name))
					else:
						complaints+=1
				else:
					complaints+=1

			#list of pages in category after bad pages have been removed
			point_pages = purged_point_pages
			

			if len(point_pages) >= NUMBER_OF_ANSWER_CHOICES:
				answer_choices_indexes = []
				answer_choices = []
				tries = 0
				while len(answer_choices_indexes)<NUMBER_OF_ANSWER_CHOICES and tries<99:
					random_page_index = random.randrange(0, len(point_pages))
					
					if random_page_index not in answer_choices_indexes and point_pages[random_page_index] not in answer_choices:
						answer_choices_indexes.append(random_page_index)
						answer_choices.append(point_pages[random_page_index])
					tries+=1
				

				chosen_choice_index = random.randrange(0, len(answer_choices))
				
				#chosen choice is a string representing the page title chosen(but not really sometimes)
				chosen_choice = answer_choices[chosen_choice_index]
				
				chosen_choice_page = wikipedia.page(chosen_choice)
				if chosen_choice == chosen_choice_page.title:

					letter_answer = ALPHABET[chosen_choice_index].lower()

					full_answer =  ALPHABET[chosen_choice_index] +") "+remove_parentheses(answer_choices[chosen_choice_index])
					




					chosen_choice_content = chosen_choice_page.content
					chosen_choice_summary = chosen_choice_page.summarize()
					chosen_choice_summary = remove_parentheses(chosen_choice_summary)
					chosen_choice_html = chosen_choice_page.html
					
					pbeg = -1
					bbeg = -1
					pend = -1
					found = False
					while not found:
						pbeg = chosen_choice_html.find("<p>", pbeg+1)
						if pbeg == -1:
							break
						bbeg = chosen_choice_html.find("<b>", pbeg)
						pend = chosen_choice_html.find("</p>", pbeg)
						if bbeg < pend:
							found = True

					extracted_para = chosen_choice_html[pbeg:pend+4] #4 is the length of "</p>", this shouldn't actually matter but make it pretty
					
					if found:		
						chosen_choice_bolds = find_bolded(extracted_para)

						for n in range(len(chosen_choice_bolds)):
							chosen_choice_bolds[n] = remove_parentheses(chosen_choice_bolds[n])

						summary_before_replace_bold = chosen_choice_summary
						for bolded in chosen_choice_bolds:
							chosen_choice_summary = chosen_choice_summary.replace(bolded, replace_bolded_expression)
						
						#only precede if something bolded was replaced, otherwise restart
						if summary_before_replace_bold != chosen_choice_summary:
							'''
							chosen_choice_title = chosen_choice_page.title
							chosen_choice_title_words = find_title_words(chosen_choice_title)
							for title_word in chosen_choice_title_words:
								chosen_choice_summary = chosen_choice_summary.replace(title_word, replace_bolded_expression)
							'''

							chosen_choice_summary = select_summary_sentences(chosen_choice_summary)

							if chosen_choice_summary is not None:
								chosen_choice_page_categories = chosen_choice_page.categories
								if is_person(chosen_choice_page_categories):
									print('AM PERSON')
									chosen_choice_title = remove_parentheses(chosen_choice_page.title)
									chosen_choice_title_words = find_title_words(chosen_choice_title)
									for title_word in chosen_choice_title_words:
										chosen_choice_summary = chosen_choice_summary.replace(title_word, replace_bolded_expression)

								answer_choices = format_answer_choices(answer_choices)

								to_return = []
								to_return.append(chosen_choice_summary)
								to_return.append(answer_choices)
								to_return.append(full_answer)
								to_return.append(final_category)
								to_return.append(letter_answer)
								return to_return

								finished = True
							else:
								print("FAILED TO FIND PERIOD")
						else:
							print("FAILED TO BOLD")
					else:
						print("FAILED TO FIND PARAGRAPH")
				else:
					print("STUPID WRAPPER GAVE ME THE WRONG PAGE")
			else:
				print("NOT ENOUGH ANSWER CHOICES")
		except Exception as e:
			print(e)




def get_question_given_category(category_name):
	try:
		category_to_search = "Category:" + category_name
		#stuff = wikipedia.search(thing, results = 10, suggestion = True)
		#print(stuff)


		#this version will be very strict, and cant deal with redirects, so "Category:Fruits" will not work while "Category:Fruit" will
		suggested_category = wikipedia.suggest(category_to_search)
		print(suggested_category)

		suggested_page = wikipedia.page(title = suggested_category, auto_suggest=True, redirect=True)
		print(suggested_page.title)
		print(suggested_page.redirects)
		suggested_page_html = suggested_page.html
		softredirect_index = suggested_page_html.find("softredirect")
		if softredirect_index != -1:
		    title_index = suggested_page_html.find("title=" , softredirect_index)
		    first_quote_index = suggested_page_html.find('"', title_index)
		    second_quote_index = suggested_page_html.find('"', first_quote_index + 1)
		    extracted_title = suggested_page_html[first_quote_index + 1:second_quote_index]
		    print(extracted_title)
		    suggested_category = extracted_title
		
		if suggested_category is None:
			print("No trivia questions successfully generated.")
			return None

		if "sockpuppets" in suggested_category:
			print("stupid sockpuppets")
			return None
		
		suggested_category_without_category = suggested_category[9:]
		print(suggested_category_without_category)

		point = wikipedia.categorymembers(suggested_category_without_category, results = None, subcategories = True) #([pages],[subcategories])
		attempts = 0
		finished = False
		while not finished:
			attempts += 1
			if attempts > 200:
				print("No trivia questions successfully generated.")
				return None
			point = wikipedia.categorymembers(suggested_category_without_category, results = None, subcategories = True) #([pages],[subcategories])
			try:
				final_category = ""
				#while there are still subcategories in point, keep assigning point to a random subcategory of the current category
				while len(point[1])>0:
					#random index in the range of number of subcategories in current point category
					random_point_index = random.randrange(0,len(point[1]))
					

					#print the subcategory corresponding to the random index
					
					final_category = str(point[1][random_point_index])
					print(str(3) + " > " + final_category)
					#reassign the subcategory page in the point category corresponding to the random index to point
					point = wikipedia.categorymembers(point[1][random_point_index],results = None, subcategories = True)

					#print the point category
					

					

				#assign the list of pages in point to point_pages list
				point_pages = point[0]
				


				final_category_lower_name = final_category.lower()

				print(str(attempts) + ":>> " + final_category_lower_name)

				purged_point_pages = []
				complaints = 0
				#bad_words = ["template", "list", "portal:", "timeline", ] 
				
				#for every page(entry) in point_pages check if the conditions for a valid page names
				for entry in point_pages:
					#creates a version of entry title in all lower case for more flexible comparisons
					entry_lower_name = entry.lower()
					if "template:" not in entry_lower_name and "list" not in entry_lower_name and "portal:" not in entry_lower_name and "timeline" not in entry_lower_name and "glossary" not in entry_lower_name and "example" not in entry_lower_name:
						if entry_lower_name not in final_category_lower_name:
							purged_point_pages.append(entry)
						else:
							complaints+=1
					else:
						complaints+=1

				#list of pages in category after bad pages have been removed
				point_pages = purged_point_pages
				

				if len(point_pages) >= NUMBER_OF_ANSWER_CHOICES:
					answer_choices_indexes = []
					answer_choices = []
					tries = 0
					while len(answer_choices_indexes)<NUMBER_OF_ANSWER_CHOICES and tries<99:
						random_page_index = random.randrange(0, len(point_pages))
						print(4)
						if random_page_index not in answer_choices_indexes and point_pages[random_page_index] not in answer_choices:
							answer_choices_indexes.append(random_page_index)
							answer_choices.append(point_pages[random_page_index])
						tries+=1
					

					chosen_choice_index = random.randrange(0, len(answer_choices))
					print(5)
					#chosen choice is a string representing the page title chosen(but not really sometimes)
					chosen_choice = answer_choices[chosen_choice_index]
					
					chosen_choice_page = wikipedia.page(chosen_choice)
					if chosen_choice == chosen_choice_page.title:

						letter_answer = ALPHABET[chosen_choice_index].lower()

						full_answer =  ALPHABET[chosen_choice_index] +") "+remove_parentheses(answer_choices[chosen_choice_index])
						




						chosen_choice_content = chosen_choice_page.content
						chosen_choice_summary = chosen_choice_page.summarize()
						chosen_choice_summary = remove_parentheses(chosen_choice_summary)
						chosen_choice_html = chosen_choice_page.html
						
						pbeg = -1
						bbeg = -1
						pend = -1
						found = False
						while not found:
							pbeg = chosen_choice_html.find("<p>", pbeg+1)
							if pbeg == -1:
								break
							bbeg = chosen_choice_html.find("<b>", pbeg)
							pend = chosen_choice_html.find("</p>", pbeg)
							if bbeg < pend:
								found = True

						extracted_para = chosen_choice_html[pbeg:pend+4] #4 is the length of "</p>", this shouldn't actually matter but make it pretty
						
						if found:		
							chosen_choice_bolds = find_bolded(extracted_para)

							for n in range(len(chosen_choice_bolds)):
								chosen_choice_bolds[n] = remove_parentheses(chosen_choice_bolds[n])

							summary_before_replace_bold = chosen_choice_summary
							for bolded in chosen_choice_bolds:
								chosen_choice_summary = chosen_choice_summary.replace(bolded, replace_bolded_expression)
							
							#only precede if something bolded was replaced, otherwise restart
							if summary_before_replace_bold != chosen_choice_summary:
								'''
								chosen_choice_title = chosen_choice_page.title
								chosen_choice_title_words = find_title_words(chosen_choice_title)
								for title_word in chosen_choice_title_words:
									chosen_choice_summary = chosen_choice_summary.replace(title_word, replace_bolded_expression)
								'''

								chosen_choice_summary = select_summary_sentences(chosen_choice_summary, suggested_category_without_category)

								if chosen_choice_summary is not None:
									chosen_choice_page_categories = chosen_choice_page.categories
									if is_person(chosen_choice_page_categories):
										print('AM PERSON')
										chosen_choice_title = remove_parentheses(chosen_choice_page.title)
										chosen_choice_title_words = find_title_words(chosen_choice_title)
										for title_word in chosen_choice_title_words:
											chosen_choice_summary = chosen_choice_summary.replace(title_word, replace_bolded_expression)
									

									answer_choices = format_answer_choices(answer_choices)

									to_return = []
									to_return.append(chosen_choice_summary)
									to_return.append(answer_choices)
									to_return.append(full_answer)
									to_return.append(final_category)
									to_return.append(letter_answer)
									return to_return

									finished = True
								else:
									print("FAILED TO FIND PERIOD")
							else:
								print("FAILED TO BOLD")
						else:
							print("FAILED TO FIND PARAGRAPH")
					else:
						print("STUPID WRAPPER GAVE ME THE WRONG PAGE")
				else:
					print("NOT ENOUGH ANSWER CHOICES")
			except Exception as e:
				print(e)
	except Exception as e:
		print(e)
		return None
		
if __name__== "__main__":
	get_question_given_category("apples")

'''
NOTES TO SELF

REMOVE PAGES IN THE CATEGORY THAT ARE THE TOPOC IF THE CATEGORY(IE. THE PAGE "VOTER DATABASE" IN CATEGORY VOTER DATABASES)

ADD SECOND SENTENCE IF NOT ENOUGH WORDS IN FIRST
MAYBE ALSO BASED ON THE NUMBER OF OTHER PAGES IN THE CATEGORY IT CAME FROM 
	IF A CATEGORY HAS A LOT OF PAGES, ITS MORE LIKELY FOR THE PAGES TO BE VERY VERY SIMILAR, NEEDING MORE INFO TO DIFFERENTIATE
	IE. SHAKESPEARE SONNETS

REARRANGE THE FIRST SENTENCE(check tagger)

IDEAS:
USE THE TAGGER TO CREATE TROLL RESPONSES

FIX THE CODE TO NOT BE SPAGETTI

BUG FIXES:
maybe use page id instead because wikipedia(page) is glitchy 
	or compare titles

two answer choices have same name after remobing parentheses

add "lit." case
	should be able to fix anyway with min word  in sentence count system later on instead of hard coding every case

maybe fixed
*remove italics in bold
*failed to remove parentheses correctly for double parenthesis  (fsafsda(fdsafds))
	honestly probably not even going to bother trying to fix this
'''
