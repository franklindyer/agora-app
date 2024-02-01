import os
import sys
from flask import Flask, render_template
import markdown

sys.path.insert(1, './params')
sys.path.insert(1, './utilities')

from limits import *
from agora_errors import *
from AgoraSyntacticFilter import *
from AgoraSemanticFilter import *
from AgoraFilter import *
from AgoraDatabaseManager import *
from AgoraEmailer import *

PORT = sys.argv[1]
GMAIL_KEY = sys.argv[2]

agoraInterpreter = AgoraFilter(None)
agoraSemantics = AgoraSemanticFilter(agoraInterpreter)
agoraSyntax = AgoraSyntacticFilter(agoraSemantics)

agoraDB = AgoraDatabaseManager("./volumes/agora.db")
agoraSemantics.setDBManager(agoraDB)

agoraEmail = AgoraEmailer("agoradevel@gmail.com", GMAIL_KEY)

# Entry point for Agora Model
agoraModel = agoraSyntax

POSTDIR = './volumes/posts/'

def handleAgoraError(err):
    return {
        "success": 0,
        "error": type(err).__name__
    }

app = Flask(__name__)
app.debug = True

@app.errorhandler(500)
def error500(err):
    return "Something went wrong server-side. Oopsie!"

@app.route('/')
def home():
    try:
        return "Home page!"
    except AgoraException as err:
        return render_template('error.html', data=handleAgoraError(err))

@app.route('/users')
def users():
    try:
        return "Coming soon..."
    except AgoraException as err:
        return render_template('error.html', data=handleAgoraError(err))

@app.route('/user/<uid>')
def user(uid):
    try:
        user_info = agoraModel.getUser(uid)
        user_info["success"] = 1
        return render_template('profile.html', data=user_info)
    except AgoraException as err:
        return render_template('error.html', data=handleAgoraError(err))

@app.route('/post/<pid>')
def post(pid):
    try:
        post_info = agoraModel.getPost(pid)
        content = open(os.path.join(POSTDIR, post_info['filename'])).read()
        html_content = markdown.markdown(content)
        post_info["content"] = html_content
        post_info["success"] = 1
        return render_template('post.html', data=post_info)
    except AgoraException as err:
        return render_template('error.html', data=handleAgoraError(err))

app.run(host = "0.0.0.0", port = PORT)
