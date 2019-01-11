from collections import OrderedDict

import json
from flask import make_response
from http import HTTPStatus


def output_json(data, code, headers=None, message=None):
    """
    wrap all the responses with additional helpful attributes.
    :param data:
    :param int code:
    :param str message:
    :param dict headers:
    :return:
    """
    success = code < HTTPStatus.BAD_REQUEST.value
    if not success and data and  data.get('message'):
        message = data.pop('message')

    data = OrderedDict([
        ('result', OrderedDict([
            ('code', code),
            ('success', code < HTTPStatus.BAD_REQUEST.value),
            ('message', message),
        ])),
        ('data', data),
    ])
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp
