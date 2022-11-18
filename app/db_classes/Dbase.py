import time
import sqlite3

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


    def addPost(self, title, content, url):
        try:
            tm = time.time()
            self.__cur.execute('INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)', (title, content, tm, url))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления в БД " + str(e))
            return False

        return True

    def getPosts(self):
        sql = '''SELECT * FROM posts'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ощибка чтения БД")
        return []


    def getPost(self, id):
        sql = "select * from posts where id=2"
        try:
            self.__cur.execute(sql)
            print(sql)
            res = self.__cur.fetchone()
            print(res)
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