from flask_login import UserMixin
from LoginDemoApp import db, login_manager


@login_manager.user_loader
def load_user(email):
    return User.get(email)


class User(UserMixin):
    def __init__(self, username, email, password, usertype):
        self.email=email
        self.username=username
        self.password=password
        self.usertype = usertype

    def get_id(self):
        return self.email

    def set_type(self, t):
        self.usertype = t

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
            cur.execute('SELECT * FROM Visitor WHERE Username = "%s"' % username)
            if cur.fetchone():
                return User(username, email, password, "visitor")
            cur.execute('SELECT * FROM Staff WHERE Username = "%s"' % username)
            if cur.fetchone():
                return User(username, email, password, "staff")
            return User(username, email, password, "admin")
        return None
