from pymongo import MongoClient
from dotenv import load_dotenv
import os
import csv

load_dotenv()
client = MongoClient(f'mongodb+srv://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@cluster0.narps.mongodb.net/gallerytw?retryWrites=true&w=majority')
db = client['Cluster0']

def upload_media():
	media = db.media
	with open('forfauna-media.csv', newline='', encoding='utf-8') as f:
		reader = csv.reader(f)
		next(reader)

		for row in reader:
			media.insert_one({'media_key':row[0], 'url':row[1], 'type':row[2]})
		
#upload_media()
def upload_tweets():
	tweets = db.tweets
	with open('forfauna-tweets.csv', newline='', encoding='utf-8') as f:
		reader = csv.reader(f)
		next(reader)

		for row in reader:
			tweets.insert_one({'id':row[0], 'text':row[1], 'media_keys':row[2]})

upload_tweets()

#tweet.insert_one({'a':'a'})