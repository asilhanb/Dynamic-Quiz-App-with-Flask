from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(64), nullable=False)
    results  = db.relationship('Result', backref='user', lazy=True)

class Question(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    text       = db.Column(db.Text, nullable=False)
    topic      = db.Column(db.String(32), nullable=False)  # e.g. 'Flask', 'NLP'
    correct    = db.Column(db.String(128), nullable=False)
    choices    = db.Column(db.PickleType, nullable=False)  # ['A','B','C','D']

class Result(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score       = db.Column(db.Integer, nullable=False)
    timestamp   = db.Column(db.DateTime, default=datetime.utcnow)
