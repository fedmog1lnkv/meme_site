import sqlite3
from datetime import datetime

conn = sqlite3.connect('memes.db')
cursor = conn.cursor()

# cursor.execute(f"INSERT INTO users (username, password, date) VALUES ('gigachad', 'qwer', '${datetime.today()}')")
# conn.commit()
# print()

cursor.execute('SELECT * FROM users')
record = cursor.fetchall()
print(record)

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
#         id INT PRIMARY KEY,
#         title VARCHAR(128),
#         author_id INT,
#         content TEXT,
#         url TEXT,
#         FOREIGN KEY (author_id) REFERENCES users(id)
#     )
# ''')

cursor.close()
conn.close()