import tweepy
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import sys
from key import access_key, secret_key

reload(sys)
sys.setdefaultencoding("utf-8")

#Elastic Search Information
host = 'search-twittmap-gd24ezicbcw3tycn7wkpyiv2li.us-west-2.es.amazonaws.com'
awsauth = AWS4Auth(access_key, secret_key, 'us-west-2', 'es')

# Set up elastic search instance
es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

# Drop down of 10 keywords
term = raw_input('Search on Twitter for:')

# Twitter Information
API_KEY = "7cqDHDwTgcQYYo21UjPfkrZtC"
API_SECRET =	"GcnuwbZpdYcoh2O64MVhtR6dssCI2tS9i0dJQLCigRUAMkyrdi"
ACCESS_TOKEN = "3431454303-nQTAecbq8UbEyE8CyNLLLWy4W3EWjWF0XQpiVWx"
ACCESS_TOKEN_SECRET = "Lt7r3rpxEMeWkGRxpcNXHMbD4XLit5MLCxBkZB4z7SZ6W"

key = tweepy.OAuthHandler(API_KEY, API_SECRET)
key.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

class Stream2Screen(tweepy.StreamListener):
    def on_status(self, status):
        if status.coordinates:
            coord = status.coordinates
            # Pass back tweets and coordinates
            post = {
                   'tweet': status.text,
                   'coordinates': coord['coordinates']
            }
            # Store the tweets on elastic search index (database)
            # Searchable documents column updates on website
            es.index(index="index",
                    doc_type="twitter",
                    body=post)

stream = tweepy.streaming.Stream(key, Stream2Screen())
stream.filter(track=[term]) 