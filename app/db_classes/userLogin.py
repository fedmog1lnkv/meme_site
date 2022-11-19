from flask_login import UserMixin
from app.db_classes.functions import secondsToDate

class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.getUserId(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])

    def get_info(self):
        return [self.__user['id'], self.__user['username'], secondsToDate(self.__user['time'])]

