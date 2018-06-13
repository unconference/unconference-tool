# -*- coding: utf-8 -*-

import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
    
bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Binary(128))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    mobile_no = db.Column(db.String(13))
    twitter = db.Column(db.String(80))
    job_title = db.Column(db.String(80))
    bio = db.Column(db.Text)

    roles = db.relationship("Roles", back_populates="user")

    def __init__(self, email, password=None, **kwargs):
        db.Model.__init__(self, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

class Roles(db.Model):
    __tablename__ = 'assigned_roles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship("User", back_populates="roles")

    def __init__(self, role, **kwargs):
        db.Model.__init__(self, role=role, **kwargs)

    def __repr__(self):
       return "<Roles(%s)>" % self.role
