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

    def deletePost(self, post_id):
        try:
            self.__cur.execute(f"DELETE FROM posts WHERE id={post_id}")
            self.__cur.execute(f"DELETE FROM likes WHERE post_id={post_id}")
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка удаления из БД " + str(e))
            return "0"
        return "1"

    def getUserPosts(self, user_id):
        sql = f'''SELECT posts.id, posts.title, posts.time, posts.url, users.username FROM posts, users WHERE posts.author_id={user_id} and users.id=posts.author_id ORDER BY posts.time DESC'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            for i in res:
                for j in i:
                    print(j, "что нахуй")
                print()
            likes = self.getLikes()
            if user_id != 0:
                liked_by_user = self.getLikedByUser(user_id)
            else:
                liked_by_user = []
            times = []
            likes_counts = []
            liked_by_user_counts = []
            j = 0
            c = 0
            # for item in liked_by_user:
            #     for i in item:
            #         print(i)
            #     print()

            for i in range(len(res)):
                times.append(timeAgo(time.time() - res[i][2]))
                if len(likes) != 0:
                    while (res[i][0] < likes[j][0] and j < len(likes) - 1):
                        j += 1
                    if res[i][0] == likes[j][0]:
                        likes_counts.append(likes[j][1])
                    else:
                        likes_counts.append(0)
                else:
                    likes_counts.append(0)
                if len(liked_by_user) != 0:
                    while (res[i][0] < liked_by_user[c][0] and c < len(liked_by_user) - 1):
                        c += 1
                    if res[i][0] == liked_by_user[c][0]:
                        liked_by_user_counts.append(liked_by_user[c][0])
                    else:
                        liked_by_user_counts.append(0)
                else:
                    liked_by_user_counts.append(0)
            print(res, times, likes_counts, liked_by_user_counts)
            if res:
                return res, times, likes_counts, liked_by_user_counts
            else:
                return [], [], [], []
        except sqlite3.Error as e:
            print("Ошибка добавления в БД " + str(e))
            return [], [], [], []

    def getPosts(self, user_id = 0):
        sql = '''SELECT posts.id, posts.title, posts.time, posts.url, users.username  FROM posts, users WHERE posts.author_id=users.id ORDER BY posts.time DESC'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            likes = self.getLikes()
            if user_id != 0:
                liked_by_user = self.getLikedByUser(user_id)
            else:
                liked_by_user = []
            times = []
            likes_counts = []
            liked_by_user_counts = []
            j = 0
            c = 0
            for item in liked_by_user:
                for i in item:
                    print(i)
                print()

            for i in range(len(res)):
                times.append(timeAgo(time.time() - res[i][2]))
                if len(likes) != 0:
                    while (res[i][0] < likes[j][0] and j < len(likes) - 1):
                        j += 1
                    if res[i][0] == likes[j][0]:
                        likes_counts.append(likes[j][1])
                    else:
                        likes_counts.append(0)
                else:
                    likes_counts.append(0)
                if len(liked_by_user) != 0:
                    while (res[i][0] < liked_by_user[c][0] and c < len(liked_by_user) - 1):
                        c += 1
                    if res[i][0] == liked_by_user[c][0]:
                        liked_by_user_counts.append(liked_by_user[c][0])
                    else:
                        liked_by_user_counts.append(0)
                else:
                    liked_by_user_counts.append(0)

            if res:
                return res, times, likes_counts, liked_by_user_counts
            else:
                return [], [], [], []
        except sqlite3.Error as e:
            print("Ошибка добавления в БД " + str(e))
            return [], [], [], []


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
    def addLike(self, post_id, user_id):
        if user_id != 0:
            sql = f"select * from likes where post_id={post_id} and user_id={user_id}"
            try:
                self.__cur.execute(sql)
                res = self.__cur.fetchone()
                if res:
                    self.__cur.execute(f"DELETE FROM likes WHERE post_id={post_id} and user_id={user_id}")
                    print("DELETED")
                else:
                    self.__cur.execute("INSERT INTO likes VALUES(NULL, ?, ?)", (post_id, user_id))
                    print("ADDED")
                self.__db.commit()
            except sqlite3.Error as e:
                print("Ошибка добавления в БД " + str(e))
                return False

        sql = f"select count(*) from likes where post_id={post_id}"
        self.__cur.execute(sql)
        res = self.__cur.fetchone()
        print(res)
        return res[0]


    def getLikedByUser(self, user_id):
        sql = f"SELECT post_id, count(*) FROM likes WHERE user_id = {user_id} GROUP BY post_id ORDER BY post_id DESC"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        if res:
            return res
        else:
            return []
    def getLikes(self):
        sql = "SELECT post_id, count(*) FROM likes GROUP BY post_id ORDER BY post_id DESC"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        return res

    def getLikedPosts(self, user_id):
        sql = f"SELECT posts.id, posts.title, posts.time, posts.url, users.username, count(likes.post_id) FROM posts, likes, users WHERE likes.user_id = {user_id} and posts.id = likes.post_id and posts.author_id=users.id GROUP BY posts.id"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            times = []

            for i in range(len(res)):
                times.append(timeAgo(time.time() - res[i][2]))

            if len(res) > 0:
                print(res, 'kek')
                print(times, 'lol')
                return res, times
            else:
                return [], []
        except sqlite3.Error as e:
            print("Ошибка добавления в БД " + str(e))
            return [], []


class User:
    def __init__(self, id, dbase):
        data = dbase.getUserId(id)
        self.__id = data[0]
        self.__username = data[1]
        self.__time = data[3]

    def getAllInfo(self):
        return [self.__id, self.__username, secondsToDate(self.__time)]

    def getName(self):
        return self.__username

