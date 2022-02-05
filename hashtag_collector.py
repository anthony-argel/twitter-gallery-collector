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
        self.oldest_id = -1

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
        if (isinstance(data, dict) == False):
            print('a dictionary wasnt returned')
            print(type(data))
            print(data)
            return -1
        if (data['meta']['result_count'] == 0):
            return -1
        l_tweet = data['data']
        l_media = data['includes']['media']
        meta = data['meta']

        if(self.newest_id < int(meta['newest_id'])):
            self.newest_id = int(meta['newest_id'])
        if(self.oldest_id == -1 or self.oldest_id > int(meta['oldest_id'])):
            self.oldest_id = int(meta['oldest_id'])
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
        check_directory(f'data/{datetime.now().strftime("%Y-%m-%d")}')
        with open(f'data/{datetime.now().strftime("%Y-%m-%d")}/{filename}-tweets.csv', 'w', newline='', encoding= 'utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'text', 'media_keys'])
            self.tweets.reverse()
            for tweet in self.tweets:
                writer.writerow([str(tweet['id']), tweet['text'], tweet['attachments']['media_keys']])

        with open(f'data/{datetime.now().strftime("%Y-%m-%d")}/{filename}-media.csv', 'w', newline='', encoding= 'utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['media_key', 'url', 'type', 'hashtag', 'tweet_text', 'id'])
            self.media.reverse()
            for content in self.media:
                temp_id = -1
                temp_text = ''
                for tweet in self.tweets:
                    if(content['media_key'] in tweet['attachments']['media_keys']):
                        temp_text = tweet['text']
                        temp_id = str(tweet['id']) 


                if('preview_image_url' in content):
                    writer.writerow([str(content['media_key']), content['preview_image_url'], content['type'], filename, temp_text, temp_id])
                else:
                    writer.writerow([str(content['media_key']), content['url'], content['type'], filename,temp_text, temp_id])
            
        with open(f'data/{datetime.now().strftime("%Y-%m-%d")}/{filename}-meta.csv', 'w', newline='', encoding= 'utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['newest_id', 'oldest_id'])
            writer.writerow([self.newest_id, self.oldest_id])


    def start(self, hashtag, newest_id = -1):
        self.tweets = []
        self.meta = []
        self.media = []
        self.newest_id = 0
        self.oldest_id = -1
        url = 'https://api.twitter.com/2/tweets/search/recent?query='
        query = f'#{hashtag} has:media -is:retweet'
        expansion = '&expansions=attachments.media_keys&media.fields=preview_image_url,url,type&max_results=100'

        query = urllib.parse.quote(query)
        query += expansion
        url += query
        if(newest_id != -1):
            print('updating from ' + newest_id)
            url += f'&since_id={newest_id}'

        data = self.get_data(url)
        if(self.parse_data(data) == -1):
            print('no new images found')
            return -1

        while('next_token' in self.meta.keys()):
            headers = {'Authorization' : f'Bearer {os.getenv("TOKEN")}'}
            current_url = url
            current_url += f'&pagination_token={self.meta["next_token"]}'
            data = self.get_data(current_url)
            self.parse_data(data)

        self.save_to_csv(hashtag)