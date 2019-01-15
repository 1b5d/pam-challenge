from http import HTTPStatus

from flask import url_for

from app.db import EventDeviceType
from test.conftest import get_field


def test_report(client, app, db):
    response = client.get('/report')
    assert HTTPStatus.OK.value == response.status_code
    rows = get_field(response.json, 'rows')
    assert rows is not None

    assert 10 == len(rows)

    first_item = next(iter(rows))
    assert '8098d8c7-f290-43bf-862b-94adb4496ed9' == first_item['id']

    # TODO: assert all attributes
    for row in rows:
        assert get_field(row, 'device_type') in EventDeviceType.values() + [None]


def test_report_pagination(client, app, db):
    offset = 10
    limit = 5
    kwargs = {
        'offset': offset,
        'limit': limit
    }
    response = client.get(url_for('report.get', **kwargs))
    assert HTTPStatus.OK.value == response.status_code
    rows = get_field(response.json, 'rows')
    assert rows is not None
    assert offset == get_field(response.json, 'pagination.offset')

    assert limit == len(rows)

    first_item = next(iter(rows))
    assert '50b2fb89-0fe6-41f4-8d3a-83e8b12a1710' == first_item['id']


def test_report_group_by(client, app, db):
    kwargs = {
        'group_by': ['device_type'],
    }
    response = client.get(url_for('report.get', **kwargs))
    assert HTTPStatus.OK.value == response.status_code
    rows = get_field(response.json, 'rows')
    assert rows is not None

    for row in rows:
        assert get_field(row, 'device_type') in EventDeviceType.values() + [None]

        assert get_field(row, 'sum')
        assert get_field(row, 'count')
        assert get_field(row, 'avg')

        # TODO: assert all fields are missing except device_type and category
        assert not get_field(row, 'client')


def test_report_order_by(client, app, db):
    kwargs = {
        'order_by': ['-timestamp'],
    }
    response = client.get(url_for('report.get', **kwargs))
    assert HTTPStatus.OK.value == response.status_code
    rows = get_field(response.json, 'rows')
    assert rows is not None

    first_item = next(iter(rows))
    assert '4ce0b06c-b331-4124-9ca0-7e35a5ce36e5' == first_item['id']


def test_report_filter(client, app, db):
    kwargs = {
        'clients': [219],
    }
    response = client.get(url_for('report.get', **kwargs))
    assert HTTPStatus.OK.value == response.status_code
    rows = get_field(response.json, 'rows')
    assert rows is not None

    assert 2 == len(rows)
