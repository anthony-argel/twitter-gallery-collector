from pymongo import MongoClient
from dotenv import load_dotenv
import os
import csv

load_dotenv()
client = MongoClient(f'mongodb+srv://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@cluster0.narps.mongodb.net/gallerytw?retryWrites=true&w=majority')
db = client['Cluster0']

hashtag = 'finefaunart'

def upload_media():
	media = db.media
	with open(f'{hashtag}-media.csv', newline='', encoding='utf-8') as f:
		reader = csv.reader(f)
		next(reader)

		for row in reader:
			media.insert_one({'media_key':row[0], 'url':row[1], 'type':row[2], 'hashtag':hashtag})
		
def upload_tweets():
	tweets = db.tweets
	with open(f'{hashtag}-tweets.csv', newline='', encoding='utf-8') as f:
		reader = csv.reader(f)
		next(reader)

		for row in reader:
			tweets.insert_one({'id':row[0], 'text':row[1], 'media_keys':row[2]})

def upload_meta():
	meta = db.metas
	with open(f'{hashtag}-meta.csv', newline='', encoding='utf-8') as f:
		reader = csv.reader(f)
		next(reader)

		for row in reader:
			meta.insert_one({'newestid':row[0], 'hashtag':hashtag})

def upload_all():
	upload_media()
	upload_tweets()
	upload_meta()

upload_all()