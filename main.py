from hashtag_collector import hashtag_collector
from mongo import upload_all

hashtag = 'FineFaunart'

#hashtag_collector = hashtag_collector()
#hashtag_collector.start(hashtag)
upload_all(hashtag)