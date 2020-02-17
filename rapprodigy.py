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

# class RapGetter():

# 	def __init__(self):
# 		self.auth_token = 'xI_s0mQF__hzFBdloHllfTJ20qrhsOiX6mf_vakxzbd2dIi73WZyMX60nFOJQ4Cb'
# 		self.arr = []
# 		self.queries = ["Have Mercy", "Broke as Fuck"]

# 	def fetch(self):
		
# 		for query in self.queries:
# 			url = 'https://api.genius.com/search?access_token=' + self.auth_token + "&q=" + query
# 			url = url.encode("utf-8")

# 			response = requests.get(url)
# 			title = response.json()["response"]["hits"][0]["result"]["title"]
# 			url = response.json()["response"]["hits"][0]["result"]["url"]
# 			id = response.json()["response"]["hits"][0]["result"]["id"]

# 			url = response.json()["response"]["hits"][0]["result"]["url"]
# 			response = requests.get(url)
# 			soup = bs.BeautifulSoup(response.text, features="html.parser")
# 			text = soup.find(class_='lyrics').get_text()
# 			# remove words between [] in text
# 			text = re.split('\[[^\]]*]', text)
# 			s = ''
# 			text = s.join(text)
# 			self.arr.append(text)

# 	def compile(self):
# 		for i in self.arr:
# 			if self.arr[0] != i:
# 				self.arr[0] = self.arr[0] + i

# 	def print_info(self):
# 		print(self.arr[0])

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

class RapGetter():

	def __init__(self):
		self.arr = []
		self.queries = []

	def fetch(self):

		url = 'https://genius.com/artists/ybn-cordae'
		url = url.encode("utf-8")

		response = requests.get(url)
		soup = bs.BeautifulSoup(response.text, features="html.parser")
		url = soup.find(class_='thumbnail_grid white_container').find(class_='vertical_album_card').get('href')

		response = requests.get(url)
		soup = bs.BeautifulSoup(response.text, features="html.parser")
		thislist = soup.find_all(class_='chart_row chart_row--light_border chart_row--full_bleed_left chart_row--align_baseline chart_row--no_hover')
		counter = 0
		for i in thislist:
			thislist[counter] = i.find(class_='chart_row-content').find('a').get('href')
			counter = counter + 1
		finallist = []
		for i in thislist:
			if 'skit' not in i:
				finallist.append(i)
		print(finallist)
		self.queries = finallist
		
		for query in self.queries:

			response = requests.get(query)
			soup = bs.BeautifulSoup(response.text, features="html.parser")
			text = soup.find(class_='lyrics').get_text()
			# remove words between [] in text
			text = re.split('\[[^\]]*]', text)
			s = ''
			text = s.join(text)
			self.arr.append(text)

	def compile(self):
		for i in self.arr:
			if self.arr[0] != i:
				self.arr[0] = self.arr[0] + i

	def print_info(self):
		print(self.arr[0])

class MarkovRap:

	def __init__(self, text, k_int):
		self.text = text
		self.k_int = k_int
		self.dictionary = ''
	#perhaps add code so that different rap lyrics dont rap around but instead they are counted for the markov model each time??
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
		for z in range(500):
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

lyrics = RapGetter()
lyrics.fetch()
lyrics.compile()
lyrics.print_info()

rap = MarkovRap(lyrics.arr[0], 7)
rap.kgram()
rap.next_letter("broke")

# url = 'https://genius.com/artists/ybn-cordae'
# url = url.encode("utf-8")

# response = requests.get(url)
# soup = bs.BeautifulSoup(response.text, features="html.parser")
# url = soup.find(class_='thumbnail_grid white_container').find(class_='vertical_album_card').get('href')

# response = requests.get(url)
# soup = bs.BeautifulSoup(response.text, features="html.parser")
# thislist = soup.find_all(class_='chart_row chart_row--light_border chart_row--full_bleed_left chart_row--align_baseline chart_row--no_hover')
# counter = 0
# for i in thislist:
# 	thislist[counter] = i.find(class_='chart_row-content').find('a').get('href')
# 	counter = counter + 1
# finallist = []
# for i in thislist:
# 	if 'skit' not in i:
# 		finallist.append(i)
# print(finallist)
