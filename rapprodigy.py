import config
import requests
import bs4 as bs
import argparse
import pandas as pd
import random
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# remove albums with super long outros and skits?

# import pdb

# parser = argparse.ArgumentParser()
# parser.add_argument("--song", help="This is the 'song' variable")

# args = parser.parse_args()
# queries = args.song

# Parser should include k_int

# Perhaps include more robust data tests here?
# Unique words, syllables.

class RapGetter():

	def __init__(self, artist, url):
		self.arr = []
		self.artist = artist
		self.queries = []
		self.word_list = ''
		self.commas = 0
		self.question_marks = 0
		self.url = url

	def fetch(self):

		# get all songs
		response = requests.get(self.url)
		soup = bs.BeautifulSoup(response.text, features="html.parser")
		thislist = soup.find_all(class_='chart_row chart_row--light_border chart_row--full_bleed_left chart_row--align_baseline chart_row--no_hover')
		counter = 0
		for i in this_list:
			this_list[counter] = i.find(class_='chart_row-content').find('a').get('href')
			counter = counter + 1
		final_list = []

		# remove skits from analysis
		for i in this_list:
			if 'skit' not in i:
				final_list.append(i)
		self.queries = final_list

	def clean(self):
		
		for query in self.queries:

			response = requests.get(query)
			soup = bs.BeautifulSoup(response.text, features="html.parser")
			text = soup.find(class_='lyrics').get_text()

			# remove words between [] in text, which stores metadata on the song
			text = re.sub('\[[^\]]*]', '', text).strip()

			# store original datal, untouched
			self.arr.append(text)

			# clean strings
			text = text.replace('\n', ' ').lower().strip()
			
			text = re.sub('[\(\)\'!]', '', text).strip()

			text = text.split(",")
			s = ''
			self.commas = len(text) - 1
			text = s.join(text).lower().strip()

			text = text.split("?")
			s = ''
			self.question_marks = len(text) - 1
			text = s.join(text).lower().strip()

			text = re.sub('\s\s+', ' ', text)
			self.word_list = text

	# for markov model
	def compile(self):
		for i in self.arr:
			if self.arr[0] != i:
				self.arr[0] = self.arr[0] + i


	# make method to call markov model??

	# this will return different info if I've run `compile` or not though, not exactly ideal.
	def print_info(self):
		print(self.arr[0])

	def print_word_list(self):
		print(self.word_list)

	# can i break this up?
	def wordcloud(self):
		store = {}
		for i in self.word_list.split(" "):
			if i in store:
				store[i] = store[i] + 1
			else:
				store[i] = 1

		set_ = set()
		arr = []
		for i in store:
			if store[i] >= 10:
				arr.append(i)

		potentially_often_used_rap_words_and_common_words = ["nigga", "uh", "yeah", "shit", "niggas", "fuck", "fuckin'", "uhh", "ayy", "the"]
		for i in arr:
			if i not in potentially_often_used_rap_words_and_common_words:
				set_.add(i)

		text = ""
		for i in set_:
			text = text + " " + i
		cloud = WordCloud(background_color="white").generate(text)
		plt.imshow(cloud)
		plt.axis("off")
		plt.show()
		print(set_)

	# @classmethod
	# def dataframe(cls):
	# 	return 

	# this is incorrect, i want to be able to create a dataframe and append things to it :/
	def dataframe(self):
		words = self.word_list.split(" ")
		df = pd.DataFrame({self.artist: words})
		return df

# class MarkovRap:

# 	def __init__(self, text, k_int):
# 		self.text = text
# 		self.k_int = k_int
# 		self.dictionary = ''
# 	#perhaps add code so that different rap lyrics dont rap around but instead they are counted for the markov model each time??
# 	def kgram(self):
# 		library = {}
# 		text_tester = self.text
# 		for i in range(self.k_int):
# 			text_tester = text_tester + self.text[i]
# 		for i in range(len(self.text)):
# 			k = i + self.k_int
# 			if library.get(text_tester[i:k]) == None:
# 				library[text_tester[i:k]] = {text_tester[k]: 1}
# 			else:
# 				if library[text_tester[i:k]].get(text_tester[k]):
# 					library[text_tester[i:k]][text_tester[k]] = library[text_tester[i:k]][text_tester[k]] + 1
# 				else:
# 					library[text_tester[i:k]][text_tester[k]] = 1
# 		self.dictionary = library

# 	def next_letter(self, text):
# 		for z in range(500):
# 			population = []
# 			weights = []
# 			for i in self.dictionary[text[-self.k_int:]]:
# 				population.append(i)
# 				weights.append(self.dictionary[text[-self.k_int:]][i])
# 			new_letter = random.choices(population, weights)
# 			text = text + new_letter[0]
# 		print(text)

# 	def print_info(self):
# 		print(self.text)
# 		print(self.k_int)
# 		print(self.dictionary)

# Randomly generate a start point for markov model?

url_list = [
	# 'https://genius.com/albums/Chance-the-rapper/Coloring-book',
	# 'https://genius.com/albums/Ybn-cordae/The-lost-boy',
	'https://genius.com/albums/Lil-wayne/Tha-carter-iii'
]

i = 0
for url in url_list:
	i = i + 1
	lyrics = RapGetter(i, url)
	lyrics.fetch()
	lyrics.clean()
	lyrics.dataframe()
# lyrics.compile()
# lyrics.wordcloud()

# rap = MarkovRap(lyrics.arr[0], 7)
# rap.kgram()
# rap.next_letter("broke a")