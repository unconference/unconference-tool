# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify, redirect, url_for
from werkzeug.datastructures import CombinedMultiDict
import unconferencetool.model as model
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import BooleanField, TextField, PasswordField, SelectField, HiddenField, TextAreaField, validators
from wtforms.fields.html5 import DateField 
import io, csv, datetime, unicodedata

class UnconferenceForm(FlaskForm):
    name = TextField('Name', [validators.Required(), validators.Length(min=1, max=30, message='Names must be less than 30 charachters.')])
    tagline = TextField('TagLine', [validators.Length(min=0, max=140, message='Taglines must be less than 140 charachters.')])
    twitter_handle = TextField('Twitter', [validators.Length(min=0, max=80, message='Twitter names must be less than 80 charachters.')])
    hashtag = TextField('Hashtag', [validators.Length(min=0, max=20, message='Hashtags must be less than 20 charachters.')])
    website = TextField('Website', [validators.Required(), validators.URL(), validators.Length(min=10, max=140, message='Website must be less than 140 charachters.')])
    email = TextField('Email', [validators.Required(), validators.email(), validators.Length(min=5, max=30, message='Email must be less than 30 charachters.')])
    location = TextField('Location', [validators.Required(), validators.Length(min=1, max=140, message='Location must be less than 140 charachters.')])
    date = DateField('Date', [validators.Required()])
    other_info = TextAreaField('Other')

class UploadAttendeesForm(FlaskForm):
    method = HiddenField("method", default="upload")
    csv_file = FileField('CSV File with a header row in format: given_name, family_name, email', validators=[FileRequired(), FileAllowed(['csv'], 'Only .csv files permitted')])

def index(unconference):
    Unconference = model.Unconference.query.get(unconference)
    return render_template("unconference.index.html", unconference=Unconference)

def locations(unconference, location=None):
    Unconference = model.Unconference.query.get(unconference)

    if location != None:
        Location = model.Location.query \
            .filter_by(unconference_id=unconference) \
            .filter_by(id=location) \
            .first()
        return render_template("unconference.locations.sessions.html", unconference=Unconference, location=Location)

    return render_template("unconference.locations.html", unconference=Unconference)

def attendees(unconference):
    form = UploadAttendeesForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST':
        if request.form['method'] == 'search':
            output = []
            results = model.Unconference_Attendee.query \
                .filter_by(unconference_id=unconference) \
                .join(model.User) \
                .filter((model.User.given_name.ilike(request.form['query'] + '%')) | (model.User.family_name.ilike(request.form['query'] + '%'))) \
                .all()
            for attendee in results:
                output.append({"id": attendee.user.id, "name": attendee.user.name, "email": attendee.user.email})
            return jsonify({"users":output})
        if request.form['method'] == 'upload' and form.validate():
            reader = csv.DictReader(io.StringIO(form.csv_file.data.read().decode("utf-8-sig"), newline=None))
            Unconference = model.Unconference.query.get(unconference)
            for row in reader:
                try:
                    u = model.User.query.filter_by(email=row['email']).first()
                    if not u:
                        given_name = unicodedata.normalize('NFKD', row['given_name']).encode('ASCII', 'ignore')
                        family_name = unicodedata.normalize('NFKD', row['family_name']).encode('ASCII', 'ignore')
                        u = model.User(row['email'], None, given_name=given_name.decode('ascii'), family_name=family_name.decode('ascii'))
                    u.unconferences.append(model.Unconference_Attendee(role="ATN",unconference=Unconference))
                    model.db.session.add(u)
                except:
                    model.db.session.rollback()
            try:
                model.db.session.commit()
            except:
                model.db.session.rollback()
    
    Unconference = model.Unconference.query.get(unconference)
    return render_template("unconference.attendees.html", form=form, unconference=Unconference)

def list():
    form = UnconferenceForm(request.form)
    if request.method == "POST" and form.validate():
        unconf = model.Unconference()
        form.populate_obj(unconf)
        model.db.session.add(unconf)
        model.db.session.commit()
    
    unconferences = model.Unconference.query.all()
    return render_template("unconference.list.html", form=form, unconferences=unconferences)

def bulk_sessions(unconference):
    Unconference = model.Unconference.query.get(unconference)
    sessions = model.Session.query \
            .filter_by(unconference_id=unconference) \
            .all()
    if not sessions:
        rooms = ["St James A", "St James B", "Westminster A", "Westminster B", "Shelley", "Wordsworth", "Chaucer", "Keats", "Burns", "Wesley", "Moore", "Rutherford", "Byron", "Abbey"]
        sessions = ["Session 1", "Session 2", "Session 3", "Session 4", "Session 5"]
        for room in rooms:
            l = model.Location(name=room, unconference=Unconference)
            for session in sessions:
                s = model.Session(location=l, title=session, unconference=Unconference, start=datetime.datetime.utcnow())
                model.db.session.add(s)
        model.db.session.commit()

    return redirect(url_for('sessions.list', unconference=unconference), code=303)
