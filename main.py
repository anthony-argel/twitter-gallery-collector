from dotenv import load_dotenv
import os
import html
import requests
import json
import csv


load_dotenv()

class hashtag_collector:
    def __init__(self):
        self.tweets = []
        self.meta = []
        self.media = []

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

        self.meta = data['meta']
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
    # while next token do that
    # https://developer.twitter.com/en/docs/twitter-api/pagination
    # &next_token=token to add

    def save_to_csv(self, filename):
        with open(f'{filename}-tweets.csv', 'w', newline='', encoding= 'utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'text', 'media_keys'])
            for tweet in self.tweets:
                writer.writerow([str(tweet['id']), tweet['text'], tweet['attachments']['media_keys']])

        with open(f'{filename}-media.csv', 'w', newline='', encoding= 'utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['media_key', 'url', 'type', 'hashtag'])
            for content in self.media:
                if('preview_image_url' in content):
                    writer.writerow([str(content['media_key']), content['preview_image_url'], content['type'], filename])
                else:
                    writer.writerow([str(content['media_key']), content['url'], content['type'], filename])
            
        with open(f'{filename}-meta.csv', 'w', newline='', encoding= 'utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['newest_id', 'oldest_id'])
            writer.writerow([str(self.meta['newest_id']), str(self.meta['oldest_id'])])


    def start(self):
        # create url
        url = 'https://api.twitter.com/2/tweets/search/recent?query='
        # querying
        # https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
        # query = '#FineFaunart has:media'
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

        data = self.get_data(url)
        self.parse_data(data)        

        while('next_token' in self.meta.keys()):
            headers = {'Authorization' : f'Bearer {os.getenv("TOKEN")}'}
            current_url = url
            current_url += f'&pagination_token={self.meta["next_token"]}'
            data = self.get_data(current_url)
            self.parse_data(data)

        self.save_to_csv('finefaunart')


hashtag_collector = hashtag_collector()
hashtag_collector.start()