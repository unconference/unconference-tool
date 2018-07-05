# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify
import unconferencetool.model as model
from flask_wtf import FlaskForm
from wtforms import BooleanField, TextField, PasswordField, SelectField, validators

class CheckInForm(FlaskForm):
    session_id = SelectField('Session', [validators.Required()] )
    user_id = TextField('Attendee (Start typing name)', [validators.Required()])
    share_details = BooleanField('I am happy for my email address to be shared with the other people in this session', [validators.Required()])


def attendees(unconference):
    if request.method == 'POST':
        if request.form['method'] == 'search':
            output = []
            results = model.db.session.query(model.Unconference_Attendee) \
                .filter(model.Unconference.id == unconference) \
                .filter((model.User.given_name.like(request.form['query'] + '%')) | (model.User.family_name.like(request.form['query'] + '%'))) \
                .all()
            for attendee in results:
                output.append({"id": attendee.user.id, "name": attendee.user.name, "email": attendee.user.email})
            return jsonify({"users":output})

def check_in(unconference):
    form = CheckInForm(request.form)
    sessions = model.db.session.query(model.Session) \
        .filter(model.Unconference.id == unconference) \
        .all()
    form.session_id.choices = [(str(g.id), g.location + ": " + g.title) for g in sessions]
    if request.method == "POST" and form.validate():
        attendee = model.Session_Attendee()
        form.populate_obj(attendee)
        model.db.session.add(attendee)
        model.db.session.commit()

    return render_template("check-in.sessions.html", form=form, unconference=unconference)
