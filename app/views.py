from flask import render_template
from flask import request
from app import app
from app import sql



@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}
    return render_template("index.html",
                           title='Home',
                           user=user)

@app.route('/create_post', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        print(request.form, type(request.form))
        title = request.form.get('title')
        content = request.form.get('content')
        sql.add_post(request.form)
        return render_template('create_post.html', title=title, content=content)
    return render_template('create_post.html', title="sss", content="ddd")
