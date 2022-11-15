import sqlite3
from app.image import post_image
from datetime import datetime

def add_post(post_info):
    print(__name__)
    conn = sqlite3.connect("memes.db", check_same_thread=False)
    cursor = conn.cursor()

    title = post_info.get('title')
    content = post_info.get('content')
    author_id = 1 # пока 1, потом из сессии парсить будем
    url = post_image("apple.jpg", "1")
    cursor.execute("INSERT INTO posts (title, content, author_id, url) VALUES (?, ?, ?, ?)", (title, content, author_id, url))
    conn.commit()
    cursor.close()
    conn.close()

#cursor.execute(f"INSERT INTO users (username, password, date) VALUES ('gigachad', 'qwer', '${datetime.today()}')")


def close_all():
    cursor.close()
    conn.close()

#cursor.execute('SELECT * FROM users')

#record = cursor.fetchall()
#print(record)

# Создание таблиц (пользователи и посты)

# cursor.execute('''
#     CREATE TABLE users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         username VARCHAR(120) NOT NULL,
#         date TEXT NOT NULL
#     )
# ''')
#
# cursor.execute('''
#     CREATE TABLE posts (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         title VARCHAR(128),
#         author_id INT,
#         content TEXT,
#         url TEXT,
#         FOREIGN KEY (author_id) REFERENCES users(id)
#     )
# ''')
