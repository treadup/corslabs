from flask import Flask, request
app = Flask(__name__)

API_HOSTNAME = 'maui.peacefulrainforest.org:5000'
WEBAPP_HOSTNAME = 'kauai.peacefulrainforest.org:5000'

def to_html(content):
    return f"<html>\n\t<body>\n\t\t{content}\t</body>\n</html>"

def webapp_index():
    return to_html("""<p>This host is the app host. This <a href="/view">/view</a>
                      contains a web page that makes a fetch call to the api.</p>
                   """)

def api_index():
    return to_html("""<p>This host is the api host. The api has a single endpoint
                      called <a href="/api">/api</a>
                   """)

@app.route('/')
def index():
    if not 'Host' in request.headers:
        return "Missing Host header."

    host = request.headers['Host']

    if host == API_HOSTNAME:
        return api_index()
    elif host == WEBAPP_HOSTNAME:
        return webapp_index()
    else:
        return f'Unknown host: {host}'

@app.route('/view')
def view():
    if not 'Host' in request.headers:
        return "Missing Host header."

    host = request.headers['Host']

    if host != WEBAPP_HOSTNAME:
        return "Incorrect hostname", 400

    return "This is the view"

@app.route('/api')
def api():
    if not 'Host' in request.headers:
        return "Missing Host header."

    host = request.headers['Host']

    if host != API_HOSTNAME:
        return "Incorrect hostname", 400

    return {"name": "Henrik", "city": "Stockholm"}
