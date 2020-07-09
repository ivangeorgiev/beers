import hashlib
from datetime import datetime
import bcrypt
from core.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), unique=False, nullable=True)
    last_name = db.Column(db.String(255), unique=False, nullable=True)
    password = db.Column(db.String(255), unique=False, nullable=True)
    token = db.Column(db.String(255), unique=True, nullable=True)
    time_registered = db.Column(db.DateTime, default=datetime.utcnow)
    time_modified = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def set_token(self):
        self.token = hashlib.sha256((self.username + str(datetime.utcnow)).encode('utf-8')).hexdigest()
        db.session.add(self)
        db.session.commit()

    def clear_token(self):
        self.token = None
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password, salt)
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return bcrypt.checkpw(password, self.password)

    def __repr__(self):
        return '<User %r>' % (self.username, )

    @staticmethod
    def register(username, email, first_name, last_name):
        user = User()
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        db.session.add(user)
        db.session.commit()
        return user

