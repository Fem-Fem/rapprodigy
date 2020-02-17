import config
import requests
import bs4 as bs
import argparse
import pandas as pd
import random

# import pdb
# import urllib

# parser = argparse.ArgumentParser()
# parser.add_argument("--song", help="This is the 'song' variable")

# args = parser.parse_args()
# query = args.song



auth_token = 'xI_s0mQF__hzFBdloHllfTJ20qrhsOiX6mf_vakxzbd2dIi73WZyMX60nFOJQ4Cb'
arr = []

queries = ["Ransom"]
for query in queries:

	url = 'https://api.genius.com/search?access_token=' + auth_token + "&q=" + query
	url = url.encode("utf-8")

	response = requests.get(url)
	title = response.json()["response"]["hits"][0]["result"]["title"]
	url = response.json()["response"]["hits"][0]["result"]["url"]
	id = response.json()["response"]["hits"][0]["result"]["id"]

	url = response.json()["response"]["hits"][0]["result"]["url"]
	response = requests.get(url)
	soup = bs.BeautifulSoup(response.text, features="html.parser")
	arr.append(soup.find(class_='lyrics').get_text())

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
		text_tester = self.text + self.text[0] + self.text[1]
		for i in range(len(self.text)):
			j = i + 1
			k = i + 1 + 1
			if library.get(text_tester[i:k]) == None:
				library[text_tester[i:k]] = {text_tester[k]: 1}
			else:
				if library[text_tester[i:k]].get(text_tester[k]):
					library[text_tester[i:k]][text_tester[k]] = library[text_tester[i:k]][text_tester[k]] + 1
				else:
					library[text_tester[i:k]][text_tester[k]] = 1
		self.dictionary = library

	def next_letter(self, text):
		for z in range(150):
			population = []
			weights = []
			for i in self.dictionary[text[-2:]]:
				population.append(i)
				weights.append(self.dictionary[text[-2:]][i])
			new_letter = random.choices(population, weights)
			text = text + new_letter[0]
		print(text)

	def print_info(self):
		print(self.text)
		print(self.k_int)
		print(self.dictionary)

rap = MarkovRap(arr[0], 2)
rap.kgram()
# rap.print_info()
rap.next_letter("I ")