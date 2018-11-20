from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from flask_login import LoginManager
from flaskext.mysql import MySQL

# Setup flask app
app = Flask(__name__)

# Secret key is required for wt-forms (you can choose anything to be your secret key)
app.config['SECRET_KEY'] = '34987rh3o4fhwofn23490'

# Setup mail server (I am using gmail)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'Your gmail address goes here'
app.config['MAIL_PASSWORD'] = 'Your gmail address password goes here'
mail = Mail(app)



# Setup Database
app.config['MYSQL_DATABASE_USER'] = 'cs4400_group32'
app.config['MYSQL_DATABASE_PASSWORD'] = 'AXtzKclB'
app.config['MYSQL_DATABASE_DB'] = 'cs4400_group32'
app.config['MYSQL_DATABASE_HOST'] = 'academic-mysql.cc.gatech.edu'
db = MySQL()
db.init_app(app)

# Setup Bcrypt (used to hash user passwords)
bcrypt = Bcrypt(app)

# Setup login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Used to generate tokens when sending confirmation mails
serializer = URLSafeTimedSerializer('iou3bv4839201b3wiqbw')

from LoginDemoApp import main
