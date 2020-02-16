import config
import requests
import bs4 as bs
import argparse
import pandas as pd

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

for lyrics in arr:
	dictionary = {}
	cleanlyrics = lyrics.replace('\n', ' ')
	for word in cleanlyrics.split(" "):
		if word.strip() == "":
			this = False
		elif word in dictionary:
			dictionary[word] = dictionary[word] + 1
		else:
			dictionary[word] = 0

	for word in dictionary:
		if dictionary[word] >= 3:
			print(word)
	print("==================")