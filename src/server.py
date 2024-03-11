import os
import sys
from flask import Flask, render_template, request, redirect, g, send_file
import html_sanitizer
import markdown

sys.path.insert(1, './params')
sys.path.insert(1, './utilities')

from limits import *
from agora_errors import *
from logopts import *
from AgoraSyntacticFilter import *
from AgoraSemanticFilter import *
from AgoraInterpreterFilter import *
from AgoraFilter import *
from AgoraDatabaseManager import *
from AgoraEmailer import *
from AgoraFileManager import *

PORT = sys.argv[1]
MAILGUN_KEY = sys.argv[2]
HOST = sys.argv[3]
RECAPTCHA_SITEKEY = sys.argv[4]
RECAPTCHA_SERVERKEY = sys.argv[5]
DEV_EMAILS = sys.argv[6]
POSTDIR = './volumes/posts/'
IMGDIR = './volumes/img'
LOGDIR = './volumes/logs'

agoraInterpreter = AgoraInterpreterFilter(None)
agoraSemantics = AgoraSemanticFilter(agoraInterpreter)
agoraSyntax = AgoraSyntacticFilter(agoraSemantics)

agoraDB = AgoraDatabaseManager("./volumes/agora.db")
agoraSemantics.setDBManager(agoraDB)
agoraInterpreter.setDBManager(agoraDB)

agoraEmail = AgoraEmailer(MAILGUN_KEY, HOST)
agoraEmail.setDeveloperEmails(DEV_EMAILS)
agoraInterpreter.setEmailer(agoraEmail)

agoraFM = AgoraFileManager(POSTDIR, IMGDIR, LOGDIR)
agoraSemantics.setFileManager(agoraFM)
agoraInterpreter.setFileManager(agoraFM)

agoraSemantics.setReCaptchaKey(RECAPTCHA_SERVERKEY)
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

sanitizerSettings = dict(html_sanitizer.sanitizer.DEFAULT_SETTINGS)
sanitizerSettings['tags'].add('img')
sanitizerSettings['tags'].add('center')
sanitizerSettings['empty'].add('img')
sanitizerSettings['attributes'].update({'img': ('src',)})
sanitizer = html_sanitizer.Sanitizer(settings=sanitizerSettings)     # We're using the library's default configuration

@app.errorhandler(AgoraException)
def agoraError(err):
    if isinstance(err, AgoraEInvalidToken) or isinstance(err, AgoraENotLoggedIn):
        return redirect('/login')
    g.data.update(handleAgoraError(err))
    return render_template('error.html', data=g.data)

@app.before_request
def agoraPreproc():
    agoraDB.connect()
    g.data = {}
    g.data["recaptcha_sitekey"] = RECAPTCHA_SITEKEY
    g.sessionToken = request.cookies.get("session")
    try:
        g.data["logged_in_user"] = agoraModel.getMyUser(g.sessionToken, concise=True)
    except AgoraException as err:
        g.data["logged_in_user"] = None

@app.route('/')
def home():
    return render_template('index.html', data=g.data)

@app.route('/users')
def users():
    return "Coming soon..."

@app.route('/user/<uid>')
def user(uid):
    userInfo = {}
    myInfo = None
        
    userInfo = agoraModel.getUser(uid)

    if g.data['logged_in_user'] is not None:
        myInfo = agoraModel.getMyUser(g.sessionToken) 
        
        if uid == str(g.data['logged_in_user']['uid']):
            userInfo = myInfo

    g.data.update(userInfo)
    g.data['logged_in_user'] = myInfo

    return render_template('profile.html', data=g.data, limits=INPUT_LENGTH_LIMITS)

@app.route('/post/<pid>')
def post(pid):
    get_post_content(pid)
    return render_template('post.html', data=g.data, limits=INPUT_LENGTH_LIMITS)

def get_post_content(pid):
    postInfo = agoraModel.getPost(pid)
    md_content = agoraFM.getPost(postInfo['filename'])
    html_content = sanitizer.sanitize(markdown.markdown(md_content))
    postInfo["content"] = html_content
    postInfo["raw_content"] = md_content
    g.data.update(postInfo)
    
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
    agoraModel.createAccount(data['email'], data['username'], data['password'], data['g-recaptcha-response'])
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
    sessionToken = agoraModel.login(data['username'], data['password'], data['g-recaptcha-response'])
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

@app.route('/settings')
def settings_get():
    if g.data['logged_in_user'] is not None:
        userInfo = agoraModel.getMyUser(g.sessionToken)
        g.data.update(userInfo)
        return render_template('settings.html', data=g.data, limits=INPUT_LENGTH_LIMITS)
    return redirect('/login')

@app.route('/settings', methods=['POST'])
def settings_post():
    return redirect('/account')

@app.route('/backup')
def backup_get():
    return render_template('recover-account.html', data=g.data)

@app.route('/backup', methods=['POST'])
def backup_post():
    data = request.form
    if 'email' in data and 'code' in data:
        agoraModel.backupRecover(data['code'], data['email'])
    return render_template('info.html', data=g.data, msg='backup-sent-email')

@app.route('/changepass')
def change_password_request_get():
    return render_template('reset-password.html', data=g.data)

@app.route('/changepass', methods=['POST'])
def change_password_request_post():
    data = request.form
    if "email" in data:
        agoraModel.recoverAccount(data["email"])
    return render_template('info.html', data=g.data, msg='recovery-sent-email')

@app.route('/changepass/<token>')
def change_password_get(token):
    g.data['token'] = token
    return render_template('new-password.html', data=g.data)

@app.route('/changepass/<token>', methods=['POST'])
def change_password_post(token):
    data = request.form
    if "password" in data:
        agoraModel.confirmRecover(token, data["password"])
        return render_template('info.html', data=g.data, msg='confirm-password-reset')
    return redirect('/login')

@app.route('/confirmemail/<token>')
def confirm_email(token):
    agoraModel.confirmEmail(token)
    return redirect("/account")

@app.route('/write')
def new_post():
    g.data['new_post'] = True
    return render_template('write-post.html', data=g.data, limits=INPUT_LENGTH_LIMITS)

@app.route('/write', methods=['POST'])
def write_post():
    data = request.form
    pid = agoraModel.writePost(g.sessionToken, data["title"], data["content"], data["g-recaptcha-response"])
    return redirect(f'/post/{pid}')

@app.route('/edit/<pid>')
def edit_post_view(pid):
    get_post_content(pid)
    return render_template('write-post.html', data=g.data, limits=INPUT_LENGTH_LIMITS)

@app.route('/edit/<pid>', methods=['POST'])
def edit_post(pid):
    data = request.form
    agoraModel.editPost(g.sessionToken, pid, data["title"], data["content"])
    return redirect(f"/post/{pid}")

@app.route('/deletepost/<pid>', methods=['POST'])
def delete_post(pid):
    agoraModel.deletePost(g.sessionToken, pid)
    return redirect("/files")

@app.route('/comment/<pid>', methods=['POST'])
def write_comment(pid):
    data = request.form
    agoraModel.comment(g.sessionToken, pid, data['content'], data['g-recaptcha-response'])
    return redirect(f"/post/{pid}")

@app.route('/deletecomment/<cid>', methods=['POST'])
def delete_comment(cid):
    pid = agoraModel.deleteComment(g.sessionToken, cid)
    return redirect(f"/post/{pid}")

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

@app.route('/vote/<pid>', methods=['POST'])
def vote(pid):
    data = request.form
    if 'vote' in data:
        match data['vote']:
            case 'like': 
                agoraModel.like(g.sessionToken, pid)
            case 'dislike': 
                agoraModel.dislike(g.sessionToken, pid) 
            case 'unlike': 
                agoraModel.unlike(g.sessionToken, pid)
            case _: 
                print('help!')
    return redirect(f'/post/{pid}')

@app.route('/upload', methods=['POST'])
def upload_image_post():
    imgData = request.files['file']
    data = request.form
    title = data['title']
    imgID = agoraModel.uploadImage(g.sessionToken, title, imgData)
    return redirect(f'/userimg/{imgID}')

@app.route('/upload')
def upload_image_get():
    return render_template('upload.html', data=g.data)

@app.route('/files')
def files():
    if g.data['logged_in_user'] is None:
        return redirect('/')
    userInfo = agoraModel.getMyUser(g.sessionToken)
    g.data.update(userInfo)
    return render_template('files.html', data=g.data)
    

@app.route('/deleteimg', methods=['POST'])
def delete_image():
    data = request.form
    if 'delete' in data:
        agoraModel.deleteImage(g.sessionToken, data['delete'])
    return redirect('/files')

@app.route('/search', methods=['POST'])
def search():
    data = request.form
    if 'user' in data:
        get_search('user', data['user'])
    if 'post' in data:
        get_search('post', data['post'])
    return render_template('search.html', data=g.data)

@app.route('/browse/users')
def browse_users():
    get_search('user', "")
    return render_template('browse.html', data=g.data)

@app.route('/browse/posts')
def browse_posts():
    get_search('post', "")
    return render_template('browse.html', data=g.data)

def get_search(querytype, query):
    results = []
    if querytype == 'user':
        results = agoraModel.searchUsers(query)
    if querytype == 'post':
        results = agoraModel.searchPosts(query)
    g.data['results'] = results
    g.data['querytype'] = querytype

@app.route('/friend/<uid>', methods=['POST'])
def friend(uid):
    agoraModel.friendRequest(g.sessionToken, uid)
    data = request.form
    if 'redirect' in data:
        return redirect(data['redirect'])
    return redirect('/account')

@app.route('/unfriend/<uid>', methods=['POST'])
def unfriend(uid):
    agoraModel.unfriend(g.sessionToken, uid)
    data = request.form
    if 'redirect' in data:
        return redirect(data['redirect'])
    return redirect('/account')

@app.route('/report')
def bug_report_get():
    return render_template('report.html', data=g.data, limits=INPUT_LENGTH_LIMITS)

@app.route('/report', methods=['POST'])
def bug_report_post():
    data = request.form
    if "content" in data:
        agoraModel.bugReport(g.sessionToken, data["content"])
    return render_template('info.html', data=g.data, msg='confirm-report-submitted')

app.run(host = "0.0.0.0", port = PORT)
