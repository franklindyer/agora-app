import os
import sys
from flask import Flask, render_template, request, redirect, g, send_file
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
IMGDIR = './volumes/img'

agoraInterpreter = AgoraInterpreterFilter(None)
agoraSemantics = AgoraSemanticFilter(agoraInterpreter)
agoraSyntax = AgoraSyntacticFilter(agoraSemantics)

agoraDB = AgoraDatabaseManager("./volumes/agora.db")
agoraSemantics.setDBManager(agoraDB)
agoraInterpreter.setDBManager(agoraDB)

agoraEmail = AgoraEmailer("agoradevel@gmail.com", GMAIL_KEY)
agoraInterpreter.setEmailer(agoraEmail)

agoraFM = AgoraFileManager(POSTDIR, IMGDIR)
agoraInterpreter.setFileManager(agoraFM)

agoraInterpreter.setHost(HOST)

# Entry point for Agora Model
agoraModel = agoraSyntax

def handleAgoraError(err):
    return {
        "success": 0,
        "error": type(err).__name__
    }

def agoraerror(pageserver):
    def wrapper(*args):
        try:
            pageserver(*args)
        except AgoraException as err:
            g.data['logged_in_user'] = None
            g.data.update(handleAgoraError(err))
            return render_template('error.html', data=g.data)

app = Flask(__name__)
app.debug = True


@app.errorhandler(AgoraException)
def agoraError(err):
    g.data.update(handleAgoraError(err))
    return render_template('error.html', data=g.data)

@app.before_request
def agoraPreproc():
    agoraDB.connect()
    g.data = {}
    g.sessionToken = request.cookies.get("session")
    try:
        g.data["logged_in_user"] = agoraModel.getMyUser(g.sessionToken, concise=True)
    except AgoraEInvalidToken as err:
        g.data["logged_in_user"] = None

@app.route('/')
def home():
    return render_template('index.html', data=g.data)

@app.route('/users')
def users():
    return "Coming soon..."

@app.route('/user/<uid>')
def user(uid):
    if g.data['logged_in_user'] is None or uid != g.data['logged_in_user']['uid']:
        userInfo = agoraModel.getUser(uid)
        g.data.update(userInfo)
    return render_template('profile.html', data=g.data, limits=INPUT_LENGTH_LIMITS)

@app.route('/post/<pid>')
def post(pid):
    postInfo = agoraModel.getPost(pid)
    content = agoraFM.getPost(postInfo['filename'])
    html_content = markdown.markdown(content)
    postInfo["content"] = html_content
    g.data.update(postInfo)
    return render_template('post.html', data=g.data)

@app.route('/userimg/<accessid>')
def user_image(accessid):
    imgname = agoraModel.getImage(accessid)
    filepath = agoraFM.relativizeImagePath(imgname)
    return send_file(filepath, mimetype='image/gif')

@app.route('/join')
def join_get():
    return render_template('join.html', data=g.data, limits=INPUT_LENGTH_LIMITS)

@app.route('/join', methods=['POST'])
def join_post():
    data = request.form
    agoraModel.createAccount(data['email'], data['username'], data['password'])
    return render_template('info.html', data=g.data, msg='confirm-sent-email')

@app.route('/join/<token>')
def join_confirm(token):
    agoraModel.confirmCreate(token)
    return redirect('/')

@app.route('/leave', methods=['POST'])
def leave_post():
    formdata = request.form
    agoraModel.deleteAccount(g.sessionToken, formdata['password'])
    return render_template('info.html', data=g.data, msg='leave-sent-email')

@app.route('/leave/<token>')
def leave_confirm(token):
    agoraModel.confirmDelete(token)
    return render_template('info.html', data=g.data, msg='goodbye')

@app.route('/login')
def login_get():
    return render_template('login.html', data=g.data)

@app.route('/login', methods=['POST'])
def login_post():
    data = request.form
    sessionToken = agoraModel.login(data['username'], data['password'])
    resp = redirect("/account")
    resp.set_cookie("session", sessionToken)
    return resp

@app.route('/logout', methods=['POST'])
def logout():
    agoraModel.logout(g.sessionToken)
    return render_template('info.html', data=g.data, msg='logout')

@app.route('/account')
def account_get():
    if g.data['logged_in_user'] is not None:
        data = agoraModel.getMyUser(g.sessionToken)
        return redirect(f"/user/{data['uid']}")
    return redirect('/login')

@app.route('/account', methods=['POST'])
def account_post():
    data = request.form
    if "status" in data:
        agoraModel.changeStatus(g.sessionToken, data['status'])
    if "username" in data:
        agoraModel.changeUsername(g.sessionToken, data['username'])
    if "pfp" in data:
        agoraModel.changePicture(g.sessionToken, data['pfp'])
    if "email" in data:
        agoraModel.changeEmail(g.sessionToken, data['email'])
    return redirect("/account")

@app.route('/backup/<code>', methods=['POST'])
def backup_post(code):
    data = request.form
    if "email" in data:
        agoraModel.backupRecover(code, data['email'])
    return render_template('info.html', data=g.data, msg='backup-sent-email')

@app.route('/confirmemail/<token>')
def confirm_email(token):
    agoraModel.confirmEmail(token)
    return redirect("/account")

@app.route('/write', methods=['POST'])
def write_post():
    data = request.form
    agoraModel.writePost(g.sessionToken, data["title"], data["content"])
    return redirect("/account")

@app.route('/deletepost/<pid>', methods=['POST'])
def delete_post(pid):
    agoraModel.deletePost(g.sessionToken, pid)
    return redirect("/account")

@app.route('/comment', methods=['POST'])
def write_comment():
    data = request.form
    agoraModel.comment(g.sessionToken, data['pid'], data['content'])
    return redirect(f"/post/{data['pid']}")

@app.route('/admin/user/<uid>')
def admin_userview(uid):
    userInfo = agoraModel.adminGetUser(g.sessionToken, uid)
    g.data.update(userInfo)
    return render_template('admin_userview.html', data=g.data)

@app.route('/admin/suspend/<uid>', methods=['POST'])
def admin_suspend(uid):
    agoraModel.adminSuspend(g.sessionToken, uid)
    return redirect(f"/admin/user/{uid}")

@app.route('/admin/unsuspend/<uid>', methods=['POST'])
def admin_unsuspend(uid):
    agoraModel.adminUnsuspend(g.sessionToken, uid)
    return redirect(f"/admin/user/{uid}")

@app.route('/admin/deleteuser/<uid>', methods=['POST'])
def admin_deleteuser(uid):
    data = request.form
    agoraModel.adminDelete(g.sessionToken, uid, data["password"])
    return redirect("/")

@app.route('/upload', methods=['POST'])
def upload_image():
    imgData = request.files['file']
    title = imgData.filename
    agoraModel.uploadImage(g.sessionToken, title, imgData)
    return redirect('/account')

@app.route('/deleteimg/<imgid>', methods=['POST'])
def delete_image(imgid):
    agoraModel.deleteImage(g.sessionToken, imgid)
    return redirect('/account')

@app.route('/search', methods=['POST'])
def search():
    data = request.form
    results = []
    querytype = ""
    if "user" in data:
        querytype = "user"
        results = agoraModel.searchUsers(data["user"])
    if "post" in data:
        querytype = "post"
        results = agoraModel.searchPosts(data["post"])
    g.data["querytype"] = querytype
    g.data["results"] = results
    return render_template("results.html", data=g.data)

app.run(host = "0.0.0.0", port = PORT)
