from flask_login import UserMixin
from LoginDemoApp import db, login_manager


@login_manager.user_loader
def load_user(username):
    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM User where Username=$s' % username)
    rv = cur.fetchall()
    return rv


