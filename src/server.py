import sys
from flask import Flask, render_template

sys.path.insert(1, './params')
sys.path.insert(1, './utilities')

from limits import *
from agora_errors import *
from AgoraSyntacticFilter import *
from AgoraSemanticFilter import *
from AgoraFilter import *
from AgoraDatabaseManager import *

agoraInterpreter = AgoraFilter(None)
agoraSemantics = AgoraSemanticFilter(agoraInterpreter)
agoraSyntax = AgoraSyntacticFilter(agoraSemantics)

agoraDB = AgoraDatabaseManager("./volumes/agora.db")
agoraSemantics.setDBManager(agoraDB)

# Entry point for Agora Model
agoraModel = agoraSyntax

app = Flask(__name__)

@app.errorhandler(500)
def error500():
    return "Something went wrong server-side. Oopsie!"

@app.route('/')
def home():
    return "Home page!"

@app.route('/users')
def users():
    return "Coming soon..."

@app.route('/user/<uid>')
def user(uid):
    user_info = agoraModel.getUser(uid)
    return render_template('profile.html', data=user_info)

app.run(host = "0.0.0.0", port = sys.argv[1])
