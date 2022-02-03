from pymongo import MongoClient
from dotenv import load_dotenv
import os
import csv
from datetime import datetime

load_dotenv()
client = MongoClient(f'mongodb+srv://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@cluster0.narps.mongodb.net/gallerytw?retryWrites=true&w=majority')
db = client['gallerytw']

def upload_media(hashtag):
	media = db.media
	with open(f'data/{datetime.now().strftime("%d-%m-%Y")}/{hashtag}-media.csv', newline='', encoding='utf-8') as f:
		reader = csv.reader(f)
		next(reader)

		for row in reader:
			media.insert_one({'media_key':row[0], 'url':row[1], 'type':row[2], 'hashtag':hashtag})
		
def upload_tweets(hashtag):
	tweets = db.tweets
	with open(f'data/{datetime.now().strftime("%d-%m-%Y")}/{hashtag}-tweets.csv', newline='', encoding='utf-8') as f:
		reader = csv.reader(f)
		next(reader)


		for row in reader:
			media_keys = []
			keys = row[2].split("\'")
			for key in keys:
				if(key == '[' or key == ']'):
					continue
				else:
					media_keys.append(key)

			tweets.insert_one({'id':row[0], 'text':row[1], 'media_keys':media_keys})

def upload_meta(hashtag):
	meta = db.metas
	with open(f'data/{datetime.now().strftime("%d-%m-%Y")}/{hashtag}-meta.csv', newline='', encoding='utf-8') as f:
		reader = csv.reader(f)
		next(reader)

		for row in reader:
			meta.insert_one({'newestid':row[0], 'hashtag':hashtag})

def upload_all(hashtag):
	upload_media(hashtag)
	upload_tweets(hashtag)
	upload_meta(hashtag)

upload_all(hashtag = 'finefaunart')