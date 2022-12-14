from datetime import datetime
from flask_login import UserMixin
from trchl import db, login_manager

# This code tells to login_manager to keep track of id_user field
@login_manager.user_loader
def load_user(id_user):
    return User.query.get(id_user)

# Class to be instantiated each time a user registers
class User(db.Model, UserMixin):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    fullname = db.Column(db.String(50), nullable=True, default='')
    email = db.Column(db.String(50), unique=True, nullable=False)
    passwd = db.Column(db.String(30), nullable=False)
    place = db.Column(db.String(50), default='')
    profile_pic = db.Column(db.String(3000), default='default.jpg')
    fav_tech = db.Column(db.String(150), default='')
    posts = db.relationship('Post', backref='author', lazy=True)


    def count_posts(self):
        return len(self.posts)
        

    def get_id(self):
        return self.id_user

# Class to be instantiated each time a post is made
class Post(db.Model):
    id_post = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)