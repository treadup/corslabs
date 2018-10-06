import json
from flask import Flask, request, current_app, make_response
app = Flask(__name__)

API_HOSTNAME = 'maui.peacefulrainforest.org:5000'
WEBAPP_HOSTNAME = 'kauai.peacefulrainforest.org:5000'

FULL_WEBAPP_HOSTNAME = "http://" + WEBAPP_HOSTNAME

HTML_TEMPLATE = """
<!doctype HTML>
<html>
<head>
  <script src="/static/scripts/index.js"></script>
</head>
<body>
<h3>Web app</h3>
<p>This is the web application. The following data was fetched from the api.</p>
<pre id="people" />
</body>
</html>
"""

JAVASCRIPT_CODE = """
const apiHostname = 'API_HOSTNAME';
const apiEndpoint = 'http://' + apiHostname + '/api';

fetch(apiEndpoint)
  .then(function(response) {
    return response.json();
  })
  .then(function(supermanJson) {
    const el = document.getElementById('people');

    el.innerText = JSON.stringify(supermanJson);
  })
  .catch(function() {
    console.log("Failed to fetch api data.");
  })

""".replace("API_HOSTNAME", API_HOSTNAME)

@app.route('/', methods=['GET'])
def index():
    if not 'Host' in request.headers:
        return "Missing Host header."

    host = request.headers['Host']

    if host != WEBAPP_HOSTNAME:
        return "Incorrect hostname", 400

    return HTML_TEMPLATE

@app.route('/static/scripts/index.js', methods=['GET'])
def javascript():
    if not 'Host' in request.headers:
        return "Missing Host header."

    host = request.headers['Host']

    if host != WEBAPP_HOSTNAME:
        return "Incorrect hostname", 400

    return JAVASCRIPT_CODE

@app.route('/api', methods=['GET', 'OPTIONS'])
def api():
    if not 'Host' in request.headers:
        return "Missing Host header."

    host = request.headers['Host']

    if host != API_HOSTNAME:
        return "Incorrect hostname", 400

    if request.method == 'OPTIONS':
        response = current_app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = FULL_WEBAPP_HOSTNAME # or "*"
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET'
        response.headers['Access-Control-Allow-Headers'] = ""
        return response
    elif request.method == 'GET':
        response = make_response(json.dumps({"name": "Superman",
                                             "alias": "Clark Kent",
                                             "city": "Metropolis"}))
        response.headers['Access-Control-Allow-Origin'] = FULL_WEBAPP_HOSTNAME # or "*"
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET'
        response.headers['Access-Control-Allow-Headers'] = ""
        return response

    return "Unsupported method", 405
