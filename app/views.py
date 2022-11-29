from flask import render_template, g, flash, session, abort, redirect, url_for
from flask import request
from app import app
import os
from app.db_classes import FDataBase, UserLogin
from werkzeug.utils import secure_filename
from app.image import post_image
import sqlite3
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import bcrypt

app.config.from_object('app.configs')
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'database.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к данной страницы необходимо авторизироваться'
login_manager.login_message_category = 'success'


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route('/')
@app.route('/index')
def index():
    css = [(url_for('static', filename='css/cardStyles.css'))]
    if "_user_id" in session:
        user_id = session['_user_id']
    else:
        user_id = 0

    posts, times, likes, liked_by_user = dbase.getPosts(user_id)
    if user_id != 0:
        user_name = current_user.get_username()
    else:
        user_name = ""
    return render_template("index.html", menu=dbase.getMenu(), count=len(times), posts=posts, times=times, likes=likes,
                           liked_by_user=liked_by_user, user_name=user_name, css=css)


@app.route('/like_loader', methods=["POST", "GET"])
def like_loader():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        post_id = str(request.data).split("=")[-1].split('\'')[0]
        if '_user_id' in session:
            user_id = session["_user_id"]
        else:
            user_id = 0
        res = dbase.addLike(post_id, user_id)
        print(res)
        if res:
            return f"{res}"
        else:
            return "0"


@app.route('/delete_post', methods=["POST", "GET"])
def delete_post():
    post_id = str(request.data).split("=")[-1].split('\'')[0]
    db = get_db()
    dbase = FDataBase(db)
    res = dbase.deletePost(post_id)
    return res


@app.route("/liked")
@login_required
def liked():
    css = [(url_for('static', filename='css/cardStyles.css'))]
    posts, times, likes, liked_by_user = dbase.getPosts(session['_user_id'])
    user_id = 0
    user_name = ""
    if "_user_id" in session:
        user_id = session["_user_id"]
        user_name = current_user.get_username()

    return render_template("liked.html", menu=dbase.getMenu(), count=len(liked_by_user), posts=posts, times=times,
                           likes=likes, liked_by_user=liked_by_user, user_name=user_name, css=css)


@app.route('/create_post', methods=['POST', 'GET'])
@login_required
def create_post():
    css = [(url_for('static', filename='css/cardStyles.css')), (url_for('static', filename='css/profileStyles.css'))]
    if request.method == 'POST':
        if secure_filename(request.files['file'].filename):
            request.files['file'].save(
                os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                             session["_user_id"] + "." + secure_filename(
                                 request.files['file'].filename.split(".")[-1])))
            url = post_image(session["_user_id"] + "." + secure_filename(request.files['file'].filename.split(".")[-1]))
            title = request.form.get('title')
            if dbase.addPost(title, url, session['_user_id']):
                flash('Пост отправлен', category='success')
            else:
                flash('Ошибка добавления', category='error')
            return render_template('create_post.html', css=css)

    return render_template('create_post.html', title="sss", content="ddd", css=css)


@app.route('/profile/<username>')
def profile_user(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        session.clear()
        abort(401)
    return f"Пользователь: {username}"


@app.route('/profile')
@login_required
def profile():
    css = [(url_for('static', filename='css/cardStyles.css')), (url_for('static', filename='css/profileStyles.css'))]
    user_id = session["_user_id"]
    print(dbase.getUserPosts(user_id))
    posts, times, likes, liked_by_user = dbase.getUserPosts(user_id)
    print(len(times))
    return render_template('profile.html', css=css, user=current_user.get_info(), count=len(times), posts=posts,
                           times=times, likes=likes, liked_by_user=liked_by_user)


@app.route("/login", methods=["POST", "GET"])
def login():
    css = [(url_for('static', filename='css/cardStyles.css')), (url_for('static', filename='css/profileStyles.css'))]
    if request.method == "POST":
        user = dbase.getUserName(request.form['username'])
        rm = 'rb_me' in request.form
        if user and bcrypt.checkpw(request.form['pwd'].encode(), user['password']):
            userLogin = UserLogin().create(user)
            login_user(userLogin, remember=rm)
            return redirect(request.args.get('next') or url_for('profile'))
        flash("Неверный логин или пароль", "error")
    return render_template('login.html', css=css)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('login'))


@app.route('/reg', methods=["POST", "GET"])
def reg():
    css = [(url_for('static', filename='css/cardStyles.css'))]
    if request.method == "POST":
        username = request.form['username']
        pwd = request.form['pwd']
        pwd_ag = request.form['pwd_ag']
        if pwd != pwd_ag:
            flash('Пароль не совпадают', 'error')
            return render_template('reg.html', css=css)
        if len(pwd) < 4:
            flash('Пароль должен быть не меньше 4 символов', 'error')
            return render_template('reg.html', css=css)
        if len(username) < 4:
            flash('Имя пользователя должно быть не меньше 4 символов', 'error')
            return render_template('reg.html', css=css)
        res = dbase.addUser(username, bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()))
        if type(res) != str:
            id = dbase.getUserName(username)[0]
            session['userLogged'] = username
            session['userId'] = id
            return redirect(url_for('login'))
        else:
            if res == "UNIQUE constraint failed: users.username":
                flash('Такой пользователь уже существует', 'error')
            else:
                flash('Ошибка регистрации', 'error')
    return render_template('reg.html', css=css)
