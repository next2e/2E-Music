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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=['POST'])
def submit():
    #http://np1.github.io/pafy/
    url = request.form['video']
    t = threading.Thread(target=addurl, args=(url,))
    t.start()
    return 'Submitted!'

@app.route("/delet")
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
    print(queue)
    return jsonify(queue)

def nextsong():
    print(queue)
    def songproc():
        global current
        print("Opening VLC")
        with open(os.devnull, 'wb') as useless_trash:
            current = subprocess.Popen(['vlc-wrapper', '-I', 'rc', queue.pop(0), '--play-and-exit'],
                        stdout=useless_trash, stderr=useless_trash)
        current.wait()
        current = None
        nextsong()

    if len(queue):
        threading.Thread(target=songproc).start()

def download(total, recvd, ratio, rate, eta):
    print(ratio)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
