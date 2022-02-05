from pymongo import MongoClient
from dotenv import load_dotenv
import os
import csv
from datetime import datetime

load_dotenv()
client = MongoClient(f'mongodb+srv://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@cluster0.narps.mongodb.net/gallerytw?retryWrites=true&w=majority')
db = client['gallerytw']

def get_latest_ids(): 
	call = [{'$group':{'_id':'$hashtag', 'newestid':{'$last':'$newestid'}}}]
	metas = db.metas
	results = metas.aggregate(call)	
	return (results)

def upload_media(hashtag,date):
	media = db.media
	path = ''
	if(date == None):
		path = f'data/{datetime.now().strftime("%Y-%m-%d")}/{hashtag}-media.csv'
	else:
		path = f'data/{date}/{hashtag}-media.csv'
	with open(path, newline='', encoding='utf-8') as f:
		reader = csv.reader(f)
		next(reader)

		for row in reader:
			media.insert_one({'media_key':row[0], 'url':row[1], 'type':row[2], 'hashtag':hashtag, 'tweet':row[4], 'id':row[5]})
		
def upload_tweets(hashtag,date):
	tweets = db.tweets
	path = ''
	if(date == None):
		path = f'data/{datetime.now().strftime("%Y-%m-%d")}/{hashtag}-tweets.csv'
	else:
		path = f'data/{date}/{hashtag}-tweets.csv'
	with open(path, newline='', encoding='utf-8') as f:
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

def upload_meta(hashtag, date):
	meta = db.metas
	path = ''
	if(date == None):
		path = f'data/{datetime.now().strftime("%Y-%m-%d")}/{hashtag}-meta.csv'
	else:
		path = f'data/{date}/{hashtag}-meta.csv'
	with open(path, newline='', encoding='utf-8') as f:
		reader = csv.reader(f)
		next(reader)

		for row in reader:
			meta.insert_one({'newestid':row[0], 'hashtag':hashtag})

def upload_all(hashtag, date = None):
	print('sending to the database...')
	upload_media(hashtag, date)
	upload_tweets(hashtag, date)
	upload_meta(hashtag, date)