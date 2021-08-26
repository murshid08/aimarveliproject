from source import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__="users"


    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(48),unique=True,nullable=False)
    password=db.Column(db.String(148),nullable=False)
    posts=db.relationship('Post',backref='author',lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category=db.Column(db.String(48),nullable=False)
    cat_fields=db.Column(db.String(48),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
