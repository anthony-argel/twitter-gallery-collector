# twitter-gallery-expander
This project uses the Twitter API to collect images from an inserted hashtag and save it to a CSV. Once the CSV is confirmed to be correct, you can then store the data in whatever database you want. (I personally used MongoDB)

From main.py, insert the hashtag you want to collect data from into the hashtag variable. If any of the lines in main.py are commented out, that's a mistake. All of the lines should be uncommented.

Some notes:
	1. You need a Twitter Developer account
	2. The Developer account has a monthly limit
	3. With the base Developer account you can only collect tweets from the last 7 days