from flask import Flask, render_template, jsonify, request
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from key import access_key, secret_key
app = Flask(__name__)

host = 'search-twittmap-gd24ezicbcw3tycn7wkpyiv2li.us-west-2.es.amazonaws.com'
awsauth = AWS4Auth(access_key, secret_key, 'us-west-2', 'es')
es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
print(es.info())

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('googleMap.html')

@app.route('/queryES/<key>', methods=['POST'])
def queryES(key):
	res = es.search(index='index', doc_type='twitter', size=1000, from_=0, body={"query":{'match':{"tweet": key}}})
	print res
	return jsonify(res['hits']['hits'])

if __name__ == "__main__":
	app.run();
