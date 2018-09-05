from flask import Flask, render_template, request, jsonify
from gevent.pywsgi import WSGIServer
from requests import get
from random import choice
import sys
import json
import pafy
import subprocess
import os
import threading
app = Flask(__name__)

current = None
queue = []
now = 'files/Nothing currently playing.mp3'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=['POST'])
def submit():
    #http://np1.github.io/pafy/
    url = request.form['video']
    t = threading.Thread(target=addurl, args=(url,))
    t.start()
    return 'ok'

@app.route("/quiet")
def quiet():
    queue.insert(0, 'files_Be quiet!.mp3')
    if current:
        skip()
    else:
        nextsong()
    return ''

@app.route("/skip")
def skip():
    global current
    current.kill()
    current = None
    return ''

@app.route("/delete", methods=['POST'])
def delete():
    song = int(request.form['song']) - 1
    queue.pop(song)
    return ''

@app.route("/playsong", methods=['POST'])
def play_song():
    song = request.form['song']
    queue.append('files/' + song);
    if not current:
        nextsong()
    return ''

@app.route("/search")
def search():
    q = request.args.get('query')
    all_songs = os.listdir('files')
    results = [s for s in all_songs if q.lower() in s.lower()]
    return jsonify(results[:50])

@app.route("/volup")
def volup():
    subprocess.call(['./volup.sh'], shell=True)
    return ''

@app.route("/voldown")
def voldown():
    subprocess.call(['./voldown.sh'], shell=True)
    return ''

@app.route('/random')
def random():
    queue.append('files/'+choice(os.listdir('files')))
    if not current:
        nextsong()
    return ''

@app.route('/shuffle')
def shuffle():
    songs = []
    all_songs = os.listdir('files')
    if len(all_songs) <= 20:
        return jsonify(all_songs)

    while len(songs) < 20:
        s = choice(os.listdir('files'))
        if s not in songs:
            songs.append(s)
    return jsonify(list(songs))

def addurl(url):
    video = pafy.new(url)
    filename = video.getbestaudio().download(filepath='files', quiet=True, callback=download)
    queue.append(filename)
    if not current:
        nextsong()

@app.route("/queue")
def getqueue():
    global now
    output = [now] + queue
    output = ['.'.join(a.split('.')[:-1])[6:] for a in output]
    return jsonify(output)

def nextsong():
    def songproc():
        global current
        global now
        print("Opening VLC")
        now = queue.pop(0)
        with open(os.devnull, 'wb') as useless_trash:
            current = subprocess.Popen(['vlc-wrapper', '-I', 'rc', now, '--play-and-exit'],
                        stdout=useless_trash, stderr=useless_trash)
        current.wait()
        now = 'files/Nothing currently playing.mp3'
        current = None
        nextsong()

    if len(queue):
        threading.Thread(target=songproc).start()

def download(total, recvd, ratio, rate, eta):
    print(ratio)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'production':
        http_server = WSGIServer(('0.0.0.0', 80), app)
    else:
        http_server = WSGIServer(('', 5000), app)

    http_server.serve_forever()
