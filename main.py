from hashtag_collector import hashtag_collector
from mongo import upload_all, get_latest_ids


hashtag_collector = hashtag_collector()

# updating the database
hashtag_data = get_latest_ids()
# if you want to use your own hashtags, remember to remove the hash symbol
# example: 
# hashtag_data = ['hashtag1', 'hashtag2', 'hashtag3']
for data in hashtag_data:
	if(isinstance(data, dict)):
		result = hashtag_collector.start(data['_id'], data['newestid'])
		if(result != -1):
			upload_all(data['_id'])
	else:
		hashtag_collector.start(data)
		upload_all(data)
