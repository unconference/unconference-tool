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
    password = db.Column(db.Binary())
    given_name = db.Column(db.String(30))
    family_name = db.Column(db.String(30))
    twitter_handle = db.Column(db.String(80))
    job_title = db.Column(db.String(80))
    bio = db.Column(db.Text)
    mobile_no = db.Column(db.String(13))
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    superuser = db.Column(db.Boolean, nullable=False, default=False)

    unconferences = db.relationship("Unconference_Attendee", back_populates="user", cascade="all, delete, delete-orphan")
    volunteer_assignments = db.relationship("Volunteer_Assignments", back_populates="user", cascade="all, delete, delete-orphan")
    pitches = db.relationship("Session", back_populates="pitched_by")
    sessions_attended = db.relationship("Session_Attendee", back_populates="user", cascade="all, delete, delete-orphan")

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
    def name(self):
        return '{0} {1}'.format(self.given_name.title(), self.family_name.title())

class Unconference(db.Model):
    __tablename__ = 'unconferences'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    tagline = db.Column(db.String(140))
    twitter_handle = db.Column(db.String(80))
    hashtag = db.Column(db.String(20))
    website = db.Column(db.String(140), nullable=False)
    email = db.Column(db.String(130), nullable=False)
    location = db.Column(db.String(140), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    other_info = db.Column(db.Text())
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    locations = db.relationship("Location", back_populates="unconference", cascade="all, delete, delete-orphan")
    sessions = db.relationship("Session", back_populates="unconference", cascade="all, delete, delete-orphan")
    attendees = db.relationship("Unconference_Attendee", back_populates="unconference", cascade="all, delete, delete-orphan")
    volunteer_roles = db.relationship("Volunteer_Role", back_populates="unconference", cascade="all, delete, delete-orphan")
    #volunteers
    #organisers

class Unconference_Attendee(db.Model):
    __tablename__ = 'unconference_attendees'
    __table_args__ = (db.UniqueConstraint('unconference_id', 'user_id', name='_unconference_user_uc'),)

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(10), nullable=False) #Enum "ORG", "VOL", "ATN"

    unconference_id = db.Column(db.Integer, db.ForeignKey('unconferences.id'), nullable=False)
    unconference = db.relationship("Unconference", back_populates="attendees")

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="unconferences")

    #volunteer_roles

class Volunteer_Role(db.Model):
    __tablename__ = 'volunteer_roles'

    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(140), nullable=False)
    Description = db.Column(db.Text(), nullable=False)

    unconference_id = db.Column(db.Integer, db.ForeignKey('unconferences.id'), nullable=False)
    unconference = db.relationship("Unconference", back_populates="volunteer_roles")

    assigned_to = db.relationship("Volunteer_Assignments", back_populates="role", cascade="all, delete, delete-orphan")

class Volunteer_Assignments(db.Model):
    __tablename__ = 'volunteer_assignemnts'

    id = db.Column(db.Integer, primary_key=True)

    role_id = db.Column(db.Integer, db.ForeignKey('volunteer_roles.id'), nullable=False)
    role = db.relationship("Volunteer_Role", back_populates="assigned_to")

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", back_populates="volunteer_assignments")

class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))

    unconference_id = db.Column(db.Integer, db.ForeignKey('unconferences.id'), nullable=False)
    unconference = db.relationship("Unconference", back_populates="locations")

    sessions = db.relationship("Session", back_populates="location")

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(140), nullable=False)
    notes_url = db.Column(db.String(140))

    unconference_id = db.Column(db.Integer, db.ForeignKey('unconferences.id'), nullable=False)
    unconference = db.relationship("Unconference", back_populates="sessions")

    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    location = db.relationship("Location", back_populates="sessions")

    pitched_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitched_by = db.relationship("User", back_populates="pitches")

    attendees = db.relationship("Session_Attendee", back_populates="session", cascade="all, delete, delete-orphan")

class Session_Attendee(db.Model):
    __tablename__ = 'session_attendees'
    __table_args__ = (db.UniqueConstraint('session_id', 'user_id', name='_session_user_uc'),)

    id = db.Column(db.Integer, primary_key=True)
    share_details = db.Column(db.Boolean, nullable=False, default=False)

    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    session = db.relationship("Session", back_populates="attendees")

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", back_populates="sessions_attended")
