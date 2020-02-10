import requests
# import pdb

r = requests.get('https://genius.com')
print(r)
print(r.text)
# pdb.set_trace()