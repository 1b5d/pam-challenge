import os

import pytest
from sqlalchemy import text

from app.app import create_app
from app.db import db as _db


@pytest.fixture(scope='session')
def app(request):
    """
    :param Request request:
    :return Flask:
    """
    app = create_app()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """
    A fixture to create a test DB for our session and destroy it after
    running the tests

    :param Flask app:
    :param Request request:
    :return SQLAlchemy:
    """
    def teardown():
        _db.session.commit()
        _db.drop_all()

    _db.app = app
    _db.create_all()

    """
    The following will execute an SQL file to insert some fixture data in the database
    to make the tests ready. I don't really like this way of populating data.
    I think it's better to insert fixture data programmatically which is described 
    in yaml / json files.
    """
    with open(os.path.join(app.root_path, 'test/fixtures/test_data.sql')) as f:
        engine = _db.create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'))
        connection = engine.connect()
        connection.execute(text(f.read()))
        connection.close()

    request.addfinalizer(teardown)
    return _db


def get_field(data, field):
    if not field or not data:
        return None
    fields = field.split('.')

    for field in fields:
        data = data.get(field, {})

    return data
