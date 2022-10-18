from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'capy615eee5f2d8953d2a3f56e6cbf4564f71a541ec85e81382e3fed49c53814a94bbara'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///howtocode.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-warning'


from trchl import routes
