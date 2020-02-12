import config
import requests
import bs4 as bs
import argparse

# import pdb
# import urllib

parser = argparse.ArgumentParser()
parser.add_argument("--song", help="This is the 'song' variable")

args = parser.parse_args()
query = args.song

url = 'https://api.genius.com/search?access_token=' + config.auth_token + "&q=" + query
url = url.encode("utf-8")

response = requests.get(url)
title = response.json()["response"]["hits"][0]["result"]["title"]
url = response.json()["response"]["hits"][0]["result"]["url"]
id = response.json()["response"]["hits"][0]["result"]["id"]

url = response.json()["response"]["hits"][0]["result"]["url"]
response = requests.get(url)
soup = bs.BeautifulSoup(response.text)
print(soup.find(class_='lyrics').get_text())