from dotenv import load_dotenv
import os
import html
import requests
import json
import csv

def save_to_csv(json_data, filename):
    with open(filename+'.csv', 'w', newline='') as f:


load_dotenv()

# create url
url = 'https://api.twitter.com/2/tweets/search/recent?query='
# querying
# https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
query = '#FineFaunart has:media'
# queries must be http encoded
# if you don't want to do it manually:
# https://www.urlencoder.io/python/
query = '%23FineFaunart%20has%3Amedia%20-is%3Aretweet'
# queries don't return media by default
# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/media
# https://twittercommunity.com/t/how-to-get-media-url/141863/16
expansion = '&expansions=attachments.media_keys&media.fields=preview_image_url,url,type'
url += query
url += expansion
headers = {'Authorization' : f'Bearer {os.getenv("TOKEN")}'}
response = requests.request('GET', url, headers=headers)
if(response.status_code != 200):
	raise Exception(
        "Request returned an error: {} {}".format(
            response.status_code, response.text
        )
    )
print(json.dumps(response.json()))

data = json.dumps(response.json())

# while next token do that
# https://developer.twitter.com/en/docs/twitter-api/pagination
# &next_token=token to add
all_data = []

# collect all data and put it in list
# write to csv once all data collected
