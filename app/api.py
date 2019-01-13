from flask_restful import Api

from app.utils import output_json


class BaseApi(Api):
    """
    A customized version of Api to change the default content renderer
    """

    def __init__(self, *args, **kwargs):
        super(BaseApi, self).__init__(*args, **kwargs)
        self.representations = {
            'application/json': output_json,
        }


api = BaseApi(catch_all_404s=True)
