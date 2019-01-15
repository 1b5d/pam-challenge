from http import HTTPStatus

from flask import render_template, make_response, request
from flask_restful import Resource

from app.db import db, Event, EventDeviceType


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

    def delete(self, uuid):
        Event.query.get_or_404(uuid)
        Event.query.filter(Event.id == uuid).delete()
        return None, HTTPStatus.OK.value

    def post(self):
        data = request.get_json()
        if data is None:
            return None, HTTPStatus.BAD_REQUEST.value

        # TODO: refactor the following into a method on DB access level
        event = Event(
            id=data.get('id'),
            device_type=EventDeviceType(data.get('device_type')),
            category=data.get('category'),
            client=data.get('client'),
            client_group=data.get('client_group'),
            timestamp=data.get('timestamp'),
            valid=data.get('valid'),
            value=data.get('value'))
        db.session.add(event)
        db.session.commit()

        return event.to_dict(), HTTPStatus.CREATED.value
