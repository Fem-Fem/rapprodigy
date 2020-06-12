print("START RAPGETTER CLASS")
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

# parser = argparse.ArgumentParser()
# parser.add_argument("--song", help="This is the 'song' variable")
# args = parser.parse_args()
# queries = args.song

# Perhaps include more robust data tests here?
# Unique words, number of syllables, number of words repeated, divide by total number of words/total length of album

# Make more granular. Unique words/question marks/commas per album and per song? do this in dataframe?

class RapGetter():

	_df = pd.DataFrame(columns = ['Artist', 'Album', 'Song', 'Text', 'Commas', 'Question Marks'])

	def __init__(self, url):
		# for markov?
		self.original_text = ''

		self.url = url
		self.queries = []
		self.wordcloud_count = 10
		self.artist = url.split("/")[4]
		self.album = url.split("/")[5]
		self.song_titles = []
		self.word_list = []
		self.commas_list = []
		self.question_marks_list = []


	def fetch(self):

		# get all songs
		response = requests.get(self.url)
		soup = bs.BeautifulSoup(response.text, features="html.parser")
		list_of_songs = soup.find_all(class_='chart_row chart_row--light_border chart_row--full_bleed_left chart_row--align_baseline chart_row--no_hover')
		counter = 0
		for i in list_of_songs:
			list_of_songs[counter] = i.find(class_='chart_row-content').find('a').get('href')
			counter = counter + 1
		final_list_of_songs = []

		# remove skits from analysis
		for i in list_of_songs:
			if 'skit' not in i:
				final_list_of_songs.append(i)
		self.queries = final_list_of_songs


	def clean(self):
		
		for query in self.queries:
		
			response = requests.get(query)
			soup = bs.BeautifulSoup(response.text, features="html.parser")

			# find song title here
			song_title = soup.find(class_='header_with_cover_art-primary_info-title').text
			self.song_titles.append(song_title)

			text = soup.find(class_='lyrics').get_text()

			# remove words between [] in text, which stores metadata on the song
			text = re.sub('\[[^\]]*]', '', text).strip()

			# store original datal, untouched
			if self.original_text == '':
				self.original_text = self.original_text + text
			else:
				self.original_text = self.original_text + " " + text

			# clean strings
			text = text.replace('\n', ' ').lower().strip()
			
			text = re.sub('[\(\)\'!]', '', text).strip()

			text = text.split(",")
			s = ''
			self.commas_list.append(len(text) - 1)
			text = s.join(text).lower().strip()

			text = text.split("?")
			s = ''
			self.question_marks_list.append(len(text) - 1)
			text = s.join(text).lower().strip()

			text = re.sub('\s\s+', ' ', text)
			self.word_list.append(text)

	# make method to call markov model

	# this will return different info if I've run `compile` or not though, not exactly ideal. 
	def print_info(self):
		print(self.original_text[0])


	def print_word_list(self):
		print(self.word_list)


	def filter_wordcloud_by_size(self, store, n):
		word_appears_more_than_n_times = []
		for i in store:
			if store[i] > n:
				word_appears_more_than_n_times.append(i)

		return word_appears_more_than_n_times


	# need to make wordcloud per song, per album, and per artist?
	def wordcloud(self):
		# count number of unique variables
		# should i just do this in the dataframe?
		store = {}
		for i in self.word_list.split(" "):
			if i in store:
				store[i] = store[i] + 1
			else:
				store[i] = 1

		word_appears_more_than_n_times = filter_wordcloud_by_size(store, self.wordcloud_count)

		potentially_often_used_rap_words_and_common_words = ["nigga", "uh", "yeah", "shit", "niggas", "fuck", "fuckin'", "uhh", "ayy", "the"]
		set_ = set()
		for i in word_appears_more_than_n_times:
			if i not in potentially_often_used_rap_words_and_common_words:
				set_.add(i)

		wordcloud_text = ""
		for i in set_:
			wordcloud_text = wordcloud_text + " " + i
		cloud = WordCloud(background_color="white").generate(wordcloud_text)
		plt.imshow(cloud)
		plt.axis("off")
		plt.show()


	def dataframe(self):
		for i in range(len(self.word_list)):
			RapGetter._df = RapGetter._df.append({
				'Artist': self.artist, 
				'Text': self.word_list[i],
				'Album': self.album,
				'Song': self.song_titles[i],
				'Commas': self.commas_list[i],
				'Question Marks': self.question_marks_list[i]
				}, ignore_index=True)
		print("RAPGETTER DATAFRAME")
		print(RapGetter._df)
		return RapGetter._df

print("END RAPGETTER CLASS")

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



url_list = [
	'https://genius.com/albums/Ybn-cordae/The-lost-boy'
]
for url in url_list:
	lyrics = RapGetter(url)
	lyrics.fetch()
	lyrics.clean()
	lyrics.dataframe()

j = ''
for i in lyrics.word_list:
	j = j + i
rap = MarkovRap(j, 7)
rap.kgram()
rap.next_letter("broke a") 


