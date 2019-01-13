"""
these tests are supposed to be the closest form to functional tests,
this is the only level of testing in this app, typically we could add more levels
like acceptance tests and unit tests to cover different level of testing and
have a complete pyramid.
"""
from http import HTTPStatus

from test.conftest import get_field


def test_root(client, app):
    """
    tests the homepage of the app.

    :param flask.testing.FlaskClient client:
    :param Flask app:
    :return:
    """
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK.value


def test_event_get(client, app, db):
    """
    tests the get event endpoint

    :param flask.testing.FlaskClient client:
    :param Flask app:
    :param SQLAlchemy db:
    :return:
    """
    response = client.get('/event/8098d8c7-f290-43bf-862b-94adb4496ed9')
    assert response.status_code == HTTPStatus.OK.value
    assert get_field(response.json, 'id') == '8098d8c7-f290-43bf-862b-94adb4496ed9'
    # we can go on here and assert all the fields of the event
    # and we can parametrize the test to look cleaner :)
    assert get_field(response.json, 'device_type') == 'desktop'


def test_event_get_non_exist(client, app, db):
    response = client.get('/event/non_exist')
    assert response.status_code == HTTPStatus.NOT_FOUND.value


def test_event_delete(client, app, db):
    response = client.delete('/event/8098d8c7-f290-43bf-862b-94adb4496ed9')
    assert response.status_code == HTTPStatus.OK.value


def test_event_delete_non_exist(client, app, db):
    response = client.delete('/event/non_exist')
    assert response.status_code == HTTPStatus.NOT_FOUND.value


def test_event_create(client, app, db):
    response = client.post('event')
    assert response.status_code == HTTPStatus.CREATED.value
