# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify
import unconferencetool.model as model

def list(unconference):
    sessions = model.Session.query \
        .filter(model.Unconference.id == unconference) \
        .all()
    Unconference = model.Unconference.query.get(unconference)

    return render_template("sessions.list.html", unconference=Unconference, sessions=sessions)

def attendees(unconference, session):
    Session = model.Session.query.get(session)
    Unconference = model.Unconference.query.get(unconference)

    return render_template("sessions.attendees.html", unconference=Unconference, session=Session)