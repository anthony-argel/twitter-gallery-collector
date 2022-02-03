from dotenv import load_dotenv
import os
import html
import requests
import json
import csv
from datetime import datetime
import urllib.parse


load_dotenv()

def check_directory(directory):
    if not os.path.exists(directory):
            os.makedirs(directory)

class hashtag_collector:
    def __init__(self):
        self.tweets = []
        self.meta = []
        self.media = []
        self.newest_id = 0

    def get_data(self, url):
        headers = {'Authorization' : f'Bearer {os.getenv("TOKEN")}'}
        response = requests.request('GET', url, headers=headers)
        if(response.status_code != 200):
        	raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return(response.json())

    def parse_data(self, response):
        l_tweet = []
        l_media = []
        data = response
        l_tweet = data['data']
        l_media = data['includes']['media']
        meta = data['meta']

        if(self.newest_id < int(meta['newest_id'])):
            self.newest_id = int(meta['newest_id'])
        self.meta = meta
        self.tweets.extend(data['data'])
        self.media.extend(data['includes']['media'])

        print()
        print(meta)
        print()
        print(l_tweet)
        print(len(l_tweet))
        print(len(self.tweets))
        print()
        print(l_media)
        print(len(l_media))

    def save_to_csv(self, filename):
        check_directory('data')
        check_directory(f'data/{datetime.now().strftime("%d-%m-%Y")}')
        with open(f'data/{datetime.now().strftime("%d-%m-%Y")}/{filename}-tweets.csv', 'w', newline='', encoding= 'utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'text', 'media_keys'])
            self.tweets.reverse()
            for tweet in self.tweets:
                writer.writerow([str(tweet['id']), tweet['text'], tweet['attachments']['media_keys']])

        with open(f'data/{datetime.now().strftime("%d-%m-%Y")}/{filename}-media.csv', 'w', newline='', encoding= 'utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['media_key', 'url', 'type', 'hashtag'])
            self.media.reverse()
            for content in self.media:
                if('preview_image_url' in content):
                    writer.writerow([str(content['media_key']), content['preview_image_url'], content['type'], filename])
                else:
                    writer.writerow([str(content['media_key']), content['url'], content['type'], filename])
            
        with open(f'data/{datetime.now().strftime("%d-%m-%Y")}/{filename}-meta.csv', 'w', newline='', encoding= 'utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['newest_id', 'oldest_id'])
            writer.writerow([str(self.meta['newest_id']), str(self.meta['oldest_id'])])


    def start(self, hashtag, newest_id = -1):
        url = 'https://api.twitter.com/2/tweets/search/recent?query='
        # querying
        # https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
        # query = '#FineFaunart has:media'
        # queries must be http encoded
        # if you don't want to do it manually:
        # https://www.urlencoder.io/python/
        query = f'#{hashtag} has:media -is:retweet'
        # queries don't return media by default
        # https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/media
        # https://twittercommunity.com/t/how-to-get-media-url/141863/16
        expansion = '&expansions=attachments.media_keys&media.fields=preview_image_url,url,type&max_results=100'

        query = urllib.parse.quote(query)
        print(query)
        query += expansion
        url += query
        if(newest_id != -1):
            url += f'&since_id={newest_id}'

        data = self.get_data(url)
        self.parse_data(data)        

        while('next_token' in self.meta.keys()):
            headers = {'Authorization' : f'Bearer {os.getenv("TOKEN")}'}
            current_url = url
            current_url += f'&pagination_token={self.meta["next_token"]}'
            data = self.get_data(current_url)
            self.parse_data(data)

        self.save_to_csv(hashtag)