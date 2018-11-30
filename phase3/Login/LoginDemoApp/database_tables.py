from flask_login import UserMixin
from LoginDemoApp import db, login_manager


@login_manager.user_loader
def load_user(email):
    return User.get(email)


class User(UserMixin):
    def __init__(self, username, email, password):
        self.email=email
        self.username=username
        self.password=password
        self.type = ""

    def get_id(self):
        return self.email

    def set_type(self, t):
        self.type = t

    @staticmethod
    def get(email):
        """try to return user_id corresponding User object.
        This method is used by load_user callback function
        """
        if not email:
            return None
        cur = db.get_db().cursor()
        cur.execute('SELECT * FROM User where Email= "%s"' % email)
        rv = cur.fetchone()
        if rv:
            username, email, password = rv
            return User(username, email, password)
        return None
