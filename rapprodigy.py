import config
import requests
import bs4 as bs
import argparse
import pandas as pd
import random
import re

# import pdb

# parser = argparse.ArgumentParser()
# parser.add_argument("--song", help="This is the 'song' variable")

# args = parser.parse_args()
# queries = args.song

#Parser should include k_int

class RapGetter():

	def __init__(self):
		self.auth_token = 'xI_s0mQF__hzFBdloHllfTJ20qrhsOiX6mf_vakxzbd2dIi73WZyMX60nFOJQ4Cb'
		self.arr = []
		self.queries = ["Have Mercy", "RNP", "Broke as Fuck"]

	def fetch(self):
		
		for query in self.queries:
			url = 'https://api.genius.com/search?access_token=' + self.auth_token + "&q=" + query
			url = url.encode("utf-8")

			response = requests.get(url)
			title = response.json()["response"]["hits"][0]["result"]["title"]
			url = response.json()["response"]["hits"][0]["result"]["url"]
			id = response.json()["response"]["hits"][0]["result"]["id"]

			url = response.json()["response"]["hits"][0]["result"]["url"]
			response = requests.get(url)
			soup = bs.BeautifulSoup(response.text, features="html.parser")
			text = soup.find(class_='lyrics').get_text()
			# remove words between [] in text
			text = re.split('\[[^\]]*]', text)
			s = ''
			text = s.join(text)
			self.arr.append(text)

	def compile(self):
		for i in self.arr:
			self.arr[0] = self.arr[0] + i

	def print_info(self):
		for i in self.arr:
			print(i)

# Perhaps include more robust data tests here?
# Unique words, syllables.

# for lyrics in arr:
# 	dictionary = {}
# 	cleanlyrics = lyrics.replace('\n', ' ')
# 	for word in cleanlyrics.split(" "):
# 		if word.strip() == "":
# 			this = False
# 		elif word in dictionary:
# 			dictionary[word] = dictionary[word] + 1
# 		else:
# 			dictionary[word] = 0

# 	for word in dictionary:
# 		if dictionary[word] >= 4:
# 			print(word)
# 	print("==================")

class MarkovRap:

	def __init__(self, text, k_int):
		self.text = text
		self.k_int = k_int
		self.dictionary = ''

	def kgram(self):
		library = {}
		text_tester = self.text
		for i in range(self.k_int):
			text_tester = text_tester + self.text[i]
		for i in range(len(self.text)):
			k = i + self.k_int
			if library.get(text_tester[i:k]) == None:
				library[text_tester[i:k]] = {text_tester[k]: 1}
			else:
				if library[text_tester[i:k]].get(text_tester[k]):
					library[text_tester[i:k]][text_tester[k]] = library[text_tester[i:k]][text_tester[k]] + 1
				else:
					library[text_tester[i:k]][text_tester[k]] = 1
		self.dictionary = library

	def next_letter(self, text):
		for z in range(300):
			population = []
			weights = []
			for i in self.dictionary[text[-self.k_int:]]:
				population.append(i)
				weights.append(self.dictionary[text[-self.k_int:]][i])
			new_letter = random.choices(population, weights)
			text = text + new_letter[0]
		print(text)

	def print_info(self):
		print(self.text)
		print(self.k_int)
		print(self.dictionary)

# Randomly generate a start point for markov model?

# rap = MarkovRap(arr[0], 2)
# rap.kgram()
# rap.next_letter("I ")

# rap = MarkovRap(arr[0], 3)
# rap.kgram()
# rap.next_letter("I g")

# rap = MarkovRap(arr[0], 4)
# rap.kgram()
# rap.next_letter("I go")

lyrics = RapGetter()
lyrics.fetch()
lyrics.compile()
lyrics.print_info()

rap = MarkovRap(lyrics.arr[0], 4)
rap.kgram()
rap.next_letter("Sweet")

