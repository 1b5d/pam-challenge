from functools import wraps

from flask_restful import Api
from werkzeug.wrappers import Response as ResponseBase

from app.utils import output_json


def unpack(value):
    """Return a four tuple of data, code, message, and headers"""
    if not isinstance(value, tuple):
        return value, 200, None, {}

    try:
        data, code, message, headers = value
        return data, code, message, headers
    except ValueError:
        pass

    try:
        data, code, message = value
        return data, code, message, {}
    except ValueError:
        pass

    try:
        data, code = value
        return data, code, None, {}
    except ValueError:
        pass

    return value, 200, None, {}


class BaseApi(Api):
    """
    A customized version of Api to change the default content renderer
    """
    def __init__(self, *args, **kwargs):
        super(BaseApi, self).__init__(*args, **kwargs)
        self.representations = {
            'application/json': output_json,
        }

    def output(self, resource):
        """Wraps a resource (as a flask view function), for cases where the
        resource does not directly return a response object
        :param resource: The resource as a flask view function
        """

        @wraps(resource)
        def wrapper(*args, **kwargs):
            resp = resource(*args, **kwargs)
            if isinstance(resp, ResponseBase):  # There may be a better way to test
                return resp
            data, code, message, headers = unpack(resp)
            return self.make_response(data, code, message=message, headers=headers)

        return wrapper


api = BaseApi(catch_all_404s=True)
