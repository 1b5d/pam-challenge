from flask import render_template, make_response
from flask_restful import Resource


class Home(Resource):
    """
    A resource for home URL.
    """
    def get(self):
        return make_response(render_template('home.html'))
