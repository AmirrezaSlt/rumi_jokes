from datetime import datetime
from rumi_jokes import db, db2, db3, login_manager
from flask_login import UserMixin
from uuid import uuid4
from pymongo.collection import ObjectId


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    major_id = db.Column(db.Integer, db.ForeignKey('majors.id'))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.jokes}')"


class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    joke_1 = db.Column(db.Integer, nullable=False)
    joke_2 = db.Column(db.Integer, nullable=False)
    priority = db.Column(db.Integer)
    expired = db.Column(db.Boolean, default=0)
    winner = db.Column(db.Boolean)


class Major(db.Model):
    __tablename__ = 'majors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)


class Joke(db2.Document):
    # _id = db2.ObjectIdField(default=ObjectId())
    content = db2.StringField(required=True)
    views = db2.IntField(default=0)
    score = db2.IntField(default=0)
    author = db2.IntField(required=True)


class Skill(db3.Model):
    __table_name__ = 'skills'
    user = db3.columns.Integer(primary_key=True)
    sname = db3.columns.Set(db3.columns.Text)
