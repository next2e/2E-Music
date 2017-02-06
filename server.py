from flask import Flask, render_template, request
from requests import get
import json
import pafy
import subprocess
import os
import threading
app = Flask(__name__)

current = None

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
    current.kill()
    return "Stopped current song"

def addurl(url):
    video = pafy.new(url)
    filename = video.getbestaudio().download(filepath='files', quiet=True, callback=download)
    global current
    current = subprocess.Popen(['cvlc', filename, '--play-and-exit'])

def download(total, recvd, ratio, rate, eta):
    print(ratio)

if __name__ == "__main__":
    app.run(debug=True)
