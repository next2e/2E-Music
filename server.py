from flask import Flask, render_template, request, jsonify
from requests import get
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

@app.route("/skip")
def delet():
    global current
    current.kill()
    current = None
    return ''

@app.route("/volup")
def volup():
    subprocess.call(['./volup.sh'], shell=True)
    return ''

@app.route("/voldown")
def voldown():
    subprocess.call(['./voldown.sh'], shell=True)
    return ''

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
    #app.run(host="0.0.0.0", port=80, debug=True)
    app.run(debug=True)
