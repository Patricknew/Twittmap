from flask import Flask, render_template
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

res = es.search(index='index', doc_type='twitter')
print res['hits']['hits']
@app.route('/', methods=["GET"])
def index():
    return render_template('googleMap.html')

# @app.route('/hello')
# def hello():
#     return 'Hello World'

if __name__ == "__main__":
	app.run();

# from flask import Flask, render_template, jsonify
# import requests
# from key import key
# app = Flask(__name__)

# search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
# details_url = "https://maps.googleapis.com/maps/api/place/details/json"

# @app.route("/", methods=["GET"])
# def retreive():
#     return render_template('layout.html') 

# @app.route("/sendRequest/<string:query>")
# def results(query):
# 	search_payload = {"key":key, "query":query}
# 	search_req = requests.get(search_url, params=search_payload)
# 	search_json = search_req.json()

# 	place_id = search_json["results"][0]["place_id"]

# 	details_payload = {"key":key, "placeid":place_id}
# 	details_resp = requests.get(details_url, params=details_payload)
# 	details_json = details_resp.json()

# 	url = details_json["result"]["url"]
# 	return jsonify({'result' : url})


# if __name__ ==  "__main__":
#     app.run(debug=True)