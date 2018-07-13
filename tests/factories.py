# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory

import datetime
import unconferencetool.model as m

class BaseFactory(SQLAlchemyModelFactory):

    class Meta:
        abstract = True
        sqlalchemy_session = m.db.session

class UserFactory(BaseFactory):

    email = Sequence(lambda n: 'user{0}@example.com'.format(n))
    password = PostGenerationMethodCall('set_password', 'example')
    given_name = Sequence(lambda n: 'Test{0}'.format(n))
    family_name = Sequence(lambda n: 'User{0}'.format(n))

    class Meta:
        model = m.User

class UnconferenceFactory(BaseFactory):

    name = Sequence(lambda n: 'Unconference{0}'.format(n))
    tagline = Sequence(lambda n: 'Unconference{0} tagline text'.format(n))
    website = Sequence(lambda n: 'http://unconference{0}.test'.format(n))
    email = Sequence(lambda n: 'team@unconference{0}.test'.format(n))
    location = Sequence(lambda n: 'Unconference{0} location'.format(n))
    date = datetime.datetime.utcnow()

    class Meta:
        model = m.Unconference