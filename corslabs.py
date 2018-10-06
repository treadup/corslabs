from flask import Flask, request
app = Flask(__name__)

API_HOSTNAME = 'maui.peacefulrainforest.org:5000'
WEBAPP_HOSTNAME = 'kauai.peacefulrainforest.org:5000'

HTML_TEMPLATE = """
<!doctype HTML>
<html>
<head>
  <script src="/static/scripts/index.js"></script>
</head>
<body>
<h3>Web app</h3>
<p>This is the web application. The following data was fetched from the api.</p>
<div id="people" />
</body>
</html>
"""

JAVASCRIPT_CODE = """
// This is the JavaScript code.

"""

@app.route('/')
def index():
    if not 'Host' in request.headers:
        return "Missing Host header."

    host = request.headers['Host']

    if host != WEBAPP_HOSTNAME:
        return "Incorrect hostname", 400

    return HTML_TEMPLATE

@app.route('/static/scripts/index.js')
def javascript():
    if not 'Host' in request.headers:
        return "Missing Host header."

    host = request.headers['Host']

    if host != WEBAPP_HOSTNAME:
        return "Incorrect hostname", 400

    return JAVASCRIPT_CODE

@app.route('/api')
def api():
    if not 'Host' in request.headers:
        return "Missing Host header."

    host = request.headers['Host']

    if host != API_HOSTNAME:
        return "Incorrect hostname", 400

    return {"name": "Superman", "alias": "Clark Kent", "city": "Metropolis"}
