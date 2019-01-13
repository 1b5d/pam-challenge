from flask import render_template, make_response
from flask_restful import Resource

from app.db import Event


class Home(Resource):
    """
    A resource for home URL.
    """

    def get(self):
        return make_response(render_template('home.html'))


class EventResource(Resource):
    """
    A resource to handle events
    """

    def get(self, uuid):
        event = Event.query.get_or_404(uuid)
        return event.to_dict()
