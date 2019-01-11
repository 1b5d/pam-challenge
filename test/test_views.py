from http import HTTPStatus


def test_root(client, app):
    """
    tests the homepage of the app.

    :param flask.testing.FlaskClient client:
    :param Flask app:
    :return:
    """
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK.value
