import config
import requests
import bs4 as bs
import argparse
import pandas as pd
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

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