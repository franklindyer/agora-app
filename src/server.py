import sys
from flask import Flask

sys.path.insert(1, './params')
sys.path.insert(1, './utilities')

from limits import *
from agora_errors import *
from AgoraSyntacticFilter import *

app = Flask(__name__)

@app.route('/')
def home():
    return "Home page!"

app.run()
