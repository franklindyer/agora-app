import os
import sys
from flask import Flask, render_template, request, redirect
import markdown

sys.path.insert(1, './params')
sys.path.insert(1, './utilities')

from limits import *
from agora_errors import *
from AgoraSyntacticFilter import *
from AgoraSemanticFilter import *
from AgoraInterpreterFilter import *
from AgoraFilter import *
from AgoraDatabaseManager import *
from AgoraEmailer import *
from AgoraFileManager import *

PORT = sys.argv[1]
GMAIL_KEY = sys.argv[2]
HOST = sys.argv[3]
POSTDIR = './volumes/posts/'

agoraInterpreter = AgoraInterpreterFilter(None)
agoraSemantics = AgoraSemanticFilter(agoraInterpreter)
agoraSyntax = AgoraSyntacticFilter(agoraSemantics)

agoraDB = AgoraDatabaseManager("./volumes/agora.db")
agoraSemantics.setDBManager(agoraDB)
agoraInterpreter.setDBManager(agoraDB)

agoraEmail = AgoraEmailer("agoradevel@gmail.com", GMAIL_KEY)
agoraInterpreter.setEmailer(agoraEmail)

agoraFM = AgoraFileManager(POSTDIR)
agoraInterpreter.setFileManager(agoraFM)

agoraInterpreter.setHost(HOST)

# Entry point for Agora Model
agoraModel = agoraSyntax

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
        return render_template('index.html')
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

@app.route('/join')
def join_get():
    try:
        return render_template('join.html', limits=INPUT_LENGTH_LIMITS)
    except AgoraException as err:
        return render_template('error.html', data=handleAgoraError(err))

@app.route('/join', methods=['POST'])
def join_post():
    data = request.form
    try:
        agoraModel.createAccount(data['email'], data['username'], data['password'])
        return render_template('info.html', msg='confirm-sent-email')
    except AgoraException as err:
        return render_template('error.html', data=handleAgoraError(err))

@app.route('/confirm/<token>')
def confirm(token):
    try:
        agoraModel.confirmCreate(token)
        return redirect('/')
    except AgoraException as err:
        return render_template('error.html', data=handleAgoraError(err))

@app.route('/login')
def login_get():
    try:
        return render_template('login.html')
    except AgoraException as err:
        return render_template('error.html', data=handleAgoraError(err))

@app.route('/login', methods=['POST'])
def login_post():
    data = request.form
    try:
        sessionToken = agoraModel.login(data['username'], data['password'])
        resp = redirect("/account")
        resp.set_cookie("session", sessionToken)
        return resp
    except AgoraException as err:
        return render_template('error.html', data=handleAgoraError(err))

@app.route('/logout', methods=['POST'])
def logout():
    sessionToken = request.cookies.get("session")
    try:
        agoraModel.logout(sessionToken)
        return render_template('info.html', msg='logout')
    except AgoraException as err:
        return render_template('error.html', data=handleAgoraError(err))

@app.route('/account')
def account():
    sessionToken = request.cookies.get("session")
    try:
        data = agoraModel.getMyUser(sessionToken)
        return render_template('account.html', data=data)
    except AgoraException as err:
        return render_template('error.html', data=handleAgoraError(err))

@app.route('/set', methods=['POST'])
def account_set():
    sessionToken = request.cookies.get("session")
    data = request.form
    try:
        if "status" in data:
            agoraModel.changeStatus(sessionToken, data['status'])
        if "username" in data:
            agoraModel.changeUsername(sessionToken, data['username'])
        return redirect("/account")
    except AgoraException as err:
        return render_template('error.html', data=handleAgoraError(err))

@app.route('/write', methods=['POST'])
def write_post():
    sessionToken = request.cookies.get("session")
    data = request.form
    try:
        agoraModel.writePost(sessionToken, data["title"], data["content"])
        return redirect("/account")
    except AgoraException as err:
        return render_template('error.html', data=handleAgoraError(err))

app.run(host = "0.0.0.0", port = PORT)
