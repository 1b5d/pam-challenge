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
    assert HTTPStatus.OK.value == response.status_code


def test_event_get(client, app, db):
    """
    tests the get event endpoint

    :param flask.testing.FlaskClient client:
    :param Flask app:
    :param SQLAlchemy db:
    :return:
    """
    response = client.get('/event/8098d8c7-f290-43bf-862b-94adb4496ed9')
    assert HTTPStatus.OK.value == response.status_code
    assert '8098d8c7-f290-43bf-862b-94adb4496ed9' == get_field(response.json, 'id')

    # TODO: assert all attributes of the event
    # and we can parametrize the test to look cleaner :)
    assert 'desktop' == get_field(response.json, 'device_type')


def test_event_get_non_exist(client, app, db):
    response = client.get('/event/non_exist')
    assert HTTPStatus.NOT_FOUND.value == response.status_code


def test_event_delete(client, app, db):
    response = client.delete('/event/8098d8c7-f290-43bf-862b-94adb4496ed9')
    assert HTTPStatus.OK.value == response.status_code


def test_event_delete_non_exist(client, app, db):
    response = client.delete('/event/non_exist')
    assert HTTPStatus.NOT_FOUND.value == response.status_code


def test_event_create(client, app, db):
    uuid = '3fa85f64-5717-4562-b3fc-2c963f66afa6'
    timestamp = '2019-01-11T23:37:49.897Z'
    response = client.post('event', json={
        'id': uuid,
        'device_type': 'desktop',
        'category': 1,
        'client': 1,
        'client_group': 1,
        'timestamp': timestamp,
        'valid': True,
        'value': 1.0
    })
    assert HTTPStatus.CREATED.value == response.status_code
    # TODO: assert all attributes of the event

    assert uuid == get_field(response.json, 'id')
    assert 'desktop' == get_field(response.json, 'device_type')
    assert timestamp == get_field(response.json, 'timestamp')
