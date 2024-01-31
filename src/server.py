import sys
from flask import Flask

sys.path.insert(1, './params')
sys.path.insert(1, './utilities')

from limits import *
from agora_errors import *
from AgoraSyntacticFilter import *
from AgoraSemanticFilter import *
from AgoraFilter import *
from AgoraDatabaseManager import *

agoraInterpreter = new AgoraFilter(None)
agoraSemantics = new AgoraSemanticFilter(agoraInterpreter)
agoraSyntax = new AgoraSyntacticFiter(agoraSemantics)

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

app.run(host = "0.0.0.0", port = sys.argv[1])
