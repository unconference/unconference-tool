# -*- coding: utf-8 -*-

from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import BooleanField, TextField, PasswordField, validators

class RegistrationForm(FlaskForm):
    username = TextField('Username', [validators.Required(), validators.Length(min=4, max=25, message='Username must be between 4 and 25 charachters.')])
    email = TextField('Email Address', [validators.Required(), validators.Length(min=6, max=35, message=''), validators.Email()])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password',  [
        validators.Required(),
        validators.EqualTo('password', message='Passwords must match')
    ])
    accept_tos = BooleanField('I accept the <a href="">TOS</a>', [validators.Required()])

def hello():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        pass
    
    return render_template("login.html", form=form)
