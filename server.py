from flask import Flask, render_template, request
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
    return "Stopped current song"

def addurl(url):
    video = pafy.new(url)
    filename = video.getbestaudio().download(filepath='files', quiet=True, callback=download)
    queue.append(filename)
    if not current:
        nextsong()

def nextsong():
    print(queue)
    def songproc():
        global current
        current = subprocess.Popen(['vlc', queue.pop(0), '--play-and-exit'])
        current.wait()
        nextsong()

    if len(queue):
        threading.Thread(target=songproc).start()

def download(total, recvd, ratio, rate, eta):
    print(ratio)

if __name__ == "__main__":
    app.run(debug=True)
