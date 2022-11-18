from flask import render_template, g
from flask import request
from app import app, sql
import os
from app.db_classes import FDataBase
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
    print(dbase.getPosts()[0][2])
    return render_template("posts.html", menu=dbase.getMenu(), user=user, posts=dbase.getPosts())

@app.route('/create_post', methods=['POST', 'GET'])
def create_post():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        print(request.form, type(request.form))
        print(request.files['file'].filename)
        print()
        request.files['file'].save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(request.files['file'].filename)))
        url = post_image(request.files['file'].filename)
        title = request.form.get('title')
        content = request.form.get('content')
        dbase.addPost(title, content, url)
        #sql.add_post(request.form)
        return render_template('create_post.html', title=title, content=content)
    return render_template('create_post.html', title="sss", content="ddd")
