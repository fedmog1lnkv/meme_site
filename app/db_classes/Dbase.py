import time
import sqlite3
from app.db_classes.functions import timeAgo, secondsToDate


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ощибка чтения БД")
        return []


    def addPost(self, title, url, author_id):
        try:
            tm = time.time()
            self.__cur.execute('INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)', (title, tm, url, author_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления в БД " + str(e))
            return False

        return True

    def getPosts(self):
        sql = '''SELECT posts.id, posts.title, posts.time, posts.url, users.username  FROM posts, users WHERE posts.author_id=users.id ORDER BY posts.time DESC'''
        print('pdspd')
        try:
            print('aaa')
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            times = []
            for i in range(len(res)):
                times.append(timeAgo(time.time() - res[i][2]))
            print('bb')
            if res:
                return res, times
        except:
            print("Ощибка чтения БД")
        return [], []


    def getPost(self, id):
        sql = f"select * from posts where id={id}"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if res: return res
        except:
            print("Ощибка чтения БД")
        return False


    def getImg(self, id):
        sql = f"SELECT image FROM posts WHERE id='{id}'"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ощибка чтения БД")
        return False

    def addUser(self, username, pwd):
        try:
            tm = time.time()
            self.__cur.execute('INSERT INTO users VALUES(NULL, ?, ?, ?)', (username, pwd, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления в БД " + str(e))
            return str(e)

        return True

    def getUserId(self, id):
        sql = f"select * from users where id={id}"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            print(res)
            if res: return res
        except:
            print("Ощибка чтения БД")
        return False
    def getUserName(self, name):
        sql = f"select * from users where username='{name}'"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if res: return res
        except:
            print("Ощибка чтения БД")
        return False
class User:
    def __init__(self, id, dbase):
        data = dbase.getUserId(id)
        self.__id = data[0]
        self.__username = data[1]
        self.__time = data[3]

    def getAllInfo(self):
        return [self.__id, self.__username, secondsToDate(self.__time)]

