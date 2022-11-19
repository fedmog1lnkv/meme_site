from flask import render_template, g, flash, session, abort, redirect, url_for
from flask import request
from app import app
import os
from app.db_classes import FDataBase, User, UserLogin
from werkzeug.utils import secure_filename
from app.image import post_image
import sqlite3
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app.config.from_object('app.configs')
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'database.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к данной страницы необходимо авторизироваться'
login_manager.login_message_category = 'success'
@login_manager.user_loader
def load_user(user_id):
    print("load_user")
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


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


# @app.errorhandler(401)
# def notThisUser(error):
#     redirect(url_for('login'))


@app.route('/')
@app.route('/index')
def index():
    print(session)
    css = [(url_for('static', filename='css/cardStyles.css'))]
    posts, times = dbase.getPosts()
    return render_template("index.html", menu=dbase.getMenu(), count=len(times), posts=posts, times=times, css=css)


@app.route('/create_post', methods=['POST', 'GET'])
@login_required
def create_post():
    css = [(url_for('static', filename='css/cardStyles.css')), (url_for('static', filename='css/profileStyles.css'))]
    if request.method == 'POST':
        print(request.form, type(request.form))
        print(request.files['file'].filename)
        print()
        request.files['file'].save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(request.files['file'].filename)))
        url = post_image(request.files['file'].filename)
        title = request.form.get('title')
        if dbase.addPost(title, url, session['_user_id']):
            flash('Пост отправлен', category='success')
        else:
            flash('Ошибка добавления', category='error')
        # sql.add_post(request.form)
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
    return render_template('profile.html', css=css, user=current_user.get_info())

@app.route("/login", methods=["POST", "GET"])
def login():
    css = [(url_for('static', filename='css/cardStyles.css')), (url_for('static', filename='css/profileStyles.css'))]
    if request.method == "POST":
        user = dbase.getUserName(request.form['username'])
        rm = 'rb_me' in request.form
        if user and request.form['pwd'] == user['password']:
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
    css = [(url_for('static', filename='css/cardStyles.css')), (url_for('static', filename='css/profileStyles.css'))]
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
        res = dbase.addUser(username, pwd)
        if type(res) != str:
            id = dbase.getUserName(username)[0]
            session['userLogged'] = username
            session['userId'] = id
            print(session)
            return redirect('/profile')
        else:
            if res == "UNIQUE constraint failed: users.username":
                flash('Такой пользователь уже существует', 'error')
            else:
                flash('Ошибка регистрации', 'error')
    return render_template('reg.html', css=css)
