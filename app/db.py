from enum import Enum

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class EventDeviceType(Enum):
    DESKTOP = 'desktop'
    MOBILE = 'mobile'
    TABLET = 'tablet'


class Event(db.Model):
    id = db.Column(db.String, primary_key=True)
    device_type = db.Column(db.Enum(EventDeviceType), nullable=True)
    category = db.Column(db.Integer, nullable=True)
    client = db.Column(db.Integer, nullable=False)
    client_group = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    valid = db.Column(db.Boolean, nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Event %r>' % self.id

    def to_dict(self):
        """
        This method is supposed to serialize the object into json
        to be able to be returned by the API. I don't like this way
        of serializing, I would rather separate the serialization logic
        in a separate place than the models themselves. And even use
        a third-party library for that like marshmallow
        https://marshmallow.readthedocs.io/en/3.0/

        :return str:
        """
        return {
            'id': self.id,
            'device_type': self.device_type.value,
            'category': self.category,
            'client': self.client,
            'client_group': self.client_group,
            'timestamp': self.timestamp.isoformat(),
            'valid': self.valid,
            'value': self.value
        }
