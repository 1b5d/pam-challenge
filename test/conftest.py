import pytest

from app.app import create_app


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


def get_field(data, field):
    if not field or not data:
        return None
    fields = field.split('.')

    for field in fields:
        data = data.get(field, {})

    return data
