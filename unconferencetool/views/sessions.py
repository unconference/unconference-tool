# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify, redirect, url_for
import unconferencetool.model as model

from flask_wtf import FlaskForm
from wtforms import HiddenField, TextField, BooleanField, validators

class CheckInForm(FlaskForm):
    session_id = HiddenField('Session', [validators.Required()])
    user_id = TextField('Attendee', [validators.Required()])
    share_details = BooleanField('I am happy for my email address to be shared with the other people in this session', [validators.Required()])

    def validate(self):
        """Validate the form."""
        initial_validation = super(CheckInForm, self).validate()
        if not initial_validation:
            return False

        attendee = model.Session_Attendee.query \
            .filter_by(session_id=self.session_id.data) \
            .filter_by(user_id=self.user_id.data) \
            .first()
        if attendee:
            self.user_id.errors.append('This Attendee has already been checked-in to this session')
            return False

        attendee = model.Unconference_Attendee.query \
            .filter_by(user_id=self.user_id.data) \
            .filter_by(unconference_id=model.Session.query.get(self.session_id.data).unconference.id) \
            .first()
        if not attendee:
            self.user_id.errors.append('Invalid Attendee')
            return False

        return True

class RemoveSessionAttendeeForm(FlaskForm):
    method = HiddenField("method", default="delete")
    session_id = HiddenField("session", [validators.Required()])
    user_id = HiddenField("attendee", [validators.Required()])

    def validate(self):
        """Validate the form."""
        initial_validation = super(RemoveSessionAttendeeForm, self).validate()
        if not initial_validation:
            return False
        
        attendee = model.Session_Attendee.query \
            .filter_by(session_id=self.session_id.data) \
            .filter_by(user_id=self.user_id.data) \
            .first()
        if not attendee:
            self.user_id.errors.append('This Attendee has not been checked-in to this session')
            return False

        return True

def list(unconference):
    Unconference = model.Unconference.query.get(unconference)

    return render_template("sessions.list.html", unconference=Unconference)

def check_in(unconference, session):
    form = CheckInForm(request.form)
    form.session_id.data = session

    Unconference = model.Unconference.query.get(unconference)
    Session = model.Session.query.get(session)

    if request.method == "POST" and form.validate():
        attendee = model.Session_Attendee()
        form.populate_obj(attendee)
        model.db.session.add(attendee)
        model.db.session.commit()

    form.user_id.data = ""
    form.share_details.data = False
    return render_template("sessions.check-in.html", form=form, unconference=Unconference, session=Session)

def attendees(unconference, session):
    form = RemoveSessionAttendeeForm(request.form)
    form.session_id.data = session

    Session = model.Session.query.get(session)
    Unconference = model.Unconference.query.get(unconference)

    if request.method == "POST" and form.validate():
        attendee = model.Session_Attendee.query \
            .filter_by(session_id=form.session_id.data) \
            .filter_by(user_id=form.user_id.data) \
            .first()
        model.db.session.delete(attendee)
        model.db.session.commit()
        return redirect(url_for('sessions.attendees', unconference=unconference, session=session), code=303)

    return render_template("sessions.attendees.html", unconference=Unconference, session=Session, form=form)