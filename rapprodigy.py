from RapGetter import RapGetter
from MarkovRap import MarkovRap

import os
from twilio.rest import Client

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
fake_rap = rap.next_letter("broke a") 
print(fake_rap)

# account_sid = "ACb5407cc24afbc49989f0d556f9c79dbd"
# auth_token = "ba3638225089714093744ac9c736af26"

# client = Client(account_sid, auth_token)

# client.messages.create(
# 	to="+16095535610",
# 	from_="+12015970044",
# 	body=fake_rap
# )

from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])

def sms_reply():
	resp = MessagingResponse()

	resp.message(fake_rap)

	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)