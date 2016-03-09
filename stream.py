from flask import Flask, request, render_template, send_from_directory
from flask.ext.api import status
import psycopg2
import config
import requests

app = Flask(__name__)

hostname = 'http://[hostname]/hls/'

@app.route('/auth')
def auth():
	if request.args.get('name') is None or request.args.get('swfurl') is None:
		return 'Malformed request', status.HTTP_400_BAD_REQUEST
	
	username = request.args.get('name')
	idhash = request.args.get('swfurl').split("?")[-1]
        
	conn = psycopg2.connect(database=config.database, user=config.user, password=config.password, host=config.host)
	cur = conn.cursor()
	cur.execute("SELECT * FROM users WHERE username=%s AND idhash=%s", (username, idhash))
	
	if len(cur.fetchall()) == 0:
		return 'Incorrect credentials', status.HTTP_401_UNAUTHORIZED

	return 'OK', status.HTTP_200_OK

@app.route('/dist/<path:path>')
def serve_js(path):
    return send_from_directory('dist', path)

@app.route('/<username>')
def serve_player(username):
    conn = psycopg2.connect(database=config.database, user=config.user, password=config.password, host=config.host)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s", (username,))
    if len(cur.fetchall()) == 0:
        return "No such user!"
    else:
        r = requests.get(hostname + username + ".m3u8")
        if r.status_code == requests.codes.ok:
            return render_template('player.html', username=username);
        else:
            return "Stream offline!"

if __name__== '__main__':
    app.run(host='0.0.0.0')
