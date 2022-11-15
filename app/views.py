from flask import render_template
from flask import request
from app import app
from app import sql



@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}
    posts = [ # список выдуманных постов
        { 
            'author': 'Рабинович',
            'name_post': 'Когда ушёл после 9 класса',
            'like_count': 20,
            'comments' : ['рили ржака', 'жоский мем', 'блин, вот бы тяночку'],
            'image': 'https://avatars.mds.yandex.net/i?id=f04884cd53ec2d8698a2ca02e0635767-5134183-images-thumbs&n=13' 
        },
        { 
            'author': 'Петрушин',
            'name_post': 'Это халяль брат',
            'like_count': 40,
            'comments' : ['я скучаю, зай', 'жоский мем', 'блин, вот бы тяночку'],
            'image':'https://storage.vsemayki.ru/images/0/1/1081/1081078/previews/people_701_holst_square_full_front_white_500.jpg' 

        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts = posts)

@app.route('/create_post', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        print(request.form, type(request.form))
        title = request.form.get('title')
        content = request.form.get('content')
        sql.add_post(request.form)
        return render_template('create_post.html', title=title, content=content)
    return render_template('create_post.html', title="sss", content="ddd")
