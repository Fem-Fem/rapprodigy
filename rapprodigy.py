from RapGetter import RapGetter
from MarkovRap import MarkovRap

# remove albums with super long outros and skits?

# parser = argparse.ArgumentParser()
# parser.add_argument("--song", help="This is the 'song' variable")
# args = parser.parse_args()
# queries = args.song

# Perhaps include more robust data tests here?
# Unique words, number of syllables, number of words repeated, divide by total number of words/total length of album

# Make more granular. Unique words/question marks/commas per album and per song? do this in dataframe?

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

import os
from twilio.rest import Client
