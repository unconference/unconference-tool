# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify
import unconferencetool.model as model

def attendees(unconference, session):
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
