from flask_login import UserMixin
from datetime import datetime
from pac import db, manager


class Note (db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    intro = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Note %r>' % self.id


class user_ac (db.Model, UserMixin):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100),  nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)


@manager.user_loader
def load_user(user_id):
    return user_ac.query.get(user_id)
