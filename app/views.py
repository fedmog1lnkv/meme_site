from flask import render_template, g, flash, session, abort, redirect, url_for
from flask import request
from app import app, sql
import os
from app.db_classes import FDataBase, User
from werkzeug.utils import secure_filename
from app.image import post_image

posts = [  # список выдуманных постов
    {
        'author': 'Рабинович',
        'name_post': 'Когда ушёл после 9 класса',
        'like_count': 20,
        'comments': ['рили ржака', 'жоский мем', 'блин, вот бы тяночку'],
        'image': 'https://avatars.mds.yandex.net/i?id=f04884cd53ec2d8698a2ca02e0635767-5134183-images-thumbs&n=13'
    },
    {
        'author': 'Петрушин',
        'name_post': 'Это халяль брат',
        'like_count': 40,
        'comments': ['я скучаю, зай', 'жоский мем', 'блин, вот бы тяночку'],
        'image': 'https://storage.vsemayki.ru/images/0/1/1081/1081078/previews/people_701_holst_square_full_front_white_500.jpg'
    }
]

import sqlite3

app.config.from_object('app.configs')
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'database.db')))


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


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}
    db = get_db()
    dbase = FDataBase(db)
    css = [(url_for('static', filename='css/cardStyles.css'))]
    posts, times = dbase.getPosts()
    print(times)
    return render_template("index.html", menu=dbase.getMenu(), count=len(times), user=user, posts=posts, times=times, css=css)


@app.route('/create_post', methods=['POST', 'GET'])
def create_post():
    db = get_db()
    dbase = FDataBase(db)
    css = [(url_for('static', filename='css/cardStyles.css')), (url_for('static', filename='css/profileStyles.css'))]
    if request.method == 'POST':
        print(request.form, type(request.form))
        print(request.files['file'].filename)
        print()
        request.files['file'].save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(request.files['file'].filename)))
        url = post_image(request.files['file'].filename)
        title = request.form.get('title')
        content = request.form.get('content')
        if dbase.addPost(title, content, url):
            flash('Пост отправлен', category='success')
        else:
            flash('Ошибка добавления', category='error')
        # sql.add_post(request.form)
        return render_template('create_post.html', title=title, content=content, css=css)
    return render_template('create_post.html', title="sss", content="ddd", css=css)


@app.route('/profile/<username>')
def profile_user(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        session.clear()
        abort(401)
    return f"Пользователь: {username}"

@app.route('/profile')
def profile():
    if 'userLogged' in session:
        db = get_db()
        dbase = FDataBase(db)
        user = User(session['userId'], dbase)
        css = [(url_for('static', filename='css/cardStyles.css')), (url_for('static', filename='css/profileStyles.css'))]
        return render_template('profile.html', user=user.getAllInfo(), css=css)
    return redirect('/login')

@app.route("/login", methods=["POST", "GET"])
def login():
    db = get_db()
    dbase = FDataBase(db)
    css = [(url_for('static', filename='css/cardStyles.css')), (url_for('static', filename='css/profileStyles.css'))]
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == "admin" and request.form['pwd'] == 'admin':
        session['userLogged'] = request.form['username']
        return redirect((url_for('profile', username=session['userLogged'])))

    return render_template('login.html', css=css)

@app.route('/reg', methods=["POST", "GET"])
def reg():
    db = get_db()
    dbase = FDataBase(db)
    css = [(url_for('static', filename='css/cardStyles.css')), (url_for('static', filename='css/profileStyles.css'))]
    if request.method == "POST":
        username = request.form['username']
        pwd = request.form['pwd']
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
