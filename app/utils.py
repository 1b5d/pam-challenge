import json

from flask import make_response


def output_json(data, code, headers=None):
    """
    wrap all the responses with additional helpful attributes.
    :param data:
    :param int code:
    :param dict headers:
    :return:
    """
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp
