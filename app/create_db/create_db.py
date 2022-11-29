import sqlite3
from flask import Flask
import bcrypt

USERNAME_ADMIN = "admin"
PASSWORD_ADMIN = "admin"

app = Flask(__name__)


def connect_db():
    conn = sqlite3.connect('app/database.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def write_admin():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users VALUES(NULL, ?, ?, ?)",
                   (USERNAME_ADMIN, bcrypt.hashpw(PASSWORD_ADMIN.encode(), bcrypt.gensalt()), 0))
    db.commit()
    db.close()


def first_post():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)",
                   ("Быстрый старт", 0, "https://i.ibb.co/q7m9cXB/first-post.jpg", 1))
    db.commit()
    db.close()


create_db()
write_admin()
first_post()
