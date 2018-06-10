# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
from flask import url_for

class TestRegistering:
    """Register a user."""

    def test_sees_error_message_if_passwords_dont_match(self, testapp):
        """Show error if passwords don't match."""
        # Goes to registration page
        res = testapp.get(url_for('index.hello'))
        # Fills out form, but passwords don't match
        form = res.forms['RegisterForm']
        form['username'] = 'foobar'
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secrets'
        # Submits
        res = form.submit()
        # sees error message
        assert 'Passwords must match' in res
